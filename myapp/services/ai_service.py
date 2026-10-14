import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from django.conf import settings

# Ensure environment variables are loaded from the exact .env path
dotenv_path = os.path.join(settings.BASE_DIR, '.env')
load_dotenv(dotenv_path)

SYSTEM_INSTRUCTION = """
You are the FarmLink AI Agricultural Assistant.

Your purpose is to help visitors understand the FarmLink ERP system and provide general agricultural information.

For FarmLink-related questions:
- Explain only actual FarmLink functionality.
- Do not invent features.
- Explain FarmLink in simple language.
- Explain the roles of Admin, Farmer, Customer, Worker, and Delivery Person.
- Explain marketplace functionality, product selling, and bidding.
- A farmer cannot bid on their own product.
- Explain Farmer-to-Farmer purchasing.
- Explain Farm supplies.
- Explain worker requests (farmers request, admin assigns).
- Explain delivery workflow: ASSIGNED -> PICKED_UP -> OUT_FOR_DELIVERY -> DELIVERED -> COMPLETED. The receiver confirms final delivery, not the delivery person.
- Explain the 80/20 sale commission when relevant.

For agriculture-related questions:
- Answer questions about crops, seeds, fertilizers, NPK, soil, irrigation, pests, diseases, weed management, organic farming, crop management, harvesting, and general farm management.

If a question is both about FarmLink and agriculture, answer both aspects.
If the visitor asks something unrelated, politely explain that the assistant is mainly designed for FarmLink and agricultural questions.

Never invent FarmLink functionality.
Never invent FarmLink prices, transactions, users, wallet information, or database information.
Never reveal passwords, API keys, private user information, or confidential database information.
"""

import time

def get_ai_response(user_message, history=None):
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY" or api_key == "":
        return "Configuration error: The Gemini API key is missing or invalid. Please configure it in the .env file."
        
    client = genai.Client(api_key=api_key)
    
    history_msgs = []
    if history:
        for msg in history:
            role = "user" if msg["role"] == "user" else "model"
            history_msgs.append(
                types.Content(role=role, parts=[types.Part.from_text(text=msg["content"])])
            )
            
    max_retries = 3
    for attempt in range(max_retries + 1):
        try:
            chat = client.chats.create(
                model="gemini-3.8-flash",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                ),
                history=history_msgs
            )
            
            response = chat.send_message(user_message)
            return response.text
            
        except Exception as e:
            error_msg = str(e).lower()
            
            # Check for permanent client errors (auth, missing model, invalid request, 400-499 except 429)
            is_permanent = False
            if "api_key" in error_msg or "auth" in error_msg or "unauthorized" in error_msg or "403" in error_msg or "401" in error_msg:
                is_permanent = True
            elif "400" in error_msg or "404" in error_msg or "invalid" in error_msg or "not_found" in error_msg:
                is_permanent = True
                
            if is_permanent:
                print(f"AI Service Permanent Error: Type: {type(e).__name__}, Error: {e}")
                if "403" in error_msg or "401" in error_msg or "auth" in error_msg:
                    return "Sorry, the AI service could not be authenticated. Please check the Gemini API configuration."
                return "Sorry, I couldn't process your question right now. Please try again."
                
            # If temporary error (503, 429, 5xx) and we have retries left
            if attempt < max_retries:
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                print(f"AI Service Temporary Error (e.g. 503/429). Retrying in {wait_time}s (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
            else:
                print(f"AI Service Max Retries Reached. Last Error: Type: {type(e).__name__}, Error: {e}")
                return "Sorry, I couldn't process your question right now. Please try again."
