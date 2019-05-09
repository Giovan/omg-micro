import os

import delegator
import logme
import yaml

import waitress
from flask import Flask

__all__ = ['Service']


PORT = os.environ.get('PORT')
YAML_TEMPLATE = """
omg: 1
""".strip()


@logme.log
class MSYML:
    def _generate_yaml(self):
        data = yaml.safe_loads(YAML_TEMPLATE)
        return data

    def ensure_yml(self, overwrite=True):
        pass


@logme.log
class OMGCLI:
    @staticmethod
    def _format_args(**args):
        args = [f'{k}={v}' for (k, v) in args.items()]
        return ' '.join(args)

    def build(self):
        self.ensure_yml()
        c = delegator.run('omg build')
        return c.ok

    def run(self, command, **args):
        pass


@logme.log
class Service(MSYML, OMGCLI):
    def __init__(self, name, root_path='.'):
        self.name = name
        self.root_path = os.path.abspath(root_path)

        self.logger.info(f'Initiating {self.name!r} service.')

        self.flask = Flask(__name__)
        self._services = []

    def serve(self, **kwargs):
        self.logger.info(f'Serving on port: f{PORT}')

        # Bind to PORT, automatically.
        bind = f'*:{PORT}'
        if 'bind' in kwargs:
            bind = kwargs.pop('bind')

        waitress.serve(app=self.flask, bind=bind, **kwargs)
        pass

    def register(self, name=None, path=None):
        def callback(func, **kwargs):
            # define flask route
            # register flask route
            pass

        return callback


service = Service(name='service')


@service.register(name='query', path='/query')
def query(uri):
    return uri
