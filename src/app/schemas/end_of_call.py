# ./src/app/schemas/end_of_call.py
from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from ..core.schemas import PersistentDeletion, TimestampSchema, UUIDSchema

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


class EndOfCallBase(BaseModel):
    type: Annotated[
        str, Field(min_length=1, max_length=50, examples=["end-of-call-report"])
    ]
    ended_reason: Annotated[
        str,
        Field(min_length=1, max_length=50, alias="endedReason", examples=["hangup"]),
    ]
    summary: Annotated[
        str,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the summary of the call."],
        ),
    ]
    transcript: Annotated[
        str, Field(min_length=1, examples=["This is the transcript of the call."])
    ]
    messages: Annotated[
        list[dict[str, str]],
        Field(examples=[{"role": "assistant", "message": "How can I help?"}]),
    ]

    class Config:
        populate_by_name = True


class EndOfCall(TimestampSchema, EndOfCallBase, UUIDSchema, PersistentDeletion):
    recording_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            alias="recordingUrl",
            examples=["https://vapi-public.s3.amazonaws.com/recordings/1234.wav"],
            default=None,
        ),
    ]
    created_by_user_id: int

    class Config:
        populate_by_name = True


class EndOfCallRead(BaseModel):
    id: int
    type: Annotated[
        str, Field(min_length=1, max_length=50, examples=["end-of-call-report"])
    ]
    ended_reason: Annotated[
        str,
        Field(min_length=1, max_length=50, alias="endedReason", examples=["hangup"]),
    ]
    summary: Annotated[
        str,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the summary of the call."],
        ),
    ]
    transcript: Annotated[
        str, Field(min_length=1, examples=["This is the transcript of the call."])
    ]
    messages: Annotated[
        list[dict[str, str]],
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
    created_by_user_id: int
    created_at: datetime

    class Config:
        populate_by_name = True


class EndOfCallCreate(EndOfCallBase):

    recording_url: Annotated[
        str | None,
        Field(
            pattern=r"^(https?|ftp)://[^\s/$.?#].[^\s]*$",
            alias="recordingUrl",
            examples=["https://vapi-public.s3.amazonaws.com/recordings/1234.wav"],
            default=None,
        ),
    ]

    class Config:
        extra = "forbid"  # replace forbid by ignore if needed
        populate_by_name = True


class EndOfCallMessage(BaseModel):
    message: Annotated[
        EndOfCallCreate,
        Field(
            examples=[
                {
                    "type": "end-of-call-report",
                    "endedReason": "hangup",
                    "recordingUrl": "https://vapi-public.s3.amazonaws.com/recordings/1234.wav",
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


class EndOfCallCreateInternal(EndOfCallCreate):
    created_by_user_id: int


class EndOfCallUpdate(BaseModel):
    type: Annotated[
        str, Field(min_length=1, max_length=50, examples=["end-of-call-report"])
    ]
    ended_reason: Annotated[
        str,
        Field(min_length=1, max_length=50, alias="endedReason", examples=["hangup"]),
    ]
    summary: Annotated[
        str,
        Field(
            min_length=1,
            max_length=63206,
            examples=["This is the updated summary of the call."],
        ),
    ]
    transcript: Annotated[
        str,
        Field(min_length=1, examples=["This is the updated transcript of the call."]),
    ]
    messages: Annotated[
        list[dict[str, str]],
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

    class Config:
        extra = "forbid"
        populate_by_name = True


class EndOfCallUpdateInternal(EndOfCallUpdate):
    updated_at: datetime


class EndOfCallDelete(BaseModel):
    is_deleted: bool
    deleted_at: datetime

    class Config:
        extra = "forbid"
