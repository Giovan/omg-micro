import delegator
import yaml


class Microservice:
    def __init__(self):
        pass

    def ensure_yml(self, overwrite=True):
        pass

    def build(self):
        self.ensure_yml()
        c = delegator.run("omg build")

    def run(self, command, **args):
        self.ensure_yml()
        pass


omg = Microservice()


@omg.register(name='query', path="/query")
def query(uri: str) -> str:
    return uri
