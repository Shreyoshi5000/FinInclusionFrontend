import json
import os
import re
import groq
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class FinancialChatbot:
    def __init__(self):
        self.knowledge_base = self._load_knowledge_base()
        self.language_greetings = {
            'english': "Hello! I'm your financial advisor. Ask me any financial questions you have.",
            'hindi': "नमस्ते! मैं आपका वित्तीय सलाहकार हूं। आपके पास कोई भी वित्तीय प्रश्न हों, मुझसे पूछें।",
            'tamil': "வணக்கம்! நான் உங்கள் நிதி ஆலோசகர். உங்களிடம் ஏதேனும் நிதி கேள்விகள் இருந்தால் என்னிடம் கேளுங்கள்.",
            'telugu': "హలో! నేను మీ ఆర్థిక సలహాదారుని. మీకు ఏవైనా ఆర్థిక ప్రశ్నలు ఉంటే నన్ను అడగండి.",
            'bengali': "হ্যালো! আমি আপনার আর্থিক পরামর্শদাতা। আপনার কোন আর্থিক প্রশ্ন থাকলে আমাকে জিজ্ঞাসা করুন।",
            'marathi': "नमस्कार! मी तुमचा आर्थिक सल्लागार आहे. तुम्हाला कोणतेही आर्थिक प्रश्न असल्यास मला विचारा.",
            'gujarati': "નમસ્તે! હું તમારો નાણાકીય સલાહકાર છું. તમારી પાસે કોઈ નાણાકીય પ્રશ્નો હોય તો મને પૂછો.",
            'kannada': "ಹಲೋ! ನಾನು ನಿಮ್ಮ ಹಣಕಾಸು ಸಲಹೆಗಾರ. ನಿಮಗೆ ಯಾವುದೇ ಹಣಕಾಸು ಪ್ರಶ್ನೆಗಳಿದ್ದರೆ ನನ್ನನ್ನು ಕೇಳಿ.",
            'malayalam': "ഹലോ! ഞാൻ നിങ്ങളുടെ ധനകാര്യ ഉപദേഷ്ടാവാണ്. നിങ്ങൾക്ക് എന്തെങ്കിലും സാമ്പത്തിക ചോദ്യങ്ങളുണ്ടെങ്കിൽ എന്നോട് ചോദിക്കൂ.",
            'punjabi': "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਮੈਂ ਤੁਹਾਡਾ ਵਿੱਤੀ ਸਲਾਹਕਾਰ ਹਾਂ। ਜੇ ਤੁਹਾਡੇ ਕੋਲ ਕੋਈ ਵਿੱਤੀ ਸਵਾਲ ਹਨ ਤਾਂ ਮੈਨੂੰ ਪੁੱਛੋ।"
        }
        
        # Common financial terms in different languages
        self.language_responses = {
            'hindi': {
                'savings': 'बचत',
                'investment': 'निवेश',
                'tax': 'कर',
                'loans': 'ऋण',
                'insurance': 'बीमा',
                'sorry': 'क्षमा करें, मेरे पास इस विशिष्ट वित्तीय विषय पर जानकारी नहीं है। कृपया बचत, निवेश, कर, ऋण या बीमा के बारे में पूछने का प्रयास करें।'
            },
            'tamil': {
                'savings': 'சேமிப்பு',
                'investment': 'முதலீடு',
                'tax': 'வரி',
                'loans': 'கடன்கள்',
                'insurance': 'காப்பீடு',
                'sorry': 'மன்னிக்கவும், எனக்கு இந்த குறிப்பிட்ட நிதி தலைப்பைப் பற்றிய தகவல் இல்லை. சேமிப்பு, முதலீடு, வரி, கடன்கள் அல்லது காப்பீடு பற்றி கேட்க முயற்சிக்கவும்.'
            }
        }
        
        # Initialize Groq client if API key is available
        groq_api_key = os.getenv("GROQ_API_KEY")
        self.groq_client = None
        if groq_api_key:
            self.groq_client = groq.Client(api_key=groq_api_key)
        else:
            print("Warning: GROQ_API_KEY not found in environment variables. Falling back to local responses.")
    
    def _load_knowledge_base(self):
        """Load the financial knowledge base from a JSON file or create a default one if it doesn't exist"""
        knowledge_base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'knowledge_base.json')
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(knowledge_base_path), exist_ok=True)
        
        # Check if knowledge base exists, if not create a default one
        if not os.path.exists(knowledge_base_path):
            default_knowledge_base = {
                "savings": {
                    "what is savings account": "A savings account is a basic type of bank account that allows you to deposit money, keep it safe, and withdraw funds, all while earning interest.",
                    "how to save money": "To save money: create a budget, reduce unnecessary expenses, set up automatic transfers to savings, pay off high-interest debt first, and look for additional income sources.",
                    "best savings schemes in india": "Popular savings schemes in India include Public Provident Fund (PPF), National Savings Certificate (NSC), Sukanya Samriddhi Yojana, Senior Citizens Savings Scheme, and bank Fixed Deposits."
                },
                "investment": {
                    "what is mutual fund": "A mutual fund is an investment vehicle that pools money from many investors to purchase securities like stocks and bonds, managed by professional fund managers.",
                    "how to start investing": "To start investing: set financial goals, build an emergency fund, understand your risk tolerance, research investment options, start with small amounts, and consider consulting a financial advisor.",
                    "best investment options in india": "Popular investment options in India include Equity Mutual Funds, Public Provident Fund, National Pension Scheme, Fixed Deposits, Real Estate, Gold, and Direct Equity investments."
                },
                "tax": {
                    "how to save tax in india": "Ways to save tax in India include investing in tax-saving instruments like PPF, ELSS, NSC, paying life insurance premiums, contributing to NPS, claiming HRA, home loan benefits, and medical insurance premiums.",
                    "what is income tax": "Income tax is a direct tax imposed by the government on income earned by individuals and businesses during a financial year.",
                    "tax slabs in india": "As of 2023, India has two tax regimes: Old regime with rates from 5% to 30% based on income slabs with deductions available, and New regime with lower rates but fewer deductions."
                },
                "loans": {
                    "how to get home loan": "To get a home loan: check your eligibility, compare lenders, prepare documents (ID proof, income proof, property documents), apply, undergo property valuation, and wait for approval and disbursement.",
                    "what is personal loan": "A personal loan is an unsecured loan provided by banks or financial institutions that can be used for any personal expenses like medical emergencies, home renovation, travel, or debt consolidation.",
                    "how to improve credit score": "To improve credit score: pay bills on time, reduce credit utilization ratio, don't close old credit accounts, limit new credit applications, regularly check your credit report, and dispute errors if any."
                },
                "insurance": {
                    "what is term insurance": "Term insurance is a pure life insurance product that provides financial coverage for a specified term. If the insured dies during the policy term, the nominee receives the death benefit.",
                    "how to choose health insurance": "Choose health insurance by considering coverage amount, network hospitals, waiting periods, sub-limits, co-payment clauses, claim settlement ratio, premium costs, and additional benefits.",
                    "types of insurance in india": "Common types of insurance in India include Life Insurance, Health Insurance, Motor Insurance, Travel Insurance, Home Insurance, and Critical Illness Insurance."
                },
                "general": {
                    "what is inflation": "Inflation is the rate at which the general level of prices for goods and services rises, causing purchasing power to fall.",
                    "how to make a budget": "To make a budget: calculate your monthly income, track expenses, categorize spending, set financial goals, allocate funds to categories, and review and adjust regularly.",
                    "what is financial planning": "Financial planning is the process of setting financial goals, creating a plan to achieve them, and regularly reviewing and adjusting the plan as needed."
                }
            }
            
            with open(knowledge_base_path, 'w', encoding='utf-8') as f:
                json.dump(default_knowledge_base, f, indent=4)
            
            return default_knowledge_base
        
        # Load existing knowledge base
        try:
            with open(knowledge_base_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge base: {e}")
            return {}
    
    def get_supported_languages(self):
        """Return a list of supported languages"""
        return list(self.language_greetings.keys())
    
    def _get_greeting(self, language):
        """Get greeting in the specified language"""
        return self.language_greetings.get(language.lower(), self.language_greetings['english'])
    
    def _find_best_match(self, user_query):
        """Find the best matching response from the knowledge base"""
        user_query = user_query.lower().strip()
        
        # Check for exact matches first
        for category, qa_pairs in self.knowledge_base.items():
            if user_query in qa_pairs:
                return qa_pairs[user_query]
        
        # If no exact match, look for the best partial match
        best_match = None
        highest_score = 0
        
        for category, qa_pairs in self.knowledge_base.items():
            for question, answer in qa_pairs.items():
                # Simple word matching algorithm
                query_words = set(re.findall(r'\w+', user_query))
                question_words = set(re.findall(r'\w+', question))
                
                # Calculate overlap score
                common_words = query_words.intersection(question_words)
                if not common_words:
                    continue
                
                score = len(common_words) / max(len(query_words), len(question_words))
                
                if score > highest_score:
                    highest_score = score
                    best_match = answer
        
        # Return the best match if score is above threshold, otherwise return a default message
        if highest_score > 0.3:
            return best_match
        else:
            return "I'm sorry, I don't have information on that specific financial topic. Please try asking about savings, investments, taxes, loans, or insurance."
    
    def _get_llm_response(self, query, context=None):
        """Get a response from the Llama-70B model via Groq API"""
        if not self.groq_client:
            return None
            
        try:
            # Prepare context from our knowledge base if available
            if not context:
                # Find relevant information from knowledge base
                best_match = self._find_best_match(query)
                context = best_match if best_match else "You are a helpful financial advisor."
                
            # Prepare the prompt
            prompt = f"""You are a helpful financial advisor assistant. 
            Answer the following financial question concisely and accurately.
            
            Context information: {context}
            
            Question: {query}
            
            Answer:"""
            
            # Call the Groq API with Llama-70B model
            completion = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "You are a helpful financial advisor. Provide accurate and concise answers to financial questions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.5
            )
            
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error calling Groq API: {e}")
            return None
    
    def get_response(self, user_message, language='english'):
        """Process user message and return a response"""
        # Special case for greeting
        if user_message.lower() in ["hello", "hi", "greetings", "namaste"]:
            return self._get_greeting(language)
        
        # Try to get response from LLM first
        llm_response = self._get_llm_response(user_message)
        
        if llm_response:
            # If we have an LLM response, use it
            response = llm_response
        else:
            # Fall back to our knowledge base
            response = self._find_best_match(user_message)
        
        # If we have some basic translations for common terms, use them
        if language.lower() != 'english' and language.lower() in self.language_responses:
            for eng_term, translated_term in self.language_responses[language.lower()].items():
                if eng_term in response.lower():
                    # This is a very basic replacement and won't work well for complex sentences
                    # A proper translation API would be better
                    response = response.replace(eng_term, translated_term)
                    
        return response
