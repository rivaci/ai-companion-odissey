from langchain_aws import ChatBedrockConverse

model = ChatBedrockConverse(
    model="anthropic.claude-3-sonnet-20240229-v1:0",
    temperature=0,
    max_tokens=None,
    region_name="us-east-1",
    credentials_profile_name="chatbot"
)

messages = [
    ("system", "You are a helpful assistant."),
    ("human", "Who is the president of France?"),
]
message = model.invoke(messages).content
print(message)