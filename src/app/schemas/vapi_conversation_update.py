# ./src/app/schemas/vapi_conversation_update.py
from datetime import datetime
from typing import Literal, Annotated, Any

from pydantic import BaseModel, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class VapiConversationUpdateBase(BaseModel):
    type: Annotated[Literal["conversation-update"], Field(min_length=1, max_length=50)]
    conversation: Annotated[
        list[dict[str, str]],
        Field(examples=[{"role": "assistant", "message": "How can I help?"}]),
    ]
    call: Annotated[
        dict[str, Any],
        Field(
            examples=[
                {"id": "51ac5220-9ae4-46fe-8e90-5fc123706970", "assistantId": None}
            ]
        ),
    ]


class VapiConversationUpdateCreateInternal(BaseModel):
    type: Annotated[Literal["conversation-update"], Field(min_length=1, max_length=50)]
    conversation: Annotated[
        list[dict[str, str]],
        Field(examples=[{"role": "assistant", "message": "How can I help?"}]),
    ]
    id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            examples=["51ac5220-9ae4-46fe-8e90-5fc123706970"],
        ),
    ]
    created_by_user_id: int


class VapiConversationUpdateUpdate(BaseModel):
    conversation: Annotated[
        list[dict[str, str]],
        Field(examples=[{"role": "assistant", "message": "How can I help?"}]),
    ]


class VapiConversationUpdate(
    TimestampSchema,
    VapiConversationUpdateCreateInternal,
    UUIDSchema,
    PersistentDeletion,
):
    pass


class VapiConversationUpdateRead(VapiConversationUpdateCreateInternal):
    created_at: datetime


class VapiConversationUpdateUpdateInternal(VapiConversationUpdateUpdate):
    updated_at: datetime


class VapiConversationUpdateDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime
