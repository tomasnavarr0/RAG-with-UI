from typing import Any
import chainlit as cl
from openai import AsyncAssistantEventHandler


class EventHandler(AsyncAssistantEventHandler):
    def __init__(self, assistant_name: str) -> None:
        super().__init__()
        self.current_message: cl.Message | None = None
        self.assistant_name = assistant_name

    async def on_text_created(self, *_: Any) -> None:
        self.current_message = await cl.Message(author=self.assistant_name, content="").send()

    async def on_text_delta(self, delta: Any, *_: Any) -> None:
        if not self.current_message:
            msg = "Not available message"
            raise ValueError(msg)

        await self.current_message.stream_token(delta.value)

    async def on_text_done(self, *_: Any) -> None:
        if not self.current_message:
            msg = "Not available message"
            raise ValueError(msg)

        await self.current_message.update()
