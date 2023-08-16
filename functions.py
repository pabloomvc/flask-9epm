import openai
import json
from easygoogletranslate import EasyGoogleTranslate
import pprint
import time
from datetime import datetime

def get_chat_completion(api_key, chat_history, current_topic, source_language, target_language, is_suggestion):

    # Load system prompt
    with open("prompts/initial_prompt.txt", "r") as initial_prompt_file:
        initial_prompt_content = initial_prompt_file.read()
        
    if current_topic["type"] == "situation":
        with open("prompts/situation_prompts/situation_prompt.txt", "r") as situation_prompt_file:
            situation_message = situation_prompt_file.read()
    elif current_topic["type"] == "personal":
        with open("prompts/situation_prompts/personal_prompt.txt", "r") as personal_prompt_file:
            situation_message = personal_prompt_file.read()
    elif current_topic["type"] == "interests":
        with open("prompts/situation_prompts/interests_prompt.txt", "r") as interests_prompt_file:
            situation_message = interests_prompt_file.read()
    elif current_topic["type"] == "productivity":
        with open("prompts/situation_prompts/productivity_prompt.txt", "r") as productivity_prompt_file:
            situation_message = productivity_prompt_file.read()

    system_prompt = f"{initial_prompt_content}\n{situation_message}"
    system_prompt = system_prompt.replace("<situation>", current_topic["title"])
    system_prompt = system_prompt.replace("<source_language>", source_language)
    system_prompt = system_prompt.replace("<target_language>", target_language)

    system_prompt_object = {"role": "system", "content": system_prompt}

    # Add the instructions to the last message in the chat.
    with open("prompts/message_instructions.txt", "r") as message_instructions_file:
        instructions = message_instructions_file.read()
        # instructions = instructions.replace("<user_message>", chat_history[-1]["content"])
        instructions = instructions.replace("<source_language>", source_language)
        instructions = instructions.replace("<target_language>", target_language)
        instructions_message = {"role": "user", "content": instructions}

    if len(chat_history)==0:
        print("🚀", chat_history)
        full_chat_history = [system_prompt_object] + [instructions_message]
    else:
        # chat_history[-1]["content"] += f"\n\ninstructions"
        full_chat_history = [system_prompt_object] + chat_history + [instructions_message]
        
    #full_chat_history[-1]["content"] = full_chat_history[-1]["content"] + "\n\n" + instructions

    
    clean_chat_history = [{"role": message["role"], "content": message["content"]} for message in full_chat_history]
    print("\nFULL CHAT CLEAN")
    for msg in clean_chat_history:
        print(msg)
    
    # Getting completion --------------------------------------------------------------
    openai.api_key = api_key
    main_completion = openai.ChatCompletion.create(temperature=0.9, model="gpt-3.5-turbo", messages= clean_chat_history)
    pp = pprint.PrettyPrinter(indent=4)
    print("🟢1️⃣")
    pp.pprint(main_completion.choices[0].message["content"])

    # Parsing the result --------------------------------------------------------------
    main_completion_response = json.loads(main_completion.choices[0].message["content"])
    resulting_message = {
        "role": main_completion.choices[0].message["role"], 
        "content": main_completion_response["reply"], 
        "suggestions": main_completion_response["suggestions"], 
        "translation": main_completion_response["translation"]}
    
    # Logs -----------------------------------------------------------------------------
    print("\nLOGS ------------")
    try:
        print(f"User said: {chat_history[-1]['content']}")
    except IndexError:
        print("CONVERSATION STARTED")
    print(f"Current Topic: {current_topic}")
    print(f"Versa Replies: {resulting_message['content']}")
    print(f"Versa Translated: {resulting_message['translation']}")

    chat_history.append(resulting_message)
    
    return chat_history


