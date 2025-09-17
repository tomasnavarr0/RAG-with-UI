import chainlit as cl
from ollama import AsyncClient
from app.config import Settings
from .abstract import AbstractAgent


class OllamaAgent(AbstractAgent):
    client: AsyncClient = AsyncClient(host=Settings.OLLAMA_HOST)

    @staticmethod
    @cl.set_starters
    async def set_starters() -> list[cl.Starter]:
        return [
            cl.Starter(label="Que es una Escritura?", message="Que es una Escritura?", icon="/public/2.png"),
            cl.Starter(label="Reales", message="Que son los derechos Reales", icon="/public/3.png"),
            cl.Starter(label="Colegio de Escribanos", message="Que es el colegio de escribanos", icon="/public/3.png"),
            cl.Starter(label="Matricula", message="Como obtener la Matricula?", icon="/public/3.png"),
        ]

    @cl.on_chat_start
    async def start_chat(self) -> None:
        cl.user_session.set("history", [])

    @cl.on_chat_resume
    async def resume_chat(self) -> None:
        if cl.user_session.get("history") is None:
            await self.start_chat()

    @cl.on_message
    async def main(self, message: cl.Message) -> None:
        history = cl.user_session.get("history") or []

        prompt = ""
        for turn in history:
            prompt += f"{turn['role']}: {turn['content']}\n"
        prompt += f"user: {message.content}\nassistant:"

        response = await self.client.generate(
            model=Settings.OLLAMA_MODEL,
            prompt=prompt,
            stream=True,
        )

        msg = cl.Message(content="")
        full_response = ""

        async for part in response:
            if not part["done"]:
                token = part["response"]
                full_response += token
                await msg.stream_token(token)

        await msg.send()

        history.append({"role": "user", "content": message.content})
        history.append({"role": "assistant", "content": full_response})
        cl.user_session.set("history", history)
