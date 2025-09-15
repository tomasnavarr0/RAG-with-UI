import chainlit as cl
from openai import AsyncOpenAI
from openai.types.beta import Assistant
from app.config import Settings
from app.utils import FileUtilsWrapper
from .event_handler import EventHandler


class Agent:
    client: AsyncOpenAI = AsyncOpenAI(api_key=Settings.OPENAI_API_KEY)
    file_utils: FileUtilsWrapper = FileUtilsWrapper(client)

    @property
    async def assistant(self) -> Assistant:
        return await self.client.beta.assistants.retrieve(Settings.ASSISTANT_ID)

    @staticmethod
    @cl.set_starters
    async def set_starters() -> list[cl.Starter]:
        return [
            cl.Starter(
                label="Que es una Escritura?",
                message="Que es una Escritura?",
                icon="/public/2.png",
            ),
            cl.Starter(label="Reales", message="Que son los derechos Reales", icon="/public/3.png"),
            cl.Starter(
                label="Colegio de Escribanos",
                message="Que es el colegio de escribanos",
                icon="/public/3.png",
            ),
            cl.Starter(
                label="Matricula",
                message="Como obtener la Matricula?",
                icon="/public/3.png",
            ),
        ]

    @cl.on_chat_start
    async def start_chat(self) -> None:
        thread = await self.client.beta.threads.create()
        cl.user_session.set("thread_id", thread.id)

    @cl.on_chat_resume
    async def resume_chat(self) -> None:
        thread_id = cl.user_session.get("thread_id")
        if not thread_id:
            await self.start_chat()

    @cl.on_message
    async def main(self, message: cl.Message) -> None:
        thread_id = cl.user_session.get("thread_id")

        attachments = await self.file_utils.process_files(message.elements)

        await self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message.content,
            attachments=attachments,
        )

        assistant = await self.assistant
        async with self.client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant.id,
            event_handler=EventHandler(assistant_name=assistant.name or "Assistant"),
        ) as stream:
            await stream.until_done()
