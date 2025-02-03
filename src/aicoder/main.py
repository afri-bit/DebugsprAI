import os
import openai

openai_key = os.getenv("OPENAI_API_KEY")

# Replace with your OpenAI API key
client = openai.OpenAI(api_key=openai_key)


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

print(response.choices[0].message.content)