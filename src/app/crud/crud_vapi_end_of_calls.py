from fastcrud import FastCRUD

from ..models.vapi_end_of_call import VapiEndOfCall
from ..schemas.vapi_end_of_call import (
    VapiEndOfCallCreateInternal,
    VapiEndOfCallDelete,
    VapiEndOfCallUpdate,
    VapiEndOfCallUpdateInternal,
)


CRUDVapiEndOfCall = FastCRUD[
    VapiEndOfCall,
    VapiEndOfCallCreateInternal,
    VapiEndOfCallUpdate,
    VapiEndOfCallUpdateInternal,
    VapiEndOfCallDelete,
]
crud_vapi_end_of_calls = CRUDVapiEndOfCall(VapiEndOfCall)
