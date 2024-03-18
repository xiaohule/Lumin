# ./tests/test_end_of_call.py
from fastapi.testclient import TestClient

from src.app.core.config import settings
from src.app.main import app

from .helper import _get_token, _get_end_of_call_ids

test_name = settings.TEST_NAME
test_username = settings.TEST_USERNAME
test_email = settings.TEST_EMAIL
test_password = settings.TEST_PASSWORD

admin_username = settings.ADMIN_USERNAME
admin_password = settings.ADMIN_PASSWORD

client = TestClient(app)


def test_post_user(client: TestClient) -> None:
    response = client.post(
        "/api/v1/user",
        json={
            "name": test_name,
            "username": test_username,
            "email": test_email,
            "password": test_password,
        },
    )
    assert response.status_code == 201


def test_get_user(client: TestClient) -> None:
    response = client.get(f"/api/v1/user/{test_username}")
    print("In test_end_of_call.py, test_get_user, response is", response.json())
    assert response.status_code == 200


def test_get_multiple_users(client: TestClient) -> None:
    response = client.get("/api/v1/users")
    print(
        "In test_end_of_call.py, test_get_multiple_users, response is", response.json()
    )
    assert response.status_code == 200


def test_post_end_of_call(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.post(
        f"/api/v1/{test_username}/end_of_call",
        json={
            "message": {
                "type": "end-of-call-report",
                "endedReason": "hangup",
                "recordingUrl": "https://vapi-public.s3.amazonaws.com/recordings/1234.wav",
                "summary": "The user picked up the phone then asked about the weather.",
                "transcript": "AI: How can I help? User: What the weather?",
                "messages": [
                    {"role": "assistant", "message": "How can I help?"},
                    {"role": "user", "message": "What  the weather?"},
                ],
            }
        },
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_post_end_of_call
    print("In test_end_of_call.py, test_post_end_of_call, response is", response.json())
    assert response.status_code == 201


def test_get_multiple_ends_of_call(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.get(
        f"/api/v1/{test_username}/ends_of_call",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_get_multiple_ends_of_call
    print(
        "In test_end_of_call.py, test_get_multiple_ends_of_call, response is",
        response.json(),
    )
    assert response.status_code == 200


def test_delete_end_of_call(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    end_of_call_ids = _get_end_of_call_ids(
        username=test_username, client=client, token=token
    )

    print(
        "In test_end_of_call.py, test_delete_end_of_call, end_of_call_ids is",
        end_of_call_ids,
    )
    # for each id in end_of_call_ids, delete the end of call
    for end_of_call_id in end_of_call_ids:
        response = client.delete(
            f"/api/v1/{test_username}/end_of_call/{end_of_call_id}",
            headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
        )
        # print the response prefixed by test_delete_end_of_call
        print(
            "In test_end_of_call.py, test_delete_end_of_call, for id",
            end_of_call_id,
            "response is",
            response.json(),
        )
        assert response.status_code == 200


def test_delete_db_end_of_call(client: TestClient) -> None:
    token = _get_token(username=admin_username, password=admin_password, client=client)
    userToken = _get_token(
        username=test_username, password=test_password, client=client
    )
    end_of_call_ids = _get_end_of_call_ids(
        username=test_username, client=client, token=userToken
    )

    print(
        "In test_end_of_call.py, test_delete_db_end_of_call, end_of_call_ids is",
        end_of_call_ids,
    )
    # for each id in end_of_call_ids, delete the end of call
    for end_of_call_id in end_of_call_ids:
        response = client.delete(
            f"/api/v1/{admin_username}/db_end_of_call/{end_of_call_id}",
            headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
        )
        # print the response prefixed by test_delete_db_end_of_call
        print(
            "In test_end_of_call.py, test_delete_db_end_of_call, for id",
            end_of_call_id,
            "response is",
            response.json(),
        )
        assert response.status_code == 200


def test_update_user(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)

    response = client.patch(
        f"/api/v1/user/{test_username}",
        json={"name": f"Updated {test_name}"},
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    assert response.status_code == 200


def test_delete_user(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)

    response = client.delete(
        f"/api/v1/user/{test_username}",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    assert response.status_code == 200


def test_delete_db_user(client: TestClient) -> None:
    token = _get_token(username=admin_username, password=admin_password, client=client)

    response = client.delete(
        f"/api/v1/db_user/{test_username}",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    assert response.status_code == 200
