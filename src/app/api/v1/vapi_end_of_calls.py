# ./src/app/api/v1/vapi_server_messages.py
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ...core.utils.cache import cache
from ...crud.crud_vapi_end_of_calls import crud_vapi_end_of_calls
from ...crud.crud_users import crud_users
from ...schemas.vapi_end_of_call import (
    VapiEndOfCallRead,
)
from ...schemas.user import UserRead

router = APIRouter(tags=["vapi_end_of_calls"])


@router.get(
    "/{username}/vapi_end_of_calls",
    response_model=PaginatedListResponse[VapiEndOfCallRead],
)
@cache(
    key_prefix="{username}_vapi_end_of_calls:page_{page}:items_per_page:{items_per_page}",
    resource_id_name="username",
    expiration=60,
)
async def read_end_of_calls(
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

    end_of_calls_data = await crud_vapi_end_of_calls.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=VapiEndOfCallRead,
        created_by_user_id=db_user["id"],
        is_deleted=False,
    )

    return paginated_response(
        crud_data=end_of_calls_data, page=page, items_per_page=items_per_page
    )


@router.get("/{username}/vapi_end_of_call/{id}", response_model=VapiEndOfCallRead)
@cache(key_prefix="{username}_vapi_end_of_call_cache", resource_id_name="id")
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

    db_end_of_call: VapiEndOfCallRead | None = await crud_vapi_end_of_calls.get(
        db=db,
        schema_to_select=VapiEndOfCallRead,
        id=id,
        created_by_user_id=db_user["id"],
        is_deleted=False,
    )
    if db_end_of_call is None:
        raise NotFoundException("VapiEndOfCall not found")

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


@router.delete("/{username}/vapi_end_of_call/{id}")
@cache(
    "{username}_vapi_end_of_call_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_vapi_end_of_calls": "{username}"},
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

    db_end_of_call = await crud_vapi_end_of_calls.get(
        db=db, schema_to_select=VapiEndOfCallRead, id=id, is_deleted=False
    )
    if db_end_of_call is None:
        raise NotFoundException("VapiEndOfCall not found")

    await crud_vapi_end_of_calls.delete(db=db, id=id)

    return {"message": "VapiEndOfCall deleted"}


@router.delete(
    "/{username}/db_vapi_end_of_call/{id}",
    dependencies=[Depends(get_current_superuser)],
)
@cache(
    "{username}_vapi_end_of_call_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_vapi_end_of_calls": "{username}"},
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

    db_end_of_call = await crud_vapi_end_of_calls.get(
        db=db, schema_to_select=VapiEndOfCallRead, id=id
    )
    if db_end_of_call is None:
        raise NotFoundException("VapiEndOfCall not found")

    await crud_vapi_end_of_calls.db_delete(db=db, id=id)
    return {"message": "VapiEndOfCall deleted from the database"}
