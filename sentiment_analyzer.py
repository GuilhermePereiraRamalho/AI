from openai import OpenAI
from dotenv import load_dotenv
import os
import openai

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

def load(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Error: {e}")

def save(file_name, content):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error while saving file: {e}")       


def sentiment_analyzer(product):
    system_prompt = f"""
        You are a sentiment analyzer for product reviews.
        Write a paragraph with up to 50 words summarizing the reviews and
        then assign the overall sentiment for the product.
        Also, identify 3 strengths and 3 weaknesses identified from the reviews.

        yaml
        Copiar código
            # Output Format

            Product Name:
            Reviews Summary:
            Overall Sentiment: [use here only Positive, Negative, or Neutral]
            Strengths: list with three bullets
            Weaknesses: list with three bullets
    """
   
    user_prompt = load(f"data\\reviews-{product}.txt")
    print(f"Started sentiment analysis for the product {product}")

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

    try:
        response = client.chat.completions.create(
            messages=message_list,
            model=model
        )

        response_text = response.choices[0].message.content
        save(f"data\\analysis-{product}.txt", response_text)
    except openai.AuthenticationError as e:
        print(f"Authentication Error: {e}")
    except openai.APIError as e:
        print(f"Api Error: {e}")

product_list = ["Jeans Made with Recycled Materials", "Organic Cotton T-Shirts", "Mineral Makeup"]

for product in product_list:    
    sentiment_analyzer(product)