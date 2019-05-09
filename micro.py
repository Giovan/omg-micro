import os


import delegator
import logme
import yaml
import waitress
from flask import Flask
from docopt import docopt

__all__ = ['Service']

DEFAULT_PORT = '8080'
PORT = os.environ.get('PORT', DEFAULT_PORT)
YAML_TEMPLATE = """
omg: 1
""".strip()
DOCKERFILE_TEMPLATE = """
FROM kennethreitz/pipenv

COPY . /app

CMD ["micro", "{entrypoint}", "serve"]
""".strip()
DEFAULT_ARG_TYPE = str
DEFAULT_ENTRYPOINT = 'server.py:service'


class MicroserviceDockerfile:
    @property
    def _dockerfile_path(self):
        return f'./Dockerfile'

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
                    f.write(
                        DOCKERFILE_TEMPLATE.format(
                            entrypoint=DEFAULT_ENTRYPOINT
                        )
                    )


@logme.log
class MicroserviceYML:
    @property
    def _yaml_path(self):
        return f'./microservice.yml'

    def _render(self):
        data = yaml.safe_load(YAML_TEMPLATE)
        for service in self.services:
            pass

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

        data = self._render()


@logme.log
class MicroserviceOMG:
    @staticmethod
    def _format_args(**args):
        args = [f'{k}={v}' for (k, v) in args.items()]
        return '-a '.join(args)

    def build(self):
        # Ensure the Dockerfile exists.
        self.ensure_dockerfile()

        # Ensure the YAML exists.
        self.ensure_yaml()

        c = delegator.run('omg build')
        return c.ok

    def run(self, command, **args):
        self.ensure()

        self.logger.info(f"Running '{self.name}/{command}' endpoint.")
        # Prepare CLI arguments.
        args = self._format_args(**args)
        c = delegator.run(f'omg run {args}')
        return c.out


@logme.log
class Microservice(MicroserviceOMG, MicroserviceYML, MicroserviceDockerfile):
    def __init__(self, name, root_path='.'):
        self.name = name
        self.root_path = os.path.abspath(root_path)
        self.services = {}

        self.logger.debug(f'Initiating {self.name!r} service.')

        self.flask = Flask(__name__)

    def ensure(self):
        # Ensure the Dockerfile exists.
        self.ensure_dockerfile()

        # Ensure the YAML exists.
        self.ensure_yaml()

    def serve(self, **kwargs):

        # Bind to PORT, automatically.
        listen = f'*:{PORT}'
        if 'listen' in kwargs:
            listen = kwargs.pop('listen')

        self.logger.info(f'Serving on: {listen!r}')

        waitress.serve(app=self.flask, listen=listen, **kwargs)
        pass

    @staticmethod
    def _args_for_f(f):
        # print(f.__code__.__defaults__)
        return f.__annotations__

    def register(self, f, *, name: str = None, uri: str = None):
        # Infer the service name.
        name = name or f.__name__
        # Infer the service URI. Note: Expects '/', like Flask.
        uri = uri or f'/{name}'

        self.logger.debug(f"Registering '{self.name}{uri}'.")

        # Store the service, for later use.
        self.services[name] = {
            'name': name,
            'uri': uri,
            'f': f,
            'args': self._args_for_f(f),
        }


Service = Microservice


def cli():
    """Micro, the OMG service generator.

    Usage:
        micro <entrypoint>
    """
    args = docopt(cli.__doc__)
    entrypoint = args['<entrypoint>']

    # Default to :service.
    if ':' not in entrypoint:
        entrypoint = f'{entrypoint}:service'

    entrypoint, entry_attr = entrypoint.split(':')

    # Strip .py from entrypoint file name.
    if entrypoint.endswith('.py'):
        entrypoint = entrypoint[0 : -1 * len('.py')]

    # Import the actual service.
    service = getattr(__import__(entrypoint), entry_attr)

    # Ensure the files exist.
    service.ensure()

    # Serve the HTTP service.
    service.serve()


if __name__ == '__main__':
    cli()
