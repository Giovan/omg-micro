# OMG: Micro Framework

A micro-framework for the **[Open Microservices Guide](https://microservices.guide/)**, for suppportive code written in Python 3.6+.

**Note**: this is pre-release software, and is subject to improvement. Contributions are welcome!

# Intended / Example Usage

```shell
$ cat service.py
```
```python
import micro

def test_function(test: str):
    return {'test': test}

service = micro.Service(name='service')
service.register(f=test_function)
```

If not available on disk, the required `Dockerfile` and `microservice.yml` files will automatically be generated, for your application.

Running your microservice:
```shell
$ micro service.py
2019-05-09 14:45:39,342 - micro - DEBUG - Initiating 'uuid' service.
2019-05-09 14:45:39,344 - micro - DEBUG - Registering Flask endpoint: '/uuid4'
2019-05-09 14:45:39,344 - micro - DEBUG - Dockerfile './Dockerfile' already exists!
2019-05-09 14:45:39,345 - micro - DEBUG - Microservice Manifest './microservice.yml' already exists!
2019-05-09 14:45:39,346 - micro - INFO - Serving on: '*:8080'
```

## Installation

```shell
$ pip install omg-micro

✨ 🍰 ✨
