import chainlit as cl
from app.chat.chat import Agent
from app.vector_db.db import VectorDB
from app.config import Settings

agent = Agent()
vector_db = VectorDB()


@cl.on_chat_start
async def on_start():
    VectorDB.upload_pdf_to_openai(Settings.PDF_PATH)
    await agent.set_starters()
    await agent.start_chat()


@cl.on_chat_resume
async def on_resume():
    await agent.resume_chat()


@cl.on_message
async def on_message(message: cl.Message):
    await agent.main(message)
