from uuid import uuid4
import pytest


@pytest.fixture
def f():
    def work(prefix=''):
        return f'{prefix}{uuid4().hex}'

    return work


@pytest.fixture
def micro():
    import micro

    return micro


@pytest.fixture
def service(micro):
    return micro.Service(name='service')


def test_assertion(f):
    assert True


def test_basic_service_registation(f, service):
    service.register(f=f)

    assert 'work' in service.services


def test_named_service_registation(f, service):
    service.register(f=f, name='test')

    assert 'test' in service.services


def test_cutom_uri_service_registation(f, service):
    service.register(f=f, name='test', uri='/not-test')

    assert 'test' in service.services
    assert service.services['test']['uri'] == '/not-test'
