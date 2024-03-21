from fastcrud import FastCRUD

from ..models.vapi_conversation_update import VapiConversationUpdate
from ..schemas.vapi_conversation_update import (
    VapiConversationUpdateCreateInternal,
    VapiConversationUpdateDelete,
    VapiConversationUpdateUpdate,
    VapiConversationUpdateUpdateInternal,
)


CRUDVapiConversationUpdate = FastCRUD[
    VapiConversationUpdate,
    VapiConversationUpdateCreateInternal,
    VapiConversationUpdateUpdate,
    VapiConversationUpdateUpdateInternal,
    VapiConversationUpdateDelete,
]
crud_vapi_conversation_updates = CRUDVapiConversationUpdate(VapiConversationUpdate)
