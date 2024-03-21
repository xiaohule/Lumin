# ./src/app/schemas/vapi_end_of_call.py
from datetime import datetime
from typing import Literal, Annotated, Any

from pydantic import BaseModel, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class VapiEndOfCallBase(BaseModel):
    type: Annotated[
        Literal["end-of-call-report"],
        Field(min_length=1, max_length=50),
    ]
    ended_reason: Annotated[
        str,
        Field(min_length=1, max_length=50, alias="endedReason", examples=["hangup"]),
    ]
    transcript: Annotated[
        str, Field(min_length=1, examples=["This is the transcript of the call."])
    ]
    summary: Annotated[
        str,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the summary of the call."],
        ),
    ]
    messages: Annotated[
        list[dict[str, Any]],
        Field(examples=[{"role": "assistant", "message": "How can I help?"}]),
    ]
    call: Annotated[
        dict[str, Any],
        Field(
            examples=[
                {"id": "51ac5220-9ae4-46fe-8e90-5fc123706970", "assistantId": None}
            ]
        ),
    ]
    recording_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            alias="recordingUrl",
            examples=["https://vapi-public.s3.amazonaws.com/recordings/1234.wav"],
            default=None,
        ),
    ]
    stereo_recording_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            alias="stereoRecordingUrl",
            examples=["https://vapi-public.s3.amazonaws.com/recordings/1234.wav"],
            default=None,
        ),
    ]
    call: Annotated[dict[str, Any] | None, Field(examples=[{"call": "Call Object"}])]
    phone_number: Annotated[
        dict[str, Any] | None,
        Field(
            alias="phoneNumber",
            examples=[{"phoneNumber": "Phone Number Object"}],
            default=None,
        ),
    ]

    class Config:
        populate_by_name = True


class VapiEndOfCallCreateInternal(VapiEndOfCallBase):
    call_id: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            examples=["51ac5220-9ae4-46fe-8e90-5fc123706970"],
        ),
    ]
    created_by_user_id: int


class VapiEndOfCallUpdate(VapiEndOfCallCreateInternal):
    pass


class VapiEndOfCall(
    TimestampSchema, VapiEndOfCallCreateInternal, UUIDSchema, PersistentDeletion
):
    pass


class VapiEndOfCallRead(VapiEndOfCallCreateInternal):
    id: int
    created_at: datetime


class VapiEndOfCallUpdateInternal(VapiEndOfCallUpdate):
    updated_at: datetime


class VapiEndOfCallDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime
