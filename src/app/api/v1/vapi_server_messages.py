# ./src/app/api/v1/vapi_server_messages.py
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

# from ..dependencies import get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import NotFoundException
from ...crud.crud_vapi_end_of_calls import crud_vapi_end_of_calls
from ...crud.crud_vapi_conversation_updates import crud_vapi_conversation_updates
from ...crud.crud_users import crud_users
from ...schemas.vapi_end_of_call import (
    VapiEndOfCallCreateInternal,
    VapiEndOfCallRead,
)
from ...schemas.vapi_conversation_update import (
    VapiConversationUpdateCreateInternal,
    VapiConversationUpdateRead,
)
from ...schemas.vapi_server_message import VapiServerMessage, VapiServerMessageRead
from ...schemas.user import UserRead

router = APIRouter(tags=["vapi_server_messages"])


@router.post(
    "/{username}/vapi_server_message",
    response_model=VapiServerMessageRead,
    status_code=201,
)
async def write_vapi_server_message(
    request: Request,
    username: str,
    message: VapiServerMessage,
    # current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> VapiServerMessageRead:

    print("In vapi_server_message.py > received message is", message)

    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=username, is_deleted=False
    )
    if db_user is None:
        raise NotFoundException("User not found")

    # if current_user["id"] != db_user["id"]:
    #     raise ForbiddenException()

    message_internal_dict = message.message.model_dump()
    message_internal_dict["created_by_user_id"] = db_user["id"]
    message_internal_dict["call_id"] = message_internal_dict["call"]["id"]

    print(
        "In vapi_server_message.py > vapi_server_message_internal_dict is",
        message_internal_dict,
    )

    if message_internal_dict["type"] == "end-of-call-report":
        end_of_call_internal = VapiEndOfCallCreateInternal(**message_internal_dict)
        created_end_of_call: VapiEndOfCallRead = await crud_vapi_end_of_calls.create(
            db=db, object=end_of_call_internal
        )
        print("In vapi_server_message.py > created_end_of_call is", created_end_of_call)
        return created_end_of_call

    elif message_internal_dict["type"] == "conversation-update":
        # relevant_data = {
        #     "type": message_internal_dict["type"],
        #     "conversation": message_internal_dict["conversation"],
        #     "created_by_user_id": message_internal_dict["created_by_user_id"],
        # }

        conversation_update_internal = VapiConversationUpdateCreateInternal(
            **message_internal_dict
        )
        created_conversation_update: VapiConversationUpdateRead = (
            await crud_vapi_conversation_updates.create(
                db=db, object=conversation_update_internal
            )
        )
        print(
            "In vapi_server_message.py > created_conversation_update is",
            created_conversation_update,
        )
        return created_conversation_update
