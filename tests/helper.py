# ./tests/helper.py
from fastapi.testclient import TestClient


def _get_token(username: str, password: str, client: TestClient):
    return client.post(
        "/api/v1/login",
        data={"username": username, "password": password},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )


def _get_vapi_end_of_calls_ids(username: str, client: TestClient, token: dict):
    response = client.get(
        f"/api/v1/{username}/vapi_end_of_calls",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    return [end_of_call["id"] for end_of_call in response.json()["data"]]


def _get_vapi_conversation_updates_ids(username: str, client: TestClient, token: dict):
    response = client.get(
        f"/api/v1/{username}/vapi_conversation_updates",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    return [
        conversation_update["id"] for conversation_update in response.json()["data"]
    ]
