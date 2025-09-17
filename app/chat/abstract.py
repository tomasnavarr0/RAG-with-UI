from abc import ABC, abstractmethod
import chainlit as cl


class AbstractAgent(ABC):
    @staticmethod
    @abstractmethod
    @cl.set_starters
    async def set_starters() -> list[cl.Starter]:
        pass

    @abstractmethod
    @cl.on_chat_start
    async def start_chat(self) -> None:
        pass

    @abstractmethod
    @cl.on_chat_resume
    async def resume_chat(self) -> None:
        pass

    @abstractmethod
    @cl.on_message
    async def main(self, message: cl.Message) -> None:
        pass
