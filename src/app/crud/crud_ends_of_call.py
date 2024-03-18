from fastcrud import FastCRUD

from ..models.end_of_call import EndOfCall
from ..schemas.end_of_call import (
    EndOfCallCreateInternal,
    EndOfCallDelete,
    EndOfCallUpdate,
    EndOfCallUpdateInternal,
)


CRUDEndOfCall = FastCRUD[
    EndOfCall,
    EndOfCallCreateInternal,
    EndOfCallUpdate,
    EndOfCallUpdateInternal,
    EndOfCallDelete,
]
crud_ends_of_call = CRUDEndOfCall(EndOfCall)
