# ./src/app/api/v1/vapi_server_messages.py
from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request
from fastcrud.paginated import PaginatedListResponse, compute_offset, paginated_response
from sqlalchemy.ext.asyncio import AsyncSession

from ..dependencies import get_current_superuser, get_current_user
from ...core.db.database import async_get_db
from ...core.exceptions.http_exceptions import ForbiddenException, NotFoundException
from ...core.utils.cache import cache
from ...crud.crud_vapi_conversation_updates import crud_vapi_conversation_updates
from ...crud.crud_users import crud_users
from ...schemas.vapi_conversation_update import (
    VapiConversationUpdateRead,
)
from ...schemas.user import UserRead

router = APIRouter(tags=["vapi_conversation_updates"])


@router.get(
    "/{username}/vapi_conversation_updates",
    response_model=PaginatedListResponse[VapiConversationUpdateRead],
)
@cache(
    key_prefix="{username}_vapi_conversation_updates:page_{page}:items_per_page:{items_per_page}",
    resource_id_name="username",
    expiration=60,
)
async def read_conversation_updates(
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

    conversation_updates_data = await crud_vapi_conversation_updates.get_multi(
        db=db,
        offset=compute_offset(page, items_per_page),
        limit=items_per_page,
        schema_to_select=VapiConversationUpdateRead,
        created_by_user_id=db_user["id"],
        is_deleted=False,
    )

    return paginated_response(
        crud_data=conversation_updates_data, page=page, items_per_page=items_per_page
    )


@router.get(
    "/{username}/vapi_conversation_update/{id}",
    response_model=VapiConversationUpdateRead,
)
@cache(key_prefix="{username}_vapi_conversation_update_cache", resource_id_name="id")
async def read_conversation_update(
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

    db_conversation_update: VapiConversationUpdateRead | None = (
        await crud_vapi_conversation_updates.get(
            db=db,
            schema_to_select=VapiConversationUpdateRead,
            id=id,
            created_by_user_id=db_user["id"],
            is_deleted=False,
        )
    )
    if db_conversation_update is None:
        raise NotFoundException("VapiConversationUpdate not found")

    return db_conversation_update


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


@router.delete("/{username}/vapi_conversation_update/{id}")
@cache(
    "{username}_vapi_conversation_update_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_vapi_conversation_updates": "{username}"},
)
async def erase_conversation_update(
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

    db_conversation_update = await crud_vapi_conversation_updates.get(
        db=db, schema_to_select=VapiConversationUpdateRead, id=id, is_deleted=False
    )
    if db_conversation_update is None:
        raise NotFoundException("VapiConversationUpdate not found")

    await crud_vapi_conversation_updates.delete(db=db, id=id)

    return {"message": "VapiConversationUpdate deleted"}


@router.delete(
    "/{username}/db_vapi_conversation_update/{id}",
    dependencies=[Depends(get_current_superuser)],
)
@cache(
    "{username}_vapi_conversation_update_cache",
    resource_id_name="id",
    to_invalidate_extra={"{username}_vapi_conversation_updates": "{username}"},
)
async def erase_db_conversation_update(
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

    db_conversation_update = await crud_vapi_conversation_updates.get(
        db=db, schema_to_select=VapiConversationUpdateRead, id=id
    )
    if db_conversation_update is None:
        raise NotFoundException("VapiConversationUpdate not found")

    await crud_vapi_conversation_updates.db_delete(db=db, id=id)
    return {"message": "VapiConversationUpdate deleted from the database"}
