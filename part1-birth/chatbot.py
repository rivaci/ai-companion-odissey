import chainlit as cl
from graph import flow  # Import the compiled LangGraph workflow
from chainlit.input_widget import Select, Switch, Slider
from langchain_core.messages import HumanMessage

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
    final_state = flow.invoke({"messages" : [input_message]}, config)
    content = final_state["messages"][-1].content

    # Send a response back to the user
    await cl.Message(
        content
    ).send()