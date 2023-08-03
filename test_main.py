import pytest
from faker import Faker
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

SERVER_URL = "http://127.0.0.1:8000/"
ORDER_API = f"{SERVER_URL}order/"
ACCOUNT_API = f"{SERVER_URL}account/"

TEST_PASSWORD = "test_password"


@pytest.fixture
def account():
    return Faker().first_name()


def test_create_account(account):
    url = ACCOUNT_API

    headers = {'accept': 'application/json', 'Content-Type': 'application/json'}
    data = {"account": account, "email": f"{account}@mail.com", "password": TEST_PASSWORD}

    response = client.post(url, headers=headers, json=data)
    expected_response = {"account": account}

    assert response.status_code == 200, f"Expected 200, but got {response.status_code}"
    assert response.json() == expected_response, f"Expected {expected_response}, but got {response.json()}"


def test_get_account(account):
    test_create_account(account)

    url = f"{ACCOUNT_API}1"
    headers = {'accept': 'application/json'}
    response = client.get(url, headers=headers)

    assert response.status_code == 200, f"Unexpected status code: got {response.status_code}, expected 200"
    assert 'account' in response.json(), "account not in response"


def verify_login(account: str) -> dict:
    test_create_account(account)

    url = f"{SERVER_URL}login"
    headers = {'accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "grant_type": "",
        "username": account,
        "password": TEST_PASSWORD,
        "scope": "",
        "client_id": "",
        "client_secret": ""
    }
    response = client.post(url, headers=headers, data=data)
    response_data = response.json()
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"
    assert 'access_token' in response_data, "access_token not in response"
    assert 'token_type' in response_data, "token_type not in response"
    return response_data


def verify_create_order(account: str, data: dict) -> (dict, int):
    resp = verify_login(account)

    url = ORDER_API
    headers = {'accept': 'application/json', 'Content-Type': 'application/json',
               'Authorization': f"{resp['token_type']} {resp['access_token']}"}
    resp = client.post(url, headers=headers, json=data)
    expected_resp = data
    resp_json = resp.json()
    id = resp_json.get('id')
    resp_json.pop('id', None)
    verify_get_order(headers, id, data)
    assert resp.status_code == 201, f"Expected 201, but got {resp.status_code}"
    assert resp_json == expected_resp, f"Expected {expected_resp}, but got {resp_json}"
    return headers, id


def verify_get_order(headers: dict, id: int, data: dict):
    url = f"{ORDER_API}{id}"
    resp = client.get(url, headers=headers)
    expected_resp = data.copy()
    expected_resp['id'] = id
    assert resp.status_code == 200, f"Expected 200, but got {resp.status_code}"
    assert resp.json() == expected_resp, "Unexpected response: got {}, want {}".format(resp.json(), expected_resp)


@pytest.mark.parametrize("data", [{"order_type": "Sell", "symbol": "EURUSD", "volume": 2000, "price": 0.2}])
def test_get_orders(account, data):
    headers, _ = verify_create_order(account, data)

    url = ORDER_API
    resp = client.get(url, headers=headers)
    resp_json = resp.json()
    resp_lst = [{k: v for k, v in dic.items() if k != 'id'} for dic in resp_json]
    expected_resp = [data]
    assert resp.status_code == 200, f"Expected 200, but got {resp.status_code}"
    assert resp_lst == expected_resp, f"Expected {expected_resp}, but got {resp_lst}"


@pytest.mark.parametrize("data", [{"order_type": "Sell", "symbol": "AUDUSD", "volume": 2020, "price": 0.202}])
def test_update_order(account, data):
    headers, id = verify_create_order(account, data)
    updated_data = {"order_type": "Buy", "symbol": "EURUSD", "volume": 2021, "price": 0.2021}

    url = f"{ORDER_API}{id}"
    resp = client.put(url, headers=headers, json=updated_data)
    verify_get_order(headers, id, updated_data)
    assert resp.status_code == 202, f"Expected 202, but got {resp.status_code}"
    assert resp.text == '"updated"', f"Expected 'updated', but got {resp.text}"


@pytest.mark.parametrize("data", [{"order_type": "Sell", "symbol": "USDJPY", "volume": 2040, "price": 0.204}])
def test_delete_order(account, data):
    headers, id = verify_create_order(account, data)
    verify_get_order(headers, id, data)

    url = f"{ORDER_API}{id}"
    resp = client.delete(url, headers=headers)
    assert resp.status_code == 204, f"Expected 204, but got {resp.status_code}"
