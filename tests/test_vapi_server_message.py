# ./tests/test_vapi_server_message.py
from fastapi.testclient import TestClient

from src.app.core.config import settings
from src.app.main import app

from .helper import (
    _get_token,
    _get_vapi_end_of_calls_ids,
    _get_vapi_conversation_updates_ids,
)

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
    print("In test_vapi_server_message.py, test_get_user, response is", response.json())
    assert response.status_code == 200


def test_get_multiple_users(client: TestClient) -> None:
    response = client.get("/api/v1/users")
    print(
        "In test_vapi_server_message.py, test_get_multiple_users, response is",
        response.json(),
    )
    assert response.status_code == 200


def test_post_vapi_end_of_call(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.post(
        f"/api/v1/{test_username}/vapi_server_message",
        json={
            "message": {
                "type": "end-of-call-report",
                "endedReason": "customer-ended-call",
                "transcript": "AI: Bienvenue aux assurances de la Caisse d'Epargne des Banques Associées. Je me présente, Je suis Léo,\nUser: Bonjour Léo, le mal engin un kebab.\nAI: Oui, je suis là et j'écoute attentivement.\n",
                "summary": "The conversation is between a user and an AI named Léo, who represents the insurance services of the Caisse d'Epargne des Banques Associées. ",
                "messages": [
                    {
                        "role": "system",
                        "message": "Bonjour, Léo ! Vous êtes la voix amicale et serviable des assurances de la caisse d'épargne et des banques associées",
                        "time": 1710830749876,
                        "secondsFromStart": 0,
                    },
                    {
                        "role": "bot",
                        "message": "Bienvenue aux assurances de la Caisse d'Epargne des Banques Associées. Je me présente, Je suis Léo,",
                        "time": 1710830751773,
                        "endTime": 1710830756923,
                        "secondsFromStart": 1.8399999,
                    },
                    {
                        "role": "user",
                        "message": "Bonjour Léo, le mal engin un kebab.",
                        "time": 1710830760353,
                        "endTime": 1710830761973.001,
                        "secondsFromStart": 10.42,
                    },
                    {
                        "role": "bot",
                        "message": "Oui, je suis là et j'écoute attentivement.",
                        "time": 1710830764623.001,
                        "endTime": 1710830766723,
                        "secondsFromStart": 14.690001,
                    },
                ],
                "recordingUrl": "https://auth.vapi.ai/storage/v1/object/public/recordings/1710830770068-910a9cd0-c2ec-4789-9dd5-ab03dad1ddc4.wav",
                "stereoRecordingUrl": "https://auth.vapi.ai/storage/v1/object/public/recordings/1710830770071-7a730b84-d082-46e0-afcf-c7eba6a8e4b8.wav",
                "call": {
                    "id": "51ac5220-9ae4-46fe-8e90-5fc123706970",
                    "assistantId": "0eff0e2a-e7ba-4fac-b867-3e40f657f6e9",
                },
                "unknownDict": {"dummy": "1234567890"},
                "unknownList": ["dummy", "1234567890"],
                "unknownString": "dummy",
            }
        },
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_post_end_of_call
    print(
        "In test_vapi_server_message.py, test_post_end_of_call, response is",
        response.json(),
    )
    assert response.status_code == 201


def test_post_vapi_end_of_call_2(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.post(
        f"/api/v1/{test_username}/vapi_server_message",
        json={
            "message": {
                "type": "end-of-call-report",
                "endedReason": "customer-ended-call",
                "transcript": "AI: Bienvenue aux assurances de la Caisse d'Epargne et des Banques Associées...",
                "summary": "In the conversation, the User explains to the AI...",
                "messages": [
                    {
                        "role": "system",
                        "message": "Bonjour, Léo !...",
                        "time": 1710844175066,
                        "secondsFromStart": 0,
                    },
                    {
                        "role": "bot",
                        "message": "Bienvenue aux assurances de la Caisse d'Epargne et des Banques Associées. Je me présente, suis Léo,",
                        "time": 1710844176876,
                        "endTime": 1710844182066,
                        "secondsFromStart": 1.76,
                    },
                    {
                        "role": "user",
                        "message": "Bonjour les vôtres, j'ai acheté une Citroën c deux il n'y a pas longtemps. Et un particulier,",
                        "time": 1710844185136,
                        "endTime": 1710844191246.001,
                        "secondsFromStart": 10.02,
                    },
                    {
                        "role": "bot",
                        "message": "Bonjour,",
                        "time": 1710844190406,
                        "endTime": 1710844190906,
                        "secondsFromStart": 15.29,
                    },
                    {
                        "role": "user",
                        "message": "Et là j'ai un petit problème c'est que en fait la la la la Citroën est en panne et personne ne me répond pas donc je voulais savoir comment procéder.",
                        "time": 1710844193456,
                        "endTime": 1710844201735.999,
                        "secondsFromStart": 18.34,
                    },
                ],
                "recordingUrl": "https://auth.vapi.ai/storage/v1/object/public/recordings/1710844344292-51fb580d-7cb5-404c-abb3-9bf41bb69fee.wav",
                "stereoRecordingUrl": "https://auth.vapi.ai/storage/v1/object/public/recordings/1710844344297-c06e51e6-ae5a-4f9f-9281-a01ec7e820c5.wav",
                "call": {
                    "id": "98ut5220-9ae4-46fe-8e90-5fc1238790",
                    "assistantId": "0eff0e2a-e7ba-4fac-b867-3e40f657f6e9",
                    "customerId": None,
                    "phoneNumberId": "7cfcdb17-e2ab-4eaf-b7ef-2630fae1c17c",
                    "type": "inboundPhoneCall",
                    "startedAt": None,
                    "endedAt": None,
                    "transcript": None,
                    "recordingUrl": None,
                    "summary": None,
                    "createdAt": "2024-03-19T10:29:34.426Z",
                    "updatedAt": "2024-03-19T10:29:34.426Z",
                    "orgId": "e126b212-5073-46eb-bed1-295d0aef12da",
                    "cost": 0,
                    "twilioCallSid": None,
                    "twilioCallStatus": None,
                    "webCallUrl": None,
                    "assistant": None,
                    "phoneNumber": None,
                    "customer": {"number": "+33768482846"},
                    "status": "ringing",
                    "endedReason": None,
                    "messages": None,
                    "maxDurationSeconds": None,
                    "stereoRecordingUrl": None,
                    "costBreakdown": None,
                    "metadata": None,
                    "phoneCallProvider": "twilio",
                    "phoneCallProviderId": "CA4a519f23ad362c959d16e4db82e96f78",
                    "webCallSipUri": None,
                    "forwardedPhoneNumber": None,
                    "phoneCallTransport": "pstn",
                    "phoneCallProviderBypassEnabled": None,
                    "phoneCallProviderDetails": None,
                },
                "phoneNumber": {
                    "id": "7cfcdb17-e2ab-4eaf-b7ef-2630fae1c17c",
                    "orgId": "e126b212-5073-46eb-bed1-295d0aef12da",
                    "assistantId": "0eff0e2a-e7ba-4fac-b867-3e40f657f6e9",
                    "number": "+17065842942",
                    "createdAt": "2024-03-19T10:10:44.279Z",
                    "updatedAt": "2024-03-19T10:10:55.771Z",
                    "stripeSubscriptionId": None,
                    "twilioAccountSid": "AC7cacf65bbb6f2ff210b2dd2f2c7ec7e7",
                    "twilioAuthToken": "50e3a7fb88b27a160f019a37a96f4787",
                    "stripeSubscriptionStatus": None,
                    "stripeSubscriptionCurrentPeriodStart": None,
                    "name": "1st US number",
                    "credentialId": None,
                    "serverUrl": None,
                    "serverUrlSecret": None,
                },
            }
        },
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_post_end_of_call_2
    print(
        "In test_vapi_server_message.py, test_post_end_of_call_2, response is",
        response.json(),
    )
    assert response.status_code == 201


def test_post_vapi_conversation_update(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.post(
        f"/api/v1/{test_username}/vapi_server_message",
        json={
            "message": {
                "type": "conversation-update",
                "conversation": [
                    {
                        "role": "assistant",
                        "content": "Bienvenue aux assurances de la Caisse d'Epargne des Banques Associées. Je me présente, suis Léo, puis-je vous aider",
                    },
                    {"role": "user", "content": "Bonjour Léo, je suis copain Vertou,"},
                    {
                        "role": "assistant",
                        "content": "Bonjour, suis ravi de vous assister. Pourriez-vous me donner votre nom complet S'il vous plaît,",
                    },
                    {
                        "role": "user",
                        "content": "Oui, oui mon prénom c'est coquin et mon nom de famille c'est Vertu v e r t o u.",
                    },
                ],
                "call": {
                    "id": "51ac5220-9ae4-46fe-8e90-5fc123706970",
                    "assistantId": None,
                    "customerId": None,
                    "phoneNumberId": None,
                    "type": "webCall",
                    "updatedAt": "2024-03-20T17:26:19.582Z",
                    "orgId": "e126b212-5073-46eb-bed1-295d0aef12da",
                    "cost": 0,
                    "twilioCallSid": None,
                    "twilioCallStatus": None,
                    "webCallUrl": "https://vapi.daily.co/giUL1FGoyFlBRa5FpHlw",
                    "assistant": {
                        "name": "Leo",
                        "model": {
                            "model": "gpt-4",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "Salut Léo ! En tant que juriste de notre service d'information juridique à la Caisse d'Épargne et des Banques Associées...",
                                }
                            ],
                            "provider": "openai",
                            "functions": [],
                            "maxTokens": 250,
                            "temperature": 0,
                        },
                    },
                    "phoneNumber": None,
                    "phoneCallProviderDetails": None,
                },
                "unknownDict": {"dummy": "1234567890"},
                "unknownList": ["dummy", "1234567890"],
                "unknownString": "dummy",
            }
        },
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_post_end_of_call
    print(
        "In test_vapi_server_message.py, test_post_vapi_conversation_update, response is",
        response.json(),
    )
    assert response.status_code == 201


def test_post_vapi_conversation_update_2(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.post(
        f"/api/v1/{test_username}/vapi_server_message",
        json={
            "message": {
                "type": "conversation-update",
                "conversation": [
                    {
                        "role": "assistant",
                        "content": "Bienvenue aux assurances de la Caisse d'Epargne des Banques Associées. Je me présente, suis Léo, puis-je vous aider",
                    },
                    {"role": "user", "content": "Bonjour Léo, je suis copain Vertou,"},
                    {
                        "role": "assistant",
                        "content": "Bonjour, suis ravi de vous assister. Pourriez-vous me donner votre nom complet S'il vous plaît,",
                    },
                    {
                        "role": "user",
                        "content": "Oui, oui mon prénom c'est coquin et mon nom de famille c'est Vertu v e r t o u.",
                    },
                    {
                        "role": "assistant",
                        "content": "Merci beaucoup Coquin Vertou. Comment puis-je vous aider aujourd'hui,",
                    },
                ],
                "call": {
                    "id": "51ac5220-9ae4-46fe-8e90-5fc123706970",
                    "assistantId": None,
                    "customerId": None,
                    "phoneNumberId": None,
                    "type": "webCall",
                    "updatedAt": "2024-03-20T17:26:19.582Z",
                    "orgId": "e126b212-5073-46eb-bed1-295d0aef12da",
                    "cost": 0,
                    "twilioCallSid": None,
                    "twilioCallStatus": None,
                    "webCallUrl": "https://vapi.daily.co/giUL1FGoyFlBRa5FpHlw",
                    "assistant": {
                        "name": "Leo",
                        "model": {
                            "model": "gpt-4",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "Salut Léo ! En tant que juriste de notre service d'information juridique à la Caisse d'Épargne et des Banques Associées...",
                                }
                            ],
                            "provider": "openai",
                            "functions": [],
                            "maxTokens": 250,
                            "temperature": 0,
                        },
                    },
                    "phoneNumber": None,
                    "phoneCallProviderDetails": None,
                },
            }
        },
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_post_end_of_call
    print(
        "In test_vapi_server_message.py, test_post_vapi_conversation_update_2, response is",
        response.json(),
    )
    assert response.status_code == 201


def test_get_multiple_conversation_updates(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.get(
        f"/api/v1/{test_username}/vapi_conversation_updates",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_get_multiple_end_of_calls
    print(
        "In test_vapi_server_message.py, test_get_multiple_conversation_updates, response is",
        response.json(),
    )
    assert response.status_code == 200


def test_delete_conversation_updates(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    conversation_updates_ids = _get_vapi_conversation_updates_ids(
        username=test_username, client=client, token=token
    )

    print(
        "In test_vapi_server_message.py, test_delete_conversation_updates, conversation_updates_ids is",
        conversation_updates_ids,
    )
    # for each id in end_of_call_ids, delete the end of call
    for conversation_update_id in conversation_updates_ids:
        response = client.delete(
            f"/api/v1/{test_username}/vapi_conversation_update/{conversation_update_id}",
            headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
        )
        # print the response prefixed by test_delete_end_of_call
        print(
            "In test_vapi_server_message.py, test_delete_conversation_updates, for id",
            conversation_update_id,
            "response is",
            response.json(),
        )
        assert response.status_code == 200


def test_delete_db_conversation_updates_ids(client: TestClient) -> None:
    token = _get_token(username=admin_username, password=admin_password, client=client)
    userToken = _get_token(
        username=test_username, password=test_password, client=client
    )
    conversation_updates_ids = _get_vapi_conversation_updates_ids(
        username=test_username, client=client, token=userToken
    )

    print(
        "In test_vapi_server_message.py, test_delete_db_conversation_updates_ids, conversation_updates_ids is",
        conversation_updates_ids,
    )
    # for each id in end_of_call_ids, delete the end of call
    for conversation_update_id in conversation_updates_ids:
        response = client.delete(
            f"/api/v1/{admin_username}/db_vapi_conversation_update/{conversation_update_id}",
            headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
        )
        # print the response prefixed by test_delete_db_end_of_call
        print(
            "In test_vapi_server_message.py, test_delete_db_conversation_updates_ids, for id",
            conversation_update_id,
            "response is",
            response.json(),
        )
        assert response.status_code == 200


def test_get_multiple_end_of_calls(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.get(
        f"/api/v1/{test_username}/vapi_end_of_calls",
        headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
    )
    # print the response prefixed by test_get_multiple_end_of_calls
    print(
        "In test_vapi_server_message.py, test_get_multiple_end_of_calls, response is",
        response.json(),
    )
    assert response.status_code == 200


def test_delete_end_of_calls(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    end_of_calls_ids = _get_vapi_end_of_calls_ids(
        username=test_username, client=client, token=token
    )

    print(
        "In test_vapi_server_message.py, test_delete_end_of_calls, end_of_calls_ids is",
        end_of_calls_ids,
    )
    # for each id in end_of_call_ids, delete the end of call
    for end_of_call_id in end_of_calls_ids:
        response = client.delete(
            f"/api/v1/{test_username}/vapi_end_of_call/{end_of_call_id}",
            headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
        )
        # print the response prefixed by test_delete_end_of_call
        print(
            "In test_vapi_server_message.py, test_delete_end_of_calls, for id",
            end_of_call_id,
            "response is",
            response.json(),
        )
        assert response.status_code == 200


def test_delete_db_end_of_calls(client: TestClient) -> None:
    token = _get_token(username=admin_username, password=admin_password, client=client)
    userToken = _get_token(
        username=test_username, password=test_password, client=client
    )
    end_of_calls_ids = _get_vapi_end_of_calls_ids(
        username=test_username, client=client, token=userToken
    )

    print(
        "In test_vapi_server_message.py, test_delete_db_end_of_call, end_of_call_ids is",
        end_of_calls_ids,
    )
    # for each id in end_of_call_ids, delete the end of call
    for end_of_call_id in end_of_calls_ids:
        response = client.delete(
            f"/api/v1/{admin_username}/db_vapi_end_of_call/{end_of_call_id}",
            headers={"Authorization": f'Bearer {token.json()["access_token"]}'},
        )
        # print the response prefixed by test_delete_db_end_of_call
        print(
            "In test_vapi_server_message.py, test_delete_db_end_of_calls, for id",
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
