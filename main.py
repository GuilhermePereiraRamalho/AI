from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "List only the names of the products, disregarding descriptions."
        },
        {
            "role": 'user',
            'content': 'List 3 sustainable products'
        }
    ],
    model="gpt-4o"
)

print(response.choices[0].message.content)
