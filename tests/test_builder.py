from unittest.mock import Mock

import pytest

from src.builder import Builder

SIGNATURE = 'SIGNATURE'
API_KEY = 'API_KEY'
RESPONSE_OBJ = {'key': 1}


@pytest.fixture()
def mocked_deps(mocker):
    mocker.patch('src.builder.get_hmac_hash', return_value=SIGNATURE)
    mocker.patch('src.builder.get_secret_key', return_value='MY_SECRET_KEY')
    mocker.patch('src.builder.get_api_key_header', return_value={'X-MBX-APIKEY': API_KEY})
    mocker.patch('src.builder.to_query_string_parameters', return_value='KEY=VALUE&KEY1=VALUE1')

    mock_response = Mock(status_code=200)
    mock_response.json.return_value = RESPONSE_OBJ

    mocker.patch('src.builder.requests.get', return_value=mock_response)


def test_builder_default_method_is_get():
    builder = Builder(endpoint='/test', payload={'key': 1})
    assert builder.method == 'GET'


def test_builder_empty_headers():
    builder = Builder(endpoint='/test', payload={'key': 1})
    assert not builder.headers


@pytest.mark.parametrize("values", [None, ''])
def test_builder_endpoint_is_null_or_empty(values):
    with pytest.raises(ValueError, match='endpoint cannot be null or empty'):
        Builder(endpoint=values, payload={})


@pytest.mark.parametrize("values", [None, {}])
def test_builder_payload_is_null_or_empty(values):
    with pytest.raises(ValueError, match='payload cannot be null or empty'):
        Builder(endpoint='/test/', payload=values)


def test_builder_change_method_is_post():
    builder = Builder(endpoint='/test', payload={'key': 1}, method='POST')
    assert builder.method == 'POST'


def test_builder_incorrect_method():
    with pytest.raises(ValueError, match='Http method is invalid'):
        Builder(endpoint='/test', payload={'key': 1}, method='TEST')


def test_set_security_payload_and_headers_ok(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}).set_security()

    assert 'signature' in builder.payload
    assert builder.payload['signature'] == SIGNATURE

    assert 'X-MBX-APIKEY' in builder.headers
    assert builder.headers['X-MBX-APIKEY'] == API_KEY


@pytest.mark.asyncio
async def test_send_http_req_ok(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}).set_security()
    await builder.send_http_req()

    assert builder.response.status_code == 200
    assert builder.response.json() == RESPONSE_OBJ


@pytest.mark.asyncio
async def test_handle_response_200_ok(mocked_deps):
    builder = Builder(endpoint='/test', payload={'key': 1}).set_security()
    await builder.send_http_req()

    builder.handle_response()

    assert not builder.has_error
    assert dict(builder.result)
    assert builder.result['successful'] == True
    assert builder.result['status_code'] == 200
    assert builder.result['results'] == RESPONSE_OBJ
