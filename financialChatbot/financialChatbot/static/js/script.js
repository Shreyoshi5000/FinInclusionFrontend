document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const languageSelect = document.getElementById('language-select');
    const suggestionChips = document.querySelectorAll('.chip');
    
    let currentLanguage = 'english';
    let currentlyPlayingButton = null;
    
    // Language mapping for speech synthesis
    const languages = {
        'english': { voice: 'en-US' },
        'hindi': { voice: 'hi-IN' },
        'tamil': { voice: 'ta-IN' },
        'telugu': { voice: 'te-IN' },
        'bengali': { voice: 'bn-IN' },
        'marathi': { voice: 'mr-IN' },
        'gujarati': { voice: 'gu-IN' },
        'kannada': { voice: 'kn-IN' },
        'malayalam': { voice: 'ml-IN' },
        'punjabi': { voice: 'pa-IN' }
    };
    
    // Load voices when they're available
    let voices = [];
    function loadVoices() {
        voices = speechSynthesis.getVoices();
    }
    
    if (speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = loadVoices;
    }
    loadVoices();
    
    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    languageSelect.addEventListener('change', (e) => {
        currentLanguage = e.target.value;
        translateBotMessages();
    });
    
    suggestionChips.forEach(chip => {
        chip.addEventListener('click', () => {
            userInput.value = chip.dataset.query;
            sendMessage();
        });
    });
    
    // Add event listener for initial speak button
    document.querySelectorAll('.speak-button').forEach(button => {
        button.addEventListener('click', handleSpeakButtonClick);
    });
    
    // Function to handle speak button click
    function handleSpeakButtonClick(e) {
        const button = e.currentTarget;
        const messageContent = button.closest('.message-content');
        const textToSpeak = messageContent.textContent.trim();
        
        // Get text to speak (excluding the button text)
        const cleanText = textToSpeak.replace(/Listen to this response/g, '').trim();
        
        // Speak the text
        speakText(cleanText, button);
    }
    
    // Function to speak text using Web Speech API
    function speakText(text, button) {
        if ('speechSynthesis' in window) {
            // Stop any ongoing speech
            speechSynthesis.cancel();
            
            if (currentlyPlayingButton) {
                currentlyPlayingButton.classList.remove('speaking');
                currentlyPlayingButton = null;
            }
            
            // If the same button was clicked while speaking, just stop playback
            if (currentlyPlayingButton === button) {
                return;
            }
            
            const utterance = new SpeechSynthesisUtterance(text);
            const lang = languages[currentLanguage];
            
            // Set language and voice
            utterance.lang = lang.voice;
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 1;
            
            // Find appropriate voice
            const voices = speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.lang.startsWith(currentLanguage) || 
                voice.lang.startsWith(lang.voice)
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            // Update button state
            button.classList.add('speaking');
            currentlyPlayingButton = button;
            
            utterance.onend = () => {
                button.classList.remove('speaking');
                currentlyPlayingButton = null;
            };
            
            utterance.onerror = () => {
                button.classList.remove('speaking');
                currentlyPlayingButton = null;
            };
            
            speechSynthesis.speak(utterance);
        } else {
            alert('Speech synthesis is not supported in this browser.');
        }
    }
    
    // Function to send user message
    function sendMessage() {
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input field
        userInput.value = '';
        
        // Show typing indicator
        showTypingIndicator();
        
        // Send message to server
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                language: currentLanguage
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add bot response to chat
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            addMessage('Sorry, there was an error processing your request. Please try again.', 'bot');
        });
    }
    
    // Function to add message to chat
    function addMessage(message, sender) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        const messageContent = document.createElement('div');
        messageContent.classList.add('message-content');
        messageContent.textContent = message;
        
        // Add speak button for bot messages
        if (sender === 'bot') {
            const speakButton = document.createElement('button');
            speakButton.classList.add('speak-button');
            speakButton.title = 'Listen to this response';
            speakButton.innerHTML = '<i class="fas fa-volume-up"></i>';
            speakButton.addEventListener('click', handleSpeakButtonClick);
            messageContent.appendChild(speakButton);
        }
        
        messageElement.appendChild(messageContent);
        chatMessages.appendChild(messageElement);
        
        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingIndicator = document.createElement('div');
        typingIndicator.classList.add('message', 'bot-message', 'typing-indicator-container');
        
        const indicatorContent = document.createElement('div');
        indicatorContent.classList.add('typing-indicator');
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            indicatorContent.appendChild(dot);
        }
        
        typingIndicator.appendChild(indicatorContent);
        chatMessages.appendChild(typingIndicator);
        
        // Scroll to bottom of chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingIndicator = document.querySelector('.typing-indicator-container');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    // Function to translate bot messages when language changes
    function translateBotMessages() {
        const botMessages = document.querySelectorAll('.bot-message .message-content');
        const initialMessage = "Hello! I'm your financial advisor. Ask me any financial questions you have.";
        
        // Only translate the initial greeting message
        if (botMessages.length > 0 && botMessages[0].textContent.includes(initialMessage) && currentLanguage !== 'english') {
            showTypingIndicator();
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: initialMessage,
                    language: currentLanguage
                })
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                // Update text content but preserve the button
                const firstMessage = botMessages[0];
                const speakButton = firstMessage.querySelector('.speak-button');
                firstMessage.textContent = data.response;
                if (speakButton) {
                    firstMessage.appendChild(speakButton);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                removeTypingIndicator();
            });
        }
    }
});
