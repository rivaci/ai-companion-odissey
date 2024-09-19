import argparse
from langgraph.graph import StateGraph, MessagesState
from langchain_aws import ChatBedrockConverse
from langgraph.checkpoint.memory import MemorySaver
from utils import save_graph_to_file

# Create the memory checkpointer
memory = MemorySaver()

# Create the model
model = ChatBedrockConverse(
    model="anthropic.claude-3-5-sonnet-20240620-v1:0",
    temperature=0,
    max_tokens=None,
    region_name="us-east-1",
    credentials_profile_name="chatbot"
)

# Define the function that generates the assistant response
def generate_answer(state: MessagesState):
    return {"messages": [model.invoke(state["messages"])]}

# Initialize the LangGraph workflow
chatbot_graph = StateGraph(MessagesState)

# Add a node that generates an answer
chatbot_graph.add_node("response", generate_answer)

# Define the flow: Start at "response" and then end
chatbot_graph.set_entry_point("response")
chatbot_graph.set_finish_point("response")

# Compile the graph
flow = chatbot_graph.compile(checkpointer=memory)

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description="Save chatbot graph to file")
    parser.add_argument(
        "file_path", 
        type=str, 
        help="The file path to save the graph image (e.g., 'graph.png')"
    )
    parser.add_argument(
        "--format", 
        type=str, 
        default="png", 
        choices=["png", "svg"], 
        help="The format of the image file (default is 'png')"
    )

    # Parse command-line arguments
    args = parser.parse_args()

    # Save the graph to the specified file
    save_graph_to_file(flow, args.file_path, format=args.format)
