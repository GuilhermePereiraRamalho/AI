from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

def product_categorizer(product_name, category_list):
    system_prompt = f"""
            You are a product categorizer. You should assume the categories present in the list below.

            # List of Valid Categories
            {category_list.split(",")}

            # Output Format
            Product: Product Name
            Category: Display the product category

            # Example Output
            Product: Solar-Powered Electric Toothbrush
            Category: Green Electronics
        """

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": 'user',
                'content': product_name
            }
        ],
        model = model,
        temperature = 0,
        max_tokens=200
    )

    return response.choices[0].message.content

valid_categories = input('Provide the valid categories, separated by commas: ')

while True:
    product_name = input("Enter the product name: ")
    response = product_categorizer(product_name, valid_categories)
    print(response)