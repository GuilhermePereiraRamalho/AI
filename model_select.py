from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

encoder = tiktoken.encoding_for_model(model)

def load(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Error: {e}")

system_prompt = """
Identify the buying profile for each customer below.

The output format should be:

customer - describe the customer's profile in 3 words
"""

user_prompt = load("data\list_of_purchases_100_customers.csv")

token_list = encoder.encode(system_prompt + user_prompt)
num_tokens = len(token_list)
print(f"Number of tokens in input: {num_tokens}")
expected_output_size = 2048

if num_tokens >= 4096 - expected_output_size:
    model = "gpt-4-1106-preview"

print(f"Chosen model: {model}")

message_list = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

response = client.chat.completions.create(
    messages = message_list,
    model=model
)

print(response.choices[0].message.content)