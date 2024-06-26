# ./src/app/models/vapi_conversation_update.py
import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON

from ..core.db.database import Base


class VapiConversationUpdate(Base):
    __tablename__ = "vapi_conversation_update"

    id: Mapped[str] = mapped_column(
        "id", String(50), nullable=False, unique=True, primary_key=True
    )
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    type: Mapped[str] = mapped_column(String(50))

    conversation: Mapped[list[dict[str, str]]] = mapped_column(JSON)

    uuid: Mapped[uuid_pkg.UUID] = mapped_column(
        default_factory=uuid_pkg.uuid4, primary_key=True, unique=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default_factory=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    is_deleted: Mapped[bool] = mapped_column(default=False, index=True)
