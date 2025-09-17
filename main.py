import chainlit as cl
from app.chat import OllamaAgent
from app.persistance.vector import ChromaVectorDB

agent = OllamaAgent()
vector_db = ChromaVectorDB()


@cl.on_chat_start
async def on_start():
    await agent.set_starters()
    await agent.start_chat()


@cl.on_chat_resume
async def on_resume():
    await agent.resume_chat()


@cl.on_message
async def on_message(message: cl.Message):
    await agent.main(message)
