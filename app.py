import chainlit as cl
from app.chat.chat import Agent

agent = Agent()

# Combinación de las dos funciones de inicio de chat
@cl.on_chat_start
async def on_start():
    await agent.set_starters()
    await agent.start_chat()


# Reanudar chat
@cl.on_chat_resume
async def on_resume():
    await agent.resume_chat()


# Manejo de mensajes
@cl.on_message
async def on_message(message: cl.Message):
    await agent.main(message)

