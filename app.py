from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load configuration from .env file
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
PROJECT_ID = os.getenv('PROJECT_ID')
LOCATION = os.getenv('LOCATION', 'global')  # Default to global if not set

# Gemini API configuration
MODEL_PATH = "gemini-2.0-flash:generateContent"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL_PATH}?key={GEMINI_API_KEY}"

# Astronomy keywords for filtering
ASTRONOMY_KEYWORDS = [
    "planet", "star", "galaxy", "black hole", "nebula", "cosmology",
    "telescope", "universe", "astronomy", "orbit", "exoplanet", "big bang"
]

def is_astronomy_question(question):
    return any(keyword in question.lower() for keyword in ASTRONOMY_KEYWORDS)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question', '')

    # Ensure the question is astronomy-related
    if not is_astronomy_question(question):
        return jsonify({
            'error': 'Please ask an astronomy-related question.'
        }), 400

    try:
        # Prepare the payload for Gemini API
        payload = {
            'contents': [
                {
                    'role': 'user',
                    'parts': [
                        {'text': question}
                    ]
                }
            ]
        }

        # Make request to Gemini API
        response = requests.post(GEMINI_URL, json=payload)
        response.raise_for_status()
        response_data = response.json()

        # Extract the answer from the response
        if (response_data and 
            response_data.get('candidates') and 
            response_data['candidates'][0].get('content') and 
            response_data['candidates'][0]['content'].get('parts')):
            answer = response_data['candidates'][0]['content']['parts'][0]['text']
            return jsonify({'answer': answer})
        else:
            return jsonify({'answer': 'No answer from Gemini.'})

    except requests.exceptions.RequestException as e:
        print(f"Error fetching response from Gemini API: {str(e)}")
        return jsonify({
            'error': 'Error fetching response from Gemini API.'
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 