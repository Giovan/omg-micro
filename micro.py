import os

import delegator
import yaml
import waitress
from flask import Flask


YAML_TEMPLATE = """
omg: 1
""".strip()


class Service:
    def __init__(self, root_path='.'):
        self.root_path = os.path.abspath(root_path)
        self.flask = Flask()
        self._services = []

    def _generate_yaml(self):
        data = yaml.safe_loads(YAML_TEMPLATE)
        return data

    @staticmethod
    def _format_args(**args):
        args = [f'{k}={v}' for (k, v) in args.items()]
        return ' '.join(args)

    def ensure_yml(self, overwrite=True):
        pass

    def build(self):
        self.ensure_yml()
        c = delegator.run('omg build')
        return c.ok

    def run(self, command, **args):
        pass

    def serve(self, **kwargs):
        waitress.serve(app=self.flask, **kwargs)

    def register(self, name=None, path=None):
        def callback(func, **kwargs):
            pass

        return callback
        # self._services.append(f)
        # print(kwargs)
        # return


service = Service()


@service.register(name='query', path='/query')
def query(uri):
    return uri
