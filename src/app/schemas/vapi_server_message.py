# ./src/app/schemas/vapi_server_message.py
from typing import Annotated, Union

from pydantic import BaseModel, Field

from .vapi_end_of_call import VapiEndOfCallBase
from .vapi_conversation_update import VapiConversationUpdateBase


class VapiServerMessage(BaseModel):
    message: Annotated[
        Union[VapiEndOfCallBase, VapiConversationUpdateBase],
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
