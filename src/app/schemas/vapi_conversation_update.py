# ./src/app/schemas/vapi_conversation_update.py
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class VapiConversationUpdateBase(BaseModel):
    type: Annotated[
        str, Field(min_length=1, max_length=50, examples=["conversation-update"])
    ]
    conversation: Annotated[
        list[dict[str, str]],
        Field(examples=[{"role": "assistant", "message": "How can I help?"}]),
    ]
    call_id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            examples=["51ac5220-9ae4-46fe-8e90-5fc123706970"],
        ),
    ]


class VapiConversationUpdate(
    TimestampSchema, VapiConversationUpdateBase, UUIDSchema, PersistentDeletion
):
    created_by_user_id: int


class VapiConversationUpdateRead(VapiConversationUpdateBase):
    id: int
    created_by_user_id: int
    created_at: datetime


class VapiConversationUpdateCreateInternal(VapiConversationUpdateBase):
    created_by_user_id: int


class VapiConversationUpdateUpdate(VapiConversationUpdateBase):
    pass


class VapiConversationUpdateUpdateInternal(VapiConversationUpdateUpdate):
    updated_at: datetime


class VapiConversationUpdateDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime
