# OMG: Micro Framework

A micro-framework for the excellent **[Open Microservices Guide](https://microservices.guide/)**, for suppportive code written in Python 3.6+.

**Note**: this is pre-release software, and is subject to improvement. Contributions are welcome!

# Intended / Example Usage

```shell
$ cat service.py
```
```python
import micro
from uuid import uuid4

service = micro.Service(name='uuid')

@service.register('/uuid4', method='get')
def gen_uuid4(prefix: str) -> str:
    """Generates a UUID, with a given prefix."""
    return f'{prefix}{uuid4().hex}'

# Alternative Syntax:
# service.add(f=gen_uuid4)

if __name__ == '__main__':
    service.serve()
```

If not available on disk, the required `Dockerfile` and `microservice.yml` files will automatically be generated, for your application:

```shell
$ cat microservice.yml
actions:
  uuid4:
    help: Generates a UUID, with a given prefix.
    http:
      method: get
      path: /uuid4
      port: 8080
    output:
      type: string
omg: 1
```

```shell
$ cat Dockerfile
FROM kennethreitz/pipenv
COPY . /app
CMD ["python3", "service.py"]
```

Now, run your microservice!

```shell
$ python service.py
2019-05-09 14:45:39,342 - micro - DEBUG - Initiating 'uuid' service.
2019-05-09 14:45:39,344 - micro - DEBUG - Registering Flask endpoint: '/uuid4'
2019-05-09 14:45:39,344 - micro - DEBUG - Dockerfile './Dockerfile' already exists!
2019-05-09 14:45:39,345 - micro - DEBUG - Microservice Manifest './microservice.yml' already exists!
2019-05-09 14:45:39,346 - micro - INFO - Serving on: '*:8080'
```

Or, use the [omg-cli](https://github.com/microservices/omg-cli):

```shell
$ omg run uuid4 -a prefix='user-'
…
```

## Installation

```shell
$ pip install omg-micro
```

**P.S.** This doesn't work yet. :)

✨ 🍰 ✨
