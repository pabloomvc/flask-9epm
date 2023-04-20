import openai
import json
from easygoogletranslate import EasyGoogleTranslate

def get_chat_completion(api_key, chat_history, source_language, target_language):

    with open("initial_prompt.txt", "r") as initial_prompt_file:
        prompt_content = initial_prompt_file.read()
        prompt_content = prompt_content.replace("<source_language>", source_language)
        prompt_content = prompt_content.replace("<target_language>", target_language)
        system_message_object = {"role": "system", "content": prompt_content}

    with open("message_instructions.txt", "r") as message_instructions_file:
        instructions = message_instructions_file.read()
        instructions = instructions.replace("<user_message>", chat_history[-1]["content"])
        instructions = instructions.replace("<source_language>", source_language)
        instructions = instructions.replace("<target_language>", target_language)
        temp_message = {"role":"user", "content":instructions}
    
    full_chat_history = [system_message_object] + chat_history[:-1] + [temp_message]
    clean_chat_history = [{"role": message["role"], "content": message["content"]} for message in full_chat_history]


    openai.api_key = api_key
    completion = openai.ChatCompletion.create(temperature=0.3, model="gpt-3.5-turbo", messages= clean_chat_history)

    resulting_message = {
        "role": completion.choices[0].message["role"], 
        "content": json.loads(completion.choices[0].message["content"])["response"], 
        "suggestions": json.loads(completion.choices[0].message["content"])["suggestions"], 
        "translation": json.loads(completion.choices[0].message["content"])["translation"]}
    
    chat_history.append(resulting_message)
    
    print("💪 New chat history")
    for msg in chat_history:
        print(msg)

    return chat_history


def translate_message(message, from_="es", to="en"):
    """At the moment I'm passing "message", but I could have this translate
    a single word at a time, and/or the sentence of that word."""

    language_codes = {
        "Spanish": "es", "English": "en", "Italian": "it", "French": "fr"
    }


    translator = EasyGoogleTranslate(
    source_language=language_codes[from_],
    target_language=language_codes[to],
    timeout=10
    )
    result = translator.translate(message)
    return result





