import delegator
import yaml


YML_TEMPLATE = """
omg: 1
""".strip()


class Microservice:
    def __init__(self):
        pass

    def _generate_yaml(self):
        data = yaml.safe_loads(YML_TEMPLATE)
        return data

    @staticmethod
    def _format_args(**args):
        args = [f'{k}={v}' for (k, v) in args.items()]
        return ' '.join(args)

    def ensure_yml(self, overwrite=True):
        pass

    def build(self):
        self.ensure_yml()
        c = delegator.run("omg build")
        return c.ok

    def run(self, command, **args):
        self.ensure_yml()
        args = self._format_args(**args)
        pass


omg = Microservice()


@omg.register(name='query', path="/query")
def query(uri: str) -> str:
    return uri
