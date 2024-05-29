from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4"

def load(file_name):
    try:
        with open(file_name, "r") as file:
            data = file.read()
            return data
    except IOError as e:
        print(f"Error loading file: {e}")

def save(file_name, content):
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(content)
    except IOError as e:
        print(f"Error saving file: {e}")

def analyze_transaction(transaction_list):
    print("1. Starting transaction analysis")
    system_prompt = """
    Analyze the following financial transactions and identify whether each of them is a "Possible Fraud" or should be "Approved".
    Add a "Status" attribute with one of the values: "Possible Fraud" or "Approved".

    Each new transaction should be inserted into the JSON list. Follow the response format below.

    # Possible fraud indications
    - Transactions with very discrepant values
    - Transactions that occur in very distant locations from each other
    
    # Output Format
    {
        "transactions": [
            {
            "id": "id",
            "type": "credit or debit",
            "establishment": "establishment name",
            "time": "transaction time",
            "amount": "R$XX.XX",
            "product_name": "product name",
            "location": "city - state (Country)"
            "status": ""
            },
        ]
    } 
    """

    message_list = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": f"Consider the CSV below, where each line is a different transaction: {transaction_list}. Your response should follow the #Response Format (just a json with no other comments)"
        }
    ]

    response = client.chat.completions.create(
        messages = message_list,
        model=model,
        temperature=0
    )

    content = response.choices[0].message.content.replace("'", '"')
    print("\nContent:", content)
    json_result = json.loads(content)
    print("\nJSON:", json_result)
    return json_result

# code omitted

def generate_report(transaction):
    print("2. Generating report for transaction ", transaction["id"])
    system_prompt = f"""
    For the following transaction, provide a report only if its status is "Possible Fraud". Provide in the report a justification for why you identify it as fraud.
    Transaction: {transaction}

    ## Response Format
    "id": "id",
    "type": "credit or debit",
    "establishment": "establishment name",
    "time": "transaction time",
    "amount": "R$XX.XX",
    "product_name": "product name",
    "location": "city - state (Country)"
    "status": "",
    "report" : "Put Not Applicable if the status is Approved"
    """

    messages_list = [
        {
            'role': 'user',
            'content': system_prompt
        }
    ]

    response = client.chat.completions.create(
        messages=messages_list,
        model=model
    )

    content =  response.choices[0].message.content
    print("Finished generating report")
    return content

def generate_recommendation(report):
    print('3. Generating recommendations')
    system_prompt = f"""
    For the following transaction, provide an appropriate recommendation based on the status and transaction details: {report}

    Recommendations could be "Notify Customer", "Trigger Anti-Fraud Department", or "Perform Manual Verification".
    They should be written in technical format.

    Also include a classification of the type of fraud, if applicable.
    """
    message_list = [
        {
            'role': 'system',
            'content': system_prompt
        }
    ]
    response =  client.chat.completions.create(
        messages=message_list,
        model=model
    )
    content = response.choices[0].message.content
    print('Finished generating recommendation')
    return content

transaction_list = load("data\\transaction.csv")
analyzed_transactions = analyze_transaction(transaction_list)

for transaction in analyzed_transactions["transactions"]: 
    if transaction["status"] == "Possible Fraud": 
        report = generate_report(transaction)
        recommendation = generate_recommendation(report)
        transaction_id = transaction["id"]
        product_transaction = transaction['product_name']
        transaction_status  = transaction['status']
        save(f'transaction-{transaction_id}-{product_transaction}-{transaction_status}.txt', recommendation)
