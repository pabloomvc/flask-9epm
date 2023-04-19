import openai
from easygoogletranslate import EasyGoogleTranslate

def get_chat_completion(api_key, chat_history, source_language, target_language):
    with open("prompt.txt", "r") as file:
        prompt_content = file.read()

    prompt_content = prompt_content.replace("<source_language>", source_language)
    prompt_content = prompt_content.replace("<target_language>", target_language)
    system_message_object = {"role": "system", "content": prompt_content}

    full_chat_history = [system_message_object] + chat_history

    openai.api_key = api_key
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages= full_chat_history
    )
    chat_history.append(completion.choices[0].message)
    
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





