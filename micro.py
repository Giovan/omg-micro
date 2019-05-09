import os

import delegator
import yaml

import waitress
from flask import Flask

__all__ = ['Service']


PORT = os.environ.get('PORT')
YAML_TEMPLATE = """
omg: 1
""".strip()


class MSYML:
    def _generate_yaml(self):
        data = yaml.safe_loads(YAML_TEMPLATE)
        return data

    def ensure_yml(self, overwrite=True):
        pass


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


class Service(MSYML, OMGCLI):
    def __init__(self, root_path='.'):
        self.root_path = os.path.abspath(root_path)
        self.flask = Flask(__name__)
        self._services = []

    def serve(self, **kwargs):
        waitress.serve(app=self.flask, **kwargs)
        pass

    def register(self, name=None, path=None):
        def callback(func, **kwargs):
            # define flask route
            # register flask route
            pass

        return callback


service = Service()


@service.register(name='query', path='/query')
def query(uri):
    return uri
