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
                    "id": "8248e704-2a50-40d2-b3a2-bd1d52a73847",
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
    print("In test_end_of_call.py, test_post_end_of_call, response is", response.json())
    assert response.status_code == 201


def test_post_end_of_call_2(client: TestClient) -> None:
    token = _get_token(username=test_username, password=test_password, client=client)
    response = client.post(
        f"/api/v1/{test_username}/end_of_call",
        json={
            "message": {
                "type": "end-of-call-report",
                "endedReason": "customer-ended-call",
                "transcript": "AI: Bienvenue aux assurances de la Caisse d'Epargne et des Banques Associées. Je me présente, suis Léo,\nUser: Bonjour les vôtres, j'ai acheté une Citroën c deux il n'y a pas longtemps. Et un particulier,\nAI: Bonjour,\nUser: Et là j'ai un petit problème c'est que en fait la la la la Citroën est en panne et personne ne me répond pas donc je voulais savoir comment procéder.\nAI: Je suis désolé d'apprendre que votre Citroën est en panne. Ne vous inquiétez pas, Voici les étapes à suivre pour gérer cette situation. Tout d'abord, assurez-vous d'être en sécurité et mettez votre véhicule hors de la circulation si possible. Deux, ensuite, vérifiez si vous avez une assistance dépannage incluse dans votre contrat d'assurance.",
                "summary": "In the conversation, the User explains to the AI, which represents a customer service chat of a bank's insurance division, that they recently bought a Citroën C2 that is now broken down. The User seems to be seeking assistance with their vehicle. The AI advises the User to ensure their safety, and to check if they have assistance included in their insurance policy. When the User expresses interest in using the legal protection service, the AI outlines the steps to resolve the issue with the seller, including contacting the seller, sending a formal demand letter, seeking help from a mediator, and potentially taking the matter to court. The User thanks the AI for the advice and ends the call.",
                "messages": [
                    {
                        "role": "system",
                        "message": "Bonjour, Léo ! Vous êtes la voix amicale et serviable des assurances de la caisse d'épargne et des banques associées, ici pour aider des clients dans le cadre de la gestion de leur sinistre. Vous êtes leur gestionnaire de sinistre. Votre tâche principale est de fournir un soutien par le biais d'interactions audio, répondant aux questions, résolvant les problèmes, offrant des conseils et faisant des recommandations de produits. Rappelez-vous, les clients ne peuvent pas vous voir, donc vos mots doivent peindre l'image de manière claire et chaleureuse.\nLors des interactions, écoutez attentivement les indices sur l'humeur du client et le contexte de leurs questions. Si un client demande si vous l'écoutez, rassurez-le avec une reconnaissance rapide et amicale. Pour les requêtes complexes nécessitant des explications détaillées, décomposez vos réponses en étapes simples et faciles à suivre. Votre objectif est de faire en sorte que chaque client se sente écouté, soutenu et satisfait du service.\n\n",
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
                    {
                        "role": "bot",
                        "message": "Je suis désolé d'apprendre que votre Citroën est en panne. Ne vous inquiétez pas, Voici les étapes à suivre pour gérer cette situation. Tout d'abord, assurez-vous d'être en sécurité et mettez votre véhicule hors de la circulation si possible. Deux, ensuite, vérifiez si vous avez une assistance dépannage incluse dans votre contrat d'assurance.",
                        "time": 1710844204666.001,
                        "endTime": 1710844223586,
                        "secondsFromStart": 29.550001,
                    },
                    {
                        "role": "user",
                        "message": "Attendez excusez-moi elle n'est pas je ne suis pas arrêté sur la voie enfin mon mon véhicule il est garé en moi, mais il ne fonctionne plus. Alors que j'attendais quand même vu que je viens de l'acheter qui fonctionne un peu plus qu'une semaine quoi.",
                        "time": 1710844224716,
                        "endTime": 1710844239096,
                        "secondsFromStart": 49.6,
                    },
                    {
                        "role": "bot",
                        "message": "Je comprends votre frustration, vraiment décevant d'avoir des problèmes avec une voiture récemment achetée. Pour votre situation, serait préférable de contacter le vendeur ou le concessionnaire où vous avez acheté la voiture. Car il pourrait être en mesure de vous aider ou de vous fournir une solution, surtout si la voiture est toujours sous garantie. Cependant, vous avez souscrit une assurance auto avec nous qui comprend une assistance dépannage, Nous pouvons également vous aider. Pouvez-vous me confirmer si c'est le cas,",
                        "time": 1710844241636,
                        "endTime": 1710844265886,
                        "secondsFromStart": 66.52,
                    },
                    {
                        "role": "user",
                        "message": "Non moi je voulais vraiment avoir votre service de protection juridique. Donc vous m'expliquiez un petit peu je dois faire maintenant, est-ce que je dois envoyer un recommandé, est-ce que je dois rencontrer le conciliateur de justice, que je dois faire des poursuites judiciaires",
                        "time": 1710844268625.995,
                        "endTime": 1710844282756,
                        "secondsFromStart": 93.509995,
                    },
                    {
                        "role": "bot",
                        "message": "Je comprends que vous bénéficiez de notre service de protection juridique. Voici les étapes à suivre pour résoudre ce problème avec le vendeur. Un. Contactez d'abord le vendeur pour lui expliquer la situation et demander une solution à l'amiable. Gardez une trace de toutes les communications avec le vendeur. Deux, si le vendeur ne répond pas ou refuse de résoudre le problème, pouvez envoyer une lettre de mise en demeure par courrier recommandé avec accusé de réception. Cette lettre doit décrire le problème, les solutions demandées et un délai raisonnable pour résoudre le problème. Trois, si le vendeur ne répond toujours pas ou ne résout pas le problème dans le délai imparti. Vous pouvez faire appel à un conciliateur de justice. Le conciliateur tentera de trouver une solution à l'amiable entre vous et le vendeur. Quatre Si aucune solution n'est trouvée après la conciliation, pouvez envisager de saisir le tribunal compétent pour engager une procédure judiciaire.",
                        "time": 1710844286806,
                        "endTime": 1710844332926,
                        "secondsFromStart": 111.69,
                    },
                    {
                        "role": "user",
                        "message": "Ouais. Ok bon merci beaucoup pour ces informations et au revoir.",
                        "time": 1710844336366,
                        "endTime": 1710844340076,
                        "secondsFromStart": 161.25,
                    },
                    {
                        "role": "function_call",
                        "name": "endCall",
                        "args": "{}",
                        "time": 1710844340807,
                        "secondsFromStart": 163.765,
                        "message": "",
                    },
                ],
                "recordingUrl": "https://auth.vapi.ai/storage/v1/object/public/recordings/1710844344292-51fb580d-7cb5-404c-abb3-9bf41bb69fee.wav",
                "stereoRecordingUrl": "https://auth.vapi.ai/storage/v1/object/public/recordings/1710844344297-c06e51e6-ae5a-4f9f-9281-a01ec7e820c5.wav",
                "call": {
                    "id": "4bd29b07-b248-4df3-b9db-29dc821e3910",
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
        "In test_end_of_call.py, test_post_end_of_call_2, response is", response.json()
    )
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
