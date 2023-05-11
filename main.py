from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
from functions import get_chat_completion, translate_message, get_message_corrections
from datetime import datetime

load_dotenv()
FIREBASE_API_CREDS = os.getenv('FIREBASE_API_CREDS')
CLIENT_URL = os.getenv('CLIENT_URL') # "http://localhost:3000"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Firebase stuff
firebase_api_creds = json.loads(FIREBASE_API_CREDS.replace("'", '"'))
cred = credentials.Certificate(firebase_api_creds)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask stuff
app = Flask(__name__)
cors = CORS(app, origins=CLIENT_URL)

"""
@app.route('/test_endpoint', methods=['GET'])
def test_endpoint():
    response_data = {"result": "you got it!"}
    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response
"""

@app.route('/create_user', methods=['POST'])
def create_user(): 
    """This will be called when a user creates an account.
    AND temporarily, also when the user logs in (bc i got a bunch of users that already 
    created accounts, but that are not in the db.)
    It'll check if the user exists in the db.
    If it doesn't, it creates the db item with the empty fields
    """
    print("🔥🔥🔥 FUNCTION CALLED")
    user_id = request.json["userId"]
    # Checks if user exists. If not, it creates it.
    doc_ref = db.collection(u'users').document(user_id)
    if not doc_ref.get().to_dict():
        print("🔥🔥🔥 CREATING USER [placeholder cuz atm im not using this, not necessary]")
        # doc_ref.set({"saved_chats": {}, "saved_words":{}})
    res_data = {"response": "create_user_enpoint"}
    response = make_response(jsonify(res_data))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/get_saved_chats', methods=['GET'])
def get_saved_chats():
    # Getting saved chats from Firebase
    user_id = request.args.get('user_id')
    doc_ref = db.collection(u'users').document(user_id)
    saved_chats = []
    
    for chat in doc_ref.collection("saved_chats").list_documents():
        saved_chats.append(chat.get().to_dict())

    # saved_chats.sort(key=lambda chat_element: chat_element[0]) # change the sort cuz saved_chats is now a list of dicts

    print("👀👀 Saved chats", saved_chats)
    response = make_response(jsonify(saved_chats))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/save_chat', methods=['POST'])
def save_chat():
    chat_history = request.json["chatHistory"]
    user_id = request.json["userId"]
    topic = request.json["currentTopic"]
    timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S:%f")
    doc_ref = db.collection(u'users').document(user_id)
    doc_ref.collection("saved_chats").document(timestamp).set({"id":timestamp, "topic":topic, "messages":chat_history})
    response = make_response(jsonify({"response": "chat was saved"}))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/unsave_chat', methods=['POST'])
def unsave_chat():
    user_id = request.json["userId"]
    chat_id = request.json["chatId"]
    doc_ref = db.collection(u'users').document(user_id)
    doc_ref.collection("saved_chats").document(chat_id).delete()
    response = make_response(jsonify({"response": "chat was UNsaved"}))
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/send_message', methods=['POST'])
def send_message():
    chat_history = request.json["chatHistory"]
    source_language = request.json["sourceLanguage"]
    target_language = request.json["targetLanguage"]
    current_topic = request.json["currentTopic"] # Create different prompts for each topic.
    is_suggestion = request.json["isSuggestion"]
    ai_message = get_chat_completion(OPENAI_API_KEY, chat_history, current_topic, source_language, target_language, is_suggestion)
    response = make_response(jsonify(ai_message))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/get_corrections', methods=['GET'])
def get_corrections():
    user_message = request.args.get('userMessage')
    source_language = request.args.get("sourceLanguage")
    target_language = request.args.get("targetLanguage")
    is_suggestion = request.args.get("isSuggestion")
    corrections = get_message_corrections(OPENAI_API_KEY,user_message, source_language, target_language, is_suggestion)
    # response_data = {"result": corrections}
    response = make_response(jsonify(corrections))
    response.headers["Content-Type"] = "application/json"
    return response










@app.route('/translate', methods=['POST'])
def translate():
    message = request.json["messageContent"]
    source_language = request.json["sourceLanguage"]
    target_language = request.json["targetLanguage"]
    print(f"SOURCE {source_language} | TARGET {target_language}")
    translation = translate_message(message, from_=target_language, to=source_language)
    response = make_response(jsonify({"translation": translation}))
    response.headers["Content-Type"] = "application/json"
    return response




if __name__ == "__main__":
    # host="0.0.0.0", port=5000
    app.run()
