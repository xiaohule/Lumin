# ./src/app/models/vapi_end_of_call.py
import uuid as uuid_pkg
from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON

from ..core.db.database import Base


class VapiEndOfCall(Base):
    __tablename__ = "vapi_end_of_call"

    id: Mapped[int] = mapped_column(
        "id",
        autoincrement=True,
        nullable=False,
        unique=True,
        primary_key=True,
        init=False,
    )
    created_by_user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)

    type: Mapped[str] = mapped_column(String(50))
    call_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    ended_reason: Mapped[str] = mapped_column(String(50))
    call: Mapped[list[dict[str, str]]] = mapped_column(JSON)
    phone_number: Mapped[list[dict[str, str]]] = mapped_column(JSON)
    summary: Mapped[str] = mapped_column(String(63206))
    transcript: Mapped[str] = mapped_column(String)
    messages: Mapped[list[dict[str, str]]] = mapped_column(
        JSON
    )  # is String(63206) in the current DB schema
    recording_url: Mapped[str | None] = mapped_column(String, default=None)
    stereo_recording_url: Mapped[str | None] = mapped_column(String, default=None)

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
