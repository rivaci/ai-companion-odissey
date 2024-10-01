import chainlit as cl
from graph import flow  # Import the compiled LangGraph workflow
from langchain_core.messages import HumanMessage, AIMessage
from data import create_data_layer
from chainlit.types import ThreadDict

create_data_layer()

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # Fetch the user matching username from your database
    # and compare the hashed password with the value stored in the database
    if (username, password) == ("admin", "chainlit"):
        return cl.User(
            identifier="admin", metadata={"role": "admin", "provider": "credentials"}
        )
    else:
        return None

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

    # check if there is a history in the user session
    history = cl.user_session.get("history")
    messages = [input_message]
    if history:
        messages = history + messages
        #clean the history
        cl.user_session.set("history", None)        

    msg = cl.Message(content="")
    await msg.send()

    # Stream the response from the LangGraph flow to the user
    async for event in flow.astream_events({"messages" : messages}, config, version="v2"):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if(len(chunk.content) > 0 and chunk.content[-1].get("type", "") == "text"):
                token = chunk.content[-1].get("text", "")
                await msg.stream_token(token)

    # Send a response back to the user
    await msg.update()

@cl.on_chat_resume
async def on_chat_resume(thread: ThreadDict):
    # Set the thread ID in the user session
    cl.user_session.set("id", thread["id"])

    history = [m for m in thread["steps"] if m["type"] == "user_message" or m["type"] == "assistant_message"]

    history_messages= []

    # Create the history messages
    for message in history:
        if message["type"] == "user_message":
            history_messages.append(HumanMessage(content=message["output"]))
        else:
            history_messages.append(AIMessage(content=message["output"]))
            
    # Set the history in the user session
    cl.user_session.set("history", history_messages)
