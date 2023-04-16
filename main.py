from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from ai_functions import get_chat_completion

load_dotenv()
CLIENT_URL = os.getenv('CLIENT_URL') # "http://localhost:3000"
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# Flask stuff
app = Flask(__name__)
cors = CORS(app, origins=CLIENT_URL)

@app.route('/test_endpoint', methods=['GET'])
def test_endpoint():
    response_data = {"result": "you got it!"}
    response = make_response(jsonify(response_data))
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/send_message', methods=['POST'])
def send_message():
    chat_history = request.json["chatHistory"]
    print("💪", chat_history)
    ai_message = get_chat_completion(OPENAI_API_KEY, chat_history)
    response_data = {"result": ai_message}
    response = make_response(jsonify(ai_message))
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == "__main__":
    # host="0.0.0.0", port=5000
    app.run()
