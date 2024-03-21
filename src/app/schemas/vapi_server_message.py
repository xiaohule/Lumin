# ./src/app/schemas/vapi_server_message.py
from typing import Annotated, Union

from pydantic import BaseModel, Field

from .vapi_end_of_call import VapiEndOfCallBase, VapiEndOfCallRead
from .vapi_conversation_update import (
    VapiConversationUpdateBase,
    VapiConversationUpdateRead,
    VapiConversationUpdateUpdate,
)


class VapiServerMessage(BaseModel):
    message: Union[VapiEndOfCallBase, VapiConversationUpdateBase] = Field(
        ..., discriminator="type"
    )


VapiServerMessageResponse = Union[
    dict[str, str], VapiConversationUpdateRead, VapiEndOfCallRead
]
