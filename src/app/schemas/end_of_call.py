# ./src/app/schemas/end_of_call.py
from datetime import datetime
from typing import Annotated, Any

from pydantic import BaseModel, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema


class EndOfCallBase(BaseModel):
    type: Annotated[
        str, Field(min_length=1, max_length=50, examples=["end-of-call-report"])
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
        extra = "ignore"  # replace forbid by ignore if needed


class EndOfCall(TimestampSchema, EndOfCallBase, UUIDSchema, PersistentDeletion):
    created_by_user_id: int


class EndOfCallRead(EndOfCallBase):
    id: int
    created_by_user_id: int
    created_at: datetime


class EndOfCallCreateInternal(EndOfCallBase):
    created_by_user_id: int


class EndOfCallUpdate(EndOfCallBase):
    pass


class EndOfCallUpdateInternal(EndOfCallUpdate):
    updated_at: datetime


class EndOfCallDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime

    class Config:
        extra = "ignore"


class EndOfCallMessage(BaseModel):
    message: Annotated[
        EndOfCallBase,
        Field(
            examples=[
                {
                    "type": "end-of-call-report",
                    "endedReason": "hangup",
                    "call": "{ Call Object }",
                    "phoneNumber": "{ Phone Number Object }",
                    "recordingUrl": "https://vapi-public.s3.amazonaws.com/recordings/1234.wav",
                    "sterioRecordingUrl": "https://vapi-public.s3.amazonaws.com/recordings/1234.wav",
                    "summary": "The user picked up the phone then asked about the weather...",
                    "transcript": "AI: How can I help? User: What's the weather? ...",
                    "messages": [
                        {
                            "role": "assistant",
                            "message": "How can I help?",
                        },
                        {"role": "user", "message": "What's the weather?"},
                    ],
                }
            ]
        ),
    ]