def get_tutor_message(api_key, current_topic, target_language, tutor_command, user_question):
    print("⭐⭐⭐⭐⭐⭐⭐", current_topic, target_language, tutor_command, user_question)
    
    openai.api_key = api_key

    if tutor_command == "/phrasing":
        with open("prompts/tutor_prompts/phrasing_prompt.txt", "r") as phrasing_prompt_file:
            system_msg = phrasing_prompt_file.read()
        
        system_msg = system_msg.replace("<target_language>", target_language)
        chat_history = [{"role": "system", "content": system_msg}, {"role": "user", "content": user_question}]
        main_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-4", messages= chat_history)
        print(main_completion.choices[0].message["content"])
        main_completion_response = json.loads(main_completion.choices[0].message["content"], strict=False)
        resulting_message = {
            "role": "assistant", 
            "tutor_command": tutor_command,
            "response": main_completion_response["response"], 
            "phrases": main_completion_response["phrases"]
            }
    elif tutor_command == "/vocab":
        with open("prompts/tutor_prompts/vocabulary_prompt.txt", "r") as vocabulary_prompt_file:
            system_msg = vocabulary_prompt_file.read()
        system_msg = system_msg.replace("<target_language>", target_language)
        chat_history = [{"role": "system", "content": system_msg}, {"role": "user", "content": user_question}]
        main_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-4", messages= chat_history)
        print(main_completion.choices[0].message["content"])
        main_completion_response = json.loads(main_completion.choices[0].message["content"], strict=False)
        resulting_message = {
            "role": "assistant", 
            "tutor_command": tutor_command,
            "response": main_completion_response["response"], 
            "vocab": main_completion_response["vocab"]
            }
    elif tutor_command == "/grammar":
        with open("prompts/tutor_prompts/grammar_prompt.txt", "r") as grammar_prompt_file:
            system_msg = grammar_prompt_file.read()
            print(system_msg)

        system_msg = system_msg.replace("<target_language>", target_language)
        chat_history = [{"role": "system", "content": system_msg}, {"role": "user", "content": user_question}]
        main_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-4", messages= chat_history)
        print(main_completion.choices[0].message["content"])
        main_completion_response = json.loads(main_completion.choices[0].message["content"], strict=False)   
        resulting_message = {
            "role": "assistant", 
            "tutor_command": tutor_command,
            "title": main_completion_response["title"], 
            "explanation": main_completion_response["explanation"],
            "examples": main_completion_response["examples"]
            }  
    elif tutor_command == "/examples":
        # TODO: The prompt, modeing the resulting_message, and the frontend to display the information.
        with open("prompts/tutor_prompts/examples_prompt.txt", "r") as examples_prompt_file:
            system_msg = examples_prompt_file.read()
            print(system_msg)

        
        user_template=f"""
User Message: {user_question}        
Format your response as JSON containing the following keys:
- "response": A friendly response to the user, explaining the usage of the word/expression if necessary, in English.
- "sentences": An array of 7 arrays. Each sub-array should look like this: [<example sentence in {target_language}>: <English translation>]"""
        system_msg = system_msg.replace("<target_language>", target_language)
        chat_history = [{"role": "system", "content": system_msg}, {"role": "user", "content": user_template}]
        main_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-4", messages= chat_history)
        print(main_completion.choices[0].message["content"])
        main_completion_response = json.loads(main_completion.choices[0].message["content"], strict=False)   
        resulting_message = {
            "role": "assistant", 
            "tutor_command": tutor_command,
            "response": main_completion_response["response"],
            "sentences": main_completion_response["sentences"]
            }
    else:
        with open("prompts/tutor_prompts/base_prompt.txt", "r") as base_prompt_file:
            system_msg = base_prompt_file.read()
        user_template = f"""
User Message: {user_question}
Format your responses as JSON containing the following keys:
- "title": A title summarizing the user's question.
- "explanation": A friendly, concise, and detailed explanation, centered exclussively around learning {target_language}, and providing examples when necessary."""
        system_msg = system_msg.replace("<target_language>", target_language)
        chat_history = [{"role": "system", "content": system_msg}, {"role": "user", "content": user_template}]
        main_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-4", messages= chat_history)
        
        print("🤣", main_completion.choices[0].message["content"])
        main_completion_response = json.loads(main_completion.choices[0].message["content"], strict=False)   
        resulting_message = {
            "role": "assistant", 
            "tutor_command": tutor_command,
            "title": main_completion_response["title"], 
            "explanation": main_completion_response["explanation"]
            }
    
    chat_history.append(main_completion_response)
    return resulting_message



