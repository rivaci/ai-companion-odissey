from langchain_aws import ChatBedrockConverse
from dotenv import load_dotenv

load_dotenv()

model = ChatBedrockConverse(
    model="anthropic.claude-3-5-sonnet-20240620-v1:0",
    temperature=0,
    max_tokens=None
)

messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Who is the president of France?"),
]
message = model.invoke(messages).content
print(message)