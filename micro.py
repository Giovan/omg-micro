import os
import functools

import delegator
import logme
import yaml
import waitress
from flask import Flask, jsonify, request, Response, make_response

__all__ = ['Service']

DEFAULT_PORT = '8080'
DEFAULT_ARG_TYPE = str
PORT = int(os.environ.get('PORT', DEFAULT_PORT))
YAML_TEMPLATE = """
omg: 1
actions:
""".strip()
DOCKERFILE_TEMPLATE = f"""
FROM kennethreitz/pipenv

COPY . /app

CMD ["python3", "service.py"]
""".strip()


class MicroserviceDockerfile:
    @property
    def _dockerfile_path(self):
        return './Dockerfile'

    def ensure_dockerfile(self, skip_if_exists=True):
        if skip_if_exists:
            if os.path.isfile(os.path.abspath(self._dockerfile_path)):
                self.logger.debug(
                    f'Dockerfile {self._dockerfile_path!r} already exists!'
                )
            else:
                self.logger.info(f'Writing {self._dockerfile_path!r} to disk.')

                # Write the template Dockerfile to disk.
                with open(self._dockerfile_path, 'w') as f:
                    f.write(DOCKERFILE_TEMPLATE)


@logme.log
class MicroserviceYML:
    @property
    def _yaml_path(self):
        return f'./microservice.yml'

    def _render(self):
        data = yaml.safe_load(YAML_TEMPLATE)
        data['actions'] = {}

        for endpoint in self.endpoints.values():
            # data['actions'][endpoint['name']] = {}

            data['actions'][endpoint['name']] = {
                'help': endpoint['f'].__doc__,
                'output': {'type': 'string'},
                'http': {
                    'path': endpoint['path'],
                    'method': endpoint['method'],
                    'port': PORT,
                },
            }

        return data

    def ensure_yaml(self, skip_if_exists=True):
        if skip_if_exists:
            if os.path.isfile(os.path.abspath(self._yaml_path)):
                self.logger.debug(
                    f'Microservice Manifest {self._yaml_path!r} already exists!'
                )
            else:
                self.logger.info(f'Writing {self._yaml_path!r} to disk.')
                with open(self._yaml_path, 'w') as f:
                    f.write(yaml.safe_dump(self._render()))


@logme.log
class Microservice(MicroserviceYML, MicroserviceDockerfile):
    def __init__(self, name, root_path='.'):
        self.name = name
        self.root_path = os.path.abspath(root_path)
        self.endpoints = {}

        self.logger.debug(f'Initiating {self.name!r} service.')

        self.flask = Flask(__name__)

    def ensure(self, skip_if_exists=True):
        # Ensure the Dockerfile exists.
        self.ensure_dockerfile(skip_if_exists=skip_if_exists)

        # Ensure the YAML exists.
        self.ensure_yaml(skip_if_exists=skip_if_exists)

    def serve(self, **kwargs):

        # Bind to PORT, automatically.
        listen = f'*:{PORT}'
        if 'listen' in kwargs:
            listen = kwargs.pop('listen')

        self.logger.info(f'Serving on: {listen!r}')

        waitress.serve(app=self.flask, listen=listen, **kwargs)
        pass

    def add(
        self, f, *, name: str = None, path: str = None, method: str = 'get'
    ):
        # Infer the service name.
        name = name or f.__name__
        # Infer the service URI. Note: Expects '/', like Flask.
        path = path or f'/{name}'

        # Store the service, for later use.
        self.endpoints[name] = {
            'name': name,
            'path': path,
            'f': f,
            'method': method,
        }

        self._register_endpoints()

    def register(self, path, **kwargs):
        def decorator(f):
            self.add(f=f, path=path, **kwargs)
            return f

        return decorator

    def _register_endpoint(self, service):
        f = service['f']
        rule = service['path']
        endpoint = service['name']

        def view_func(**kwargs):

            # Check type annoytations of enpoint function,
            # Flag query parameters as usable, if it appears to be applicable.

            params = {}
            json = request.get_json()

            # Whitelist function arguments.
            for arg in f.__annotations__:
                if arg in request.args:
                    params[arg] = request.args[arg]

                if json:
                    if arg in json:
                        params[arg] = json[arg]

                # TODO:; grab values from HTTP Headers.
                # TODO:  gab balues from multipart upload.

            # Pass all query parameters as function arguments, if applicable.
            self.logger.info(f'Calling {rule!r} with args: {params!r}.')

            # Call the function.
            try:
                result = f(**params)
            except TypeError:
                keys = repr([v for v in f.__annotations__.keys()])
                result = make_response(
                    f"Invalid parameters passed. Expected: {keys}", 412
                )
                self.logger.warn(
                    f'Calling {rule!r} with args: {params!r} failed!'
                )

            # Return the result immediately, if it is a Flask Response.
            if isinstance(result, Response):
                return result

            # Return the result, relying on JSON, then falling back to bytes.
            try:
                return jsonify(result)
            except ValueError:
                return result

        self.logger.debug(f'Registering Flask endpoint: {rule!r}')
        self.flask.add_url_rule(
            rule=rule, endpoint=endpoint, view_func=view_func
        )

    def _register_endpoints(self):
        for endpoint in self.endpoints.values():
            self._register_endpoint(endpoint)


Service = Microservice
