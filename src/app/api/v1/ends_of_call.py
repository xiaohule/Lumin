# ./src/app/api/v1/ends_of_call.py
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ...core.utils.cache import cache
from ...crud.crud_ends_of_call import crud_ends_of_call
from ...crud.crud_users import crud_users
from ...schemas.end_of_call import (
    EndOfCallMessage,
    EndOfCallCreate,
    EndOfCallCreateInternal,
    EndOfCallRead,
)
from ...schemas.user import UserRead

router = APIRouter(tags=["ends_of_call"])

# End of Call Report
# When a call ends, the assistant will make a POST request to endpoint post("/{username}/end_of_call with the following body:
# {
#   "message": {
#     "type": "end-of-call-report",
#     "endedReason": "hangup",
#     "call": { Call Object },
#     "recordingUrl": "https://vapi-public.s3.amazonaws.com/recordings/1234.wav",
#     "summary": "The user picked up the phone then asked about the weather...",
#     "transcript": "AI: How can I help? User: What's the weather? ...",
#     "messages":[
#       {
#         "role": "assistant",
#         "message": "How can I help?",
#       },
#       {
#         "role": "user",
#         "message": "What's the weather?"
#       },
#       ...
#     ]
#   }
# }
# endedReason can be any of the options defined on the Call Object.


@router.post("/{username}/end_of_call", response_model=EndOfCallRead, status_code=201)
async def write_end_of_call(
    request: Request,
    username: str,
    message: EndOfCallMessage,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> EndOfCallRead:

    # print("In ends_of_call.py > received message1 is", message.dict())
    print("In ends_of_call.py > received message is", message)

    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=username, is_deleted=False
    )
    if db_user is None:
        raise NotFoundException("User not found")

    if current_user["id"] != db_user["id"]:
        raise ForbiddenException()

    end_of_call_internal_dict = message.message.model_dump()
    # end_of_call_internal_dict.pop('type', None)  # Remove 'type' if it's not needed for the model
    end_of_call_internal_dict["created_by_user_id"] = db_user["id"]

    print(
        "In ends_of_call.py > end_of_call_internal_dict is", end_of_call_internal_dict
    )

    end_of_call_internal = EndOfCallCreateInternal(**end_of_call_internal_dict)
    created_end_of_call: EndOfCallRead = await crud_ends_of_call.create(
        db=db, object=end_of_call_internal
    )

    print("In ends_of_call.py > created_end_of_call is", created_end_of_call)

    return created_end_of_call


@router.get(
    "/{username}/ends_of_call", response_model=PaginatedListResponse[EndOfCallRead]
)
@cache(
    key_prefix="{username}_ends_of_call:page_{page}:items_per_page:{items_per_page}",
    resource_id_name="username",
    expiration=60,
)
async def read_ends_of_call(
    request: Request,
    username: str,
    db: Annotated[AsyncSession, Depends(async_get_db)],
    page: int = 1,
    items_per_page: int = 10,
) -> dict:
    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=username, is_deleted=False
    )
    if not db_user:
        raise NotFoundException("User not found")

    ends_of_call_data = await crud_ends_of_call.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=EndOfCallRead,
        created_by_user_id=db_user["id"],
        is_deleted=False,
    )

    return paginated_response(
        crud_data=ends_of_call_data, page=page, items_per_page=items_per_page
    )


@router.get("/{username}/end_of_call/{id}", response_model=EndOfCallRead)
@cache(key_prefix="{username}_end_of_call_cache", resource_id_name="id")
async def read_end_of_call(
    request: Request,
    username: str,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict:
    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=username, is_deleted=False
    )
    if db_user is None:
        raise NotFoundException("User not found")

    db_end_of_call: EndOfCallRead | None = await crud_ends_of_call.get(
        db=db,
        schema_to_select=EndOfCallRead,
        id=id,
        created_by_user_id=db_user["id"],
        is_deleted=False,
    )
    if db_end_of_call is None:
        raise NotFoundException("EndOfCall not found")

    return db_end_of_call


# @router.patch("/{username}/post/{id}")
# @cache(
#     "{username}_post_cache",
#     resource_id_name="id",
#     pattern_to_invalidate_extra=["{username}_posts:*"],
# )
# async def patch_post(
#     request: Request,
#     username: str,
#     id: int,
#     values: PostUpdate,
#     current_user: Annotated[UserRead, Depends(get_current_user)],
#     db: Annotated[AsyncSession, Depends(async_get_db)],
# ) -> dict[str, str]:
#     db_user = await crud_users.get(
#         db=db, schema_to_select=UserRead, username=username, is_deleted=False
#     )
#     if db_user is None:
#         raise NotFoundException("User not found")

#     if current_user["id"] != db_user["id"]:
#         raise ForbiddenException()

#     db_post = await crud_posts.get(
#         db=db, schema_to_select=PostRead, id=id, is_deleted=False
#     )
#     if db_post is None:
#         raise NotFoundException("Post not found")

#     await crud_posts.update(db=db, object=values, id=id)
#     return {"message": "Post updated"}


@router.delete("/{username}/end_of_call/{id}")
@cache(
    "{username}_end_of_call_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_ends_of_call": "{username}"},
)
async def erase_end_of_call(
    request: Request,
    username: str,
    id: int,
    current_user: Annotated[UserRead, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=username, is_deleted=False
    )
    if db_user is None:
        raise NotFoundException("User not found")

    if current_user["id"] != db_user["id"]:
        raise ForbiddenException()

    db_end_of_call = await crud_ends_of_call.get(
        db=db, schema_to_select=EndOfCallRead, id=id, is_deleted=False
    )
    if db_end_of_call is None:
        raise NotFoundException("EndOfCall not found")

    await crud_ends_of_call.delete(db=db, id=id)

    return {"message": "EndOfCall deleted"}


@router.delete(
    "/{username}/db_end_of_call/{id}", dependencies=[Depends(get_current_superuser)]
)
@cache(
    "{username}_end_of_call_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_ends_of_call": "{username}"},
)
async def erase_db_end_of_call(
    request: Request,
    username: str,
    id: int,
    db: Annotated[AsyncSession, Depends(async_get_db)],
) -> dict[str, str]:
    db_user = await crud_users.get(
        db=db, schema_to_select=UserRead, username=username, is_deleted=False
    )
    if db_user is None:
        raise NotFoundException("User not found")

    db_end_of_call = await crud_ends_of_call.get(
        db=db, schema_to_select=EndOfCallRead, id=id
    )
    if db_end_of_call is None:
        raise NotFoundException("EndOfCall not found")

    await crud_ends_of_call.db_delete(db=db, id=id)
    return {"message": "EndOfCall deleted from the database"}