def get_message_corrections(api_key, user_message, source_language, target_language, is_suggestion=False):
    
    # GETTING MESSAGE CORRECTIONS!
    # Right now im doing it with gpt, but I MIGHT have to find (cheaper) alternatives.
    # Creating the message for the 2nd call to the gpt, to get the user's errors and corrections.
    # I figured this would take some of the load off the other call, and help the gpt avoid confusion. Let's see.
    
    openai.api_key = api_key
    if is_suggestion == "false":
        with open("prompts/get_corrections_prompt.txt", "r") as get_corrections_file:
            corrections_message = get_corrections_file.read()
            corrections_message = corrections_message.replace("<source_language>", source_language)
            corrections_message = corrections_message.replace("<target_language>", target_language)
            corrections_message = corrections_message.replace("<user_message>", user_message)
            corrections_message_dict = [{"role": "assistant", "content": corrections_message}]
        corrections_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-4", messages=corrections_message_dict)
        corrections_response = json.loads(corrections_completion.choices[0].message["content"])
    else: 
        time.sleep(2)
        corrections_response = {"corrected_message": None, "translated_message": None, "errors": []}
    
    pp = pprint.PrettyPrinter(indent=4)

    print(f"\n[{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]")
    print(f"---- {source_language} to {target_language} ----")
    print(f"User Message: {user_message}")
    try:
        print(f"Corrected Message: {corrections_response['corrected_message']}")
        print(f"Translation: {corrections_response['translated_message']}")
        print(f"Errors: {corrections_response['errors']}")
    except Exception as e:
        print("\nError logging the corrections_response")
        print(corrections_response)
        print(e)



    return corrections_response

def translate_word_by_word(api_key, target_language, message):
    openai.api_key = api_key

    with open("prompts/word_by_word/system_prompt.txt", "r") as system_prompt_file:
        system_prompt = system_prompt_file.read()
        system_prompt = system_prompt.replace("<target_language>", target_language)

    with open("prompts/word_by_word/message_prompt.txt", "r") as message_prompt_file:
        formatting_prompt = message_prompt_file.read()
        # formatting_prompt = formatting_prompt.replace("<message>", message)

    messages = [
    {"role": "system", 
        "content": system_prompt},
    {"role": "user",
        "content": f"Translate the following message from {target_language} to English, word by word:\n{message}"
        }, 
    {"role": "user", 
     "content": formatting_prompt}
    ]
    if message:
        main_completion = openai.ChatCompletion.create(temperature=0.3, model="gpt-4", messages=messages)
        main_completion_json = json.loads(main_completion.choices[0].message["content"])
    else:
        main_completion = {"translations":[]}
        
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(main_completion.choices[0].message["content"])
    # print("COMPLETION TYPE:", type(main_completion.choices[0].message["content"]))
    return main_completion_json


# OPENAI_API_KEY = OPENAI_API_KEY="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"
# translate_word_by_word(OPENAI_API_KEY, "Spanish", "Gracias! La pizza estaba deliciosa. ¿Cómo puedo pagarte?")


# ---------------------------------------------------------------------------------------------------------------

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




'''
import os
from dotenv import load_dotenv
pp = pprint.PrettyPrinter(indent=4)
load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY

messages = [
    {"role": "system", "content": "you're a helpful assistant, designed to help the user with language-related tasks."},
    {"role": "user", 
     "content": """I will give you a sentence, and you will give me a phrase-by-phrase translation to Italian.
    Tenía muchísima hambre anoche, así que decidí hacerme un sandwich de tocino. También le agregué algo de lechuga y tomate. Estuvo buenísimo.
     Format your response as JSON with the following keys: 
     - tranlated_words: an array with the words and their translations {"phrase": <phrase_1>, "translation": <translation_1 to Italian>}
     """
     }
]
     #'I was very hungry last night, so I decided to make me a bacon sandwich. I also added some lettuce and tomato. It was amazing.'

main_completion = openai.ChatCompletion.create(temperature=0.1, model="gpt-3.5-turbo", messages=messages)
pp.pprint(main_completion.choices[0].message["content"])'''