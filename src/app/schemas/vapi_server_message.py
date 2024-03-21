# ./src/app/schemas/vapi_server_message.py
from typing import Annotated, Union

from pydantic import BaseModel, Field

from .vapi_end_of_call import VapiEndOfCallBase, VapiEndOfCallRead
from .vapi_conversation_update import (
    VapiConversationUpdateBase,
    VapiConversationUpdateRead,
)


class VapiServerMessage(BaseModel):
    message: Union[VapiEndOfCallBase, VapiConversationUpdateBase] = Field(
        ..., discriminator="type"
    )


VapiServerMessageRead = Union[VapiEndOfCallRead, VapiConversationUpdateRead]
