import tiktoken

model = "gpt-4"
encoder = tiktoken.encoding_for_model(model)
token_list = encoder.encode("You are a product categorizer.")

print("Token List: ", token_list)
print("Number of tokens: ", len(token_list))
print(f"Cost for the {model} model is ${(len(token_list)/1000) * 0.03}")

model = "gpt-3.5-turbo-1106"
encoder = tiktoken.encoding_for_model(model)
token_list = encoder.encode("You are a product categorizer.")

print("Token List: ", token_list)
print("Number of tokens: ", len(token_list))
print(f"Cost for the {model} model is ${(len(token_list)/1000) * 0.001}")


print(f"The cost of GPT-4 is {0.03/0.001} times higher than that of GPT-3.5 Turbo")