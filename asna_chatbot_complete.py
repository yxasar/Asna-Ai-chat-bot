
"""
AI Chatbot "Asna" - Multiple Implementation Examples
This file demonstrates different approaches to building an AI chatbot named "Asna"
"""

# ========================================
# Approach 1: Simple Rule-Based Chatbot with NLTK
# ========================================

import re
import random
from datetime import datetime
import os
import google.generativeai as genai


# Set your Gemini API key
genai.configure(api_key="####################")
MODEL = genai.GenerativeModel("models/gemini-1.5-flash")



# Initialize Gemini client


def get_gemini_response(user_input):
    model = genai.GenerativeModel("models/gemini-1.5-flash")

    response = model.generate_content(user_input)
    return response.text

class SimpleAsna:
    """Simple rule-based chatbot using pattern matching"""

    def __init__(self):
        self.name = "Asna"
        self.patterns = {
            'greeting': [
                r'hi|hello|hey|good morning|good afternoon|good evening',
                [f"Hello! I'm {self.name}, your AI assistant. How can I help you today?",
                 f"Hi there! {self.name} here. What can I do for you?",
                 f"Hey! I'm {self.name}. How are you doing?"]
            ],
            'name_question': [
                r'what.*your name|who are you|what should i call you',
                [f"I'm {self.name}, your friendly AI chatbot!",
                 f"My name is {self.name}. Nice to meet you!"]
            ],
            'how_are_you': [
                r'how are you|how.*doing',
                ["I'm doing great, thanks for asking! How about you?",
                 "I'm fine, thank you! How can I assist you today?"]
            ],
            'goodbye': [
                r'bye|goodbye|see you|farewell|talk to you later',
                ["Goodbye! Have a great day!",
                 "See you later! Take care!",
                 "Bye! Feel free to chat with me anytime!"]
            ],
            'help': [
                r'help|what can you do|capabilities',
                [f"I'm {self.name} and I can help you with basic conversations. Try asking me about my name, how I'm doing, or just say hello!",
                 "I can chat with you, answer simple questions, and provide basic assistance. What would you like to know?"]
            ]
        }

    def get_response(self, user_input):
        """Get response based on pattern matching"""
        user_input = user_input.lower().strip()

        for intent, (pattern, responses) in self.patterns.items():
            if re.search(pattern, user_input):
                return random.choice(responses)

        # Default response
        return "I'm still learning! Could you rephrase that or ask me something else?"

# ========================================
# Approach 2: OpenAI GPT API Integration
# ========================================

class GeminiAsna:
    """Chatbot using Gemini AI API, always responds as Asna"""

    def __init__(self):
        self.name = "Asna"
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")


    def get_response(self, user_input):
        try:
            # Tell Gemini that it is Asna
            prompt = (
                f"You are {self.name}, a friendly and helpful AI assistant. "
                f"Always introduce yourself as {self.name} and answer conversationally.\n"
                f"User: {user_input}\n"
                f"{self.name}:"
            )
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"


# ========================================
# Approach 3: Flask Web Interface
# ========================================

class FlaskAsnaChatbot:
    """Flask web application for Asna chatbot"""

    def __init__(self, chatbot_engine):
        self.chatbot = chatbot_engine

    def create_app(self):
        """Create Flask application"""
        from flask import Flask, render_template_string, request, jsonify

        app = Flask(__name__)

        # HTML template
        template = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>asna.ai</title>
            <style>
                body { font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #000; color: #fff; }
                .chat-container { border: 1px solid #ddd; height: 400px; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background-color: #111; }
                .message { margin: 10px 0; }
                .user { text-align: right; color: #0af;; }
                .asna { text-align: left; color: #0f0; }
                input[type="text"] { width: 80%; padding: 10px;background-color: #222; color: #fff; border: 1px solid #555; }
                button { padding: 10px 20px; background-color: #333; color: #fff; border: 1px solid #555; cursor: pointer;}
            </style>
        </head>
        <body>
            <h1>Asna.ai </h1>
            <div class="chat-container" id="chatContainer">
                <div class="message asna"><strong>Asna:</strong> Hi! I'm Asna, your AI assistant. How can I help you today?</div>
            </div>
            <div>
                <input type="text" id="userInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>

            <script>
                function sendMessage() {
                    const input = document.getElementById('userInput');
                    const message = input.value.trim();
                    if (!message) return;

                    // Add user message
                    addMessage('You: ' + message, 'user');
                    input.value = '';

                    // Send to server
                    fetch('/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: message })
                    })
                    .then(response => response.json())
                    .then(data => {
                        addMessage('Asna: ' + data.response, 'asna');
                    });
                }

                function addMessage(text, className) {
                    const container = document.getElementById('chatContainer');
                    const div = document.createElement('div');
                    div.className = 'message ' + className;
                    div.innerHTML = '<strong>' + text + '</strong>';
                    container.appendChild(div);
                    container.scrollTop = container.scrollHeight;
                }

                function handleKeyPress(event) {
                    if (event.key === 'Enter') {
                        sendMessage();
                    }
                }
            </script>
        </body>
        </html>
        """

        @app.route('/')
        def home():
            return render_template_string(template)

        @app.route('/chat', methods=['POST'])
        def chat():
            user_message = request.json.get('message', '')
            response = self.chatbot.get_response(user_message)
            return jsonify({'response': response})

        return app

# ========================================
# Usage Examples
# ========================================

def demo_simple_asna():
    """Demonstrate simple rule-based Asna"""
    print("=== Simple Asna Demo ===")
    asna = SimpleAsna()

    test_inputs = [
        "Hello!",
        "What's your name?",
        "How are you doing?",
        "Can you help me?",
        "What's the weather like?",
        "Goodbye!"
    ]

    for user_input in test_inputs:
        response = asna.get_response(user_input)
        print(f"User: {user_input}")
        print(f"Asna: {response}\n")

def run_console_chatbot():
    """Run interactive console version"""
    print("=== Console Chat with Asna ===")
    print("Type 'quit' to exit")

    asna = SimpleAsna()

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("Asna: Goodbye! Have a great day!")
            break

        response = asna.get_response(user_input)
        print(f"Asna: {response}")

def run_flask_app():
    """Run Flask web application"""
    from threading import Timer
    import webbrowser

    print("Starting Gemini-powered Asna...")
    chatbot_engine = GeminiAsna()

    # Create Flask app
    flask_app = FlaskAsnaChatbot(chatbot_engine)
    app = flask_app.create_app()

    # Only open browser in the main process
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()

    # Explicitly bind to localhost
    app.run(host="localhost", port=5000, debug=True)


    

# ========================================
# Installation and Setup Guide
# ========================================

def print_setup_guide():
    """Print setup instructions"""
    print("""
    === Setup Guide for Asna Chatbot ===

    1. Basic Requirements:
       pip install flask
       pip install openai  # For GPT integration

    2. For Simple Rule-Based Chatbot:
       - No additional setup required
       - Run demo_simple_asna() to test

    3. For OpenAI GPT Integration:
       - Get OpenAI API key from https://openai.com
       - Set environment variable: OPENAI_API_KEY=your_key_here
       - Or pass directly to GPTAsna(api_key="your_key")

    4. For Flask Web Interface:
       - Run run_flask_app() 
       - Open browser to http://localhost:5000

    5. File Structure:
       asna_chatbot/
       ├── asna.py (this file)
       ├── requirements.txt
       └── templates/ (if using separate HTML files)
    """)

if __name__ == "__main__":
    print("Starting Asna Chatbot web interface...")
    run_flask_app()

