import chainlit as cl
from app.chat.openai import OpenAIAgent
from app.persistance.vector.openai import OpenAIVectorDB

openai_agent = OpenAIAgent()
vector_db = OpenAIVectorDB()


@cl.on_chat_start
async def on_start():
    await openai_agent.set_starters()
    await openai_agent.start_chat()


@cl.on_chat_resume
async def on_resume():
    await openai_agent.resume_chat()


@cl.on_message
async def on_message(message: cl.Message):
    await openai_agent.main(message)
