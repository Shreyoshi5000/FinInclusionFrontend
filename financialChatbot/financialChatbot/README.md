# Financial Chatbot

A multilingual financial chatbot that helps individuals with basic financial questions. The chatbot supports multiple Indian languages, allowing users to interact in their native language.

## Features

- Answer basic financial questions using Llama-70B LLM via Groq API
- Support for multiple Indian languages
- Text-to-speech functionality with speaker buttons
- Simple and intuitive user interface
- Real-time language translation

## Setup and Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up your Groq API key:
   - Sign up for an account at [Groq](https://console.groq.com/)
   - Get your API key from the Groq console
   - Edit the `.env` file and replace `your_groq_api_key_here` with your actual API key
   ```
   GROQ_API_KEY=your_actual_api_key_here
   ```

4. Run the application:
   ```
   python app.py
   ```
5. Open your browser and navigate to `http://localhost:5000`

## Using the Chatbot

1. **Select your language**: Choose from 10 supported Indian languages using the dropdown menu
2. **Ask financial questions**: Type your question in the input box and click "Send"
3. **Use suggestion chips**: Click on the suggestion chips for quick access to common questions
4. **Listen to responses**: Click the speaker button next to any response to hear it spoken aloud

## Supported Languages

- English
- Hindi
- Tamil
- Telugu
- Bengali
- Marathi
- Gujarati
- Kannada
- Malayalam
- Punjabi

## Project Structure

- `app.py`: Main Flask application
- `static/`: Contains CSS, JS, and other static files
- `templates/`: HTML templates
- `chatbot/`: Chatbot implementation
- `data/`: Financial knowledge base and language resources
- `.env`: Environment variables including API keys

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **LLM**: Llama-70B via Groq API
- **Text-to-Speech**: gTTS (Google Text-to-Speech)
- **Language Support**: Pre-translated content with basic term mapping
