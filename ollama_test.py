from ollama import chat

response = chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": "Who are you?"
        }
    ]
)

print(response["message"]["content"])