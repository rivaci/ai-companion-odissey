import chainlit as cl
from graph import flow  # Import the compiled LangGraph workflow
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.messages.ai import AIMessageChunk

 
# Define the starters
@cl.set_starters
def set_starters():
    return [
        cl.Starter(
            label="Tell me something interesting !",
            message="Give me an interesting fact about history or science.",
            icon="/public/idea.svg"
        ),
        cl.Starter(
            label="What is quantum computing?",
            message="Explain what quantum computing is in simple terms.",
            icon="/public/idea.svg"
        ),
        cl.Starter(
            label="Explain photosynthesis",
            message="Can you explain how photosynthesis works? Include the key steps in the process.",
            icon="/public/idea.svg"
        )
    ]

@cl.on_message
async def main(message: cl.Message):

    # Invoke the LangGraph flow to get the assistant's response
    thread_id = cl.user_session.get("id")
    config = {"configurable": {"thread_id": thread_id }}
    input_message = HumanMessage(content=message.content)

    msg = cl.Message(content="")
    await msg.send()

    async for event in flow.astream_events({"messages" : [input_message]}, config, version="v2"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if(isinstance(chunk, AIMessageChunk) and len(chunk.content) > 0 and chunk.content[-1].get("type", "") == "text"):
                token = chunk.content[-1].get("text", "")
                await msg.stream_token(token)

    # Send a response back to the user
    await msg.update()
