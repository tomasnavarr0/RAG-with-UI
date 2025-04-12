import chainlit as cl
from app.chat.chat import Agent
from app.vector_db.db import VectorDB

agent = Agent()
vector_db = VectorDB()


@cl.on_chat_start
async def on_start():
    vector_db.add_all()
    await agent.set_starters()
    await agent.start_chat()


@cl.on_chat_resume
async def on_resume():
    await agent.resume_chat()


@cl.on_message
async def on_message(message: cl.Message):
    await agent.main(message)
