import requests
import pytest

def mock_get(url, params=None, **kwargs):
    if params == {"username": "admin", "password": "admin"}:
        class MockResponse:
            status_code = 401
            text = ""
        return MockResponse()
    elif params == {"username": "admin", "password": "qwerty"}:
        class MockResponse:
            status_code = 201
            text = ""
        return MockResponse()
    else:
        class MockResponse:
            status_code = 400
            text = "Invalid request"
        return MockResponse()

def test_unauthorized_access(mocker):
    mocker.patch('requests.get', side_effect=mock_get)
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "admin"}
    
    response = requests.get(url, params=params)
    
    assert response.status_code == 401, f"Expected 401, but got {response.status_code}"
    assert isinstance(response.text, str), "Expected a text response"

def test_authorized_access(mocker):
    mocker.patch('requests.get', side_effect=mock_get)
    url = "http://127.0.0.1:8000/users"
    params = {"username": "admin", "password": "qwerty"}
    
    response = requests.get(url, params=params)
    
    assert response.status_code == 201, f"Expected 201, but got {response.status_code}"
    assert isinstance(response.text, str), "Expected a text response"

if __name__ == "__main__":
    pytest.main(["-v", __file__])
