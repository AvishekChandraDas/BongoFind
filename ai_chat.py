from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all domains during development
CORS(app, resources={
    r"/chat": {
        "origins": "*",
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Configure Gemini API
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-1.5-pro-latest')

# Enhanced system prompt
SYSTEM_PROMPT = """You are BongoFind AI, a helpful assistant for the BongoFind website. 
You help people find services and information about Sylhet, Bangladesh.

Your knowledge includes:
1. Restaurants: Panshi, Pachvai, Pach Bhai, Woondaal
2. Doctors & Hospitals: MAG Osmani Medical, Popular Medical
3. Educational Institutions: SUST, Leading University, Metropolitan University
4. Shopping: Shukria Market, City Center, Bondor Bazar
5. Property Areas: Uposhohor, Housing Estate, Tilagor
6. Tourist Spots: Ratargul, Jaflong, Lalakhal, Bisnakandi
7. Emergency Numbers: Police (999), Ambulance (999, 16263)
8. Transportation: Ena Transport, Hanif Enterprise, Osmani Airport

Keep responses friendly, concise, and specific to Sylhet. If unsure, guide users to relevant sections of the website."""

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        
        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        # Combine system prompt with user message
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {user_message}\nAssistant:"
        
        # Generate response using Gemini
        response = model.generate_content(full_prompt)
        
        print(f"User: {user_message}")
        print(f"AI: {response.text}")
        
        return jsonify({
            "response": response.text,
            "model": "gemini-pro"
        })
        
    except Exception as e:
        print(f"Error: {str(e)}")
        error_message = f"An error occurred: {str(e)}"
        return jsonify({"error": error_message}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, port=port) 
