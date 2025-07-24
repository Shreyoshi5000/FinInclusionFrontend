from flask import Flask, render_template, request, jsonify, send_file
import os
import json
import sys
import tempfile
from flask_cors import CORS
from gtts import gTTS
from chatbot.financial_bot import FinancialChatbot

app = Flask(__name__)
CORS(app)
chatbot = FinancialChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    language = data.get('language', 'english')
    
    response = chatbot.get_response(user_message, language)
    
    return jsonify({
        'response': response
    })

@app.route('/supported_languages')
def supported_languages():
    return jsonify({
        'languages': chatbot.get_supported_languages()
    })

@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', 'en')
    
    # Map our language codes to gTTS language codes
    language_map = {
        'english': 'en',
        'hindi': 'hi',
        'tamil': 'ta',
        'telugu': 'te',
        'bengali': 'bn',
        'marathi': 'mr',
        'gujarati': 'gu',
        'kannada': 'kn',
        'malayalam': 'ml',
        'punjabi': 'pa'
    }
    
    # Get the appropriate language code
    lang_code = language_map.get(language.lower(), 'en')
    
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
    temp_filename = temp_file.name
    temp_file.close()
    
    # Generate the speech file
    try:
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(temp_filename)
        
        # Return the audio file
        return send_file(
            temp_filename,
            mimetype="audio/mp3",
            as_attachment=True,
            download_name="speech.mp3"
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        # Schedule the file for deletion (will be deleted after response is sent)
        @app.after_request
        def remove_file(response):
            try:
                if os.path.exists(temp_filename):
                    os.unlink(temp_filename)
            except Exception as e:
                app.logger.error(f"Error removing temporary file: {e}")
            return response

if __name__ == '__main__':
    app.run(debug=True)
