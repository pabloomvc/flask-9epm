import openai

def query_gpt():

    openai.api_key = "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"
    text = openai.ChatCompletion.create(
        engine = "gpt-3.5-turbo",
        temperature = 0.7,
        n=1,
        max_tokens = 300,
        prompt=f"""
        I'm developing chatbot, which users will be able to maintain long and casual conversations with. 
        Explain in detail how suitable the model gpt-3.5-turbo is to fulfill this purpose.
        """
        )

    return text

def get_chat_completion(chat_history):


    with open("prompt.txt", "r") as file:
        prompt_content = file.read()
        system_message_object = {"role": "system", "content": prompt_content}

    full_chat_history = [system_message_object] + chat_history

    openai.api_key = "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"
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= full_chat_history
    )
    chat_history.append(completion.choices[0].message)
    
    print("💪 New chat history")
    for msg in chat_history:
        print(msg)

    return chat_history





