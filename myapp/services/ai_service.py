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

Response Formatting Guidelines:
- Respond in clean, natural, readable plain text.
- Do NOT use Markdown formatting characters such as asterisks (* or **), hashtags (#, ##, ###), or decorative separators (--- or ===).
- Do NOT use bold or italic formatting syntax.
- Write headings as clean normal text on their own line followed by a blank line.
- Do NOT use bullet symbols (*, -, +). Present lists as clean, separate lines or sentences.
- When numbering steps or sequential points, use clean numbering (e.g., 1. Step name, 2. Step name) without bolding, asterisks, or dashes.
- Format responses into natural paragraphs with blank lines between different topics or sections so answers are easy to read.
- Preserve all factual accuracy, prices (e.g. ₹ or $), percentages (e.g. 20%), formulas, numbers, URLs, and email addresses in natural plain text.

Never invent FarmLink functionality.
Never invent FarmLink prices, transactions, users, wallet information, or database information.
Never reveal passwords, API keys, private user information, or confidential database information.
"""

import time
import re

def clean_ai_response(text):
    """
    Cleans and formats an AI response into readable, natural plain text:
    - Removes unnecessary Markdown symbols (*, **, #, ##, ###, --, etc.)
    - Removes Markdown heading syntax while preserving headings as normal text
    - Converts Markdown bullet lists (*, -, +, --) into clean lines without bullet symbols
    - Normalizes numbered lists into clean, readable steps
    - Removes code block fences while preserving code content
    - Converts Markdown link/image syntax while preserving useful link text and URLs
    - Preserves numbers, math, prices (₹, $), percentages, email addresses, and URLs
    - Ensures paragraphs and topics are cleanly separated without collapsing into one long line
    """
    if not text or not isinstance(text, str):
        return ""

    # Normalize line endings
    t = text.replace('\r\n', '\n').replace('\r', '\n')

    # Remove code block fences while preserving the code content inside
    t = re.sub(r'^[ \t]*```[a-zA-Z0-9_\-+]*[ \t]*\n', '', t, flags=re.MULTILINE)
    t = re.sub(r'\n[ \t]*```[ \t]*$', '', t, flags=re.MULTILINE)
    t = re.sub(r'^[ \t]*```[ \t]*$', '', t, flags=re.MULTILINE)

    # Remove horizontal rules and decorative dividers (---, ***, ___, ===, - - -, etc.)
    t = re.sub(r'^[ \t]*([*_\-=])[ \t]*(?:\1[ \t]*){2,}[ \t]*$', '', t, flags=re.MULTILINE)

    # Convert Markdown images: ![alt](url) -> alt (or remove if empty)
    t = re.sub(r'!\[([^\]]*)\]\([^)]+\)', r'\1', t)

    # Convert Markdown links: [label](url) -> label (url) or url
    def _clean_link(match):
        label = match.group(1).strip()
        url = match.group(2).strip()
        if not label or label == url:
            return url
        if url.startswith('#'):
            return label
        return f"{label} ({url})"

    t = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', _clean_link, t)

    # Remove Markdown blockquotes (> quote)
    t = re.sub(r'^[ \t]*>[ \t]?', '', t, flags=re.MULTILINE)

    # Process line-by-line: headings, standalone bold titles, bullets, numbered lists
    lines = t.split('\n')
    cleaned_lines = []

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Markdown headings: # Heading, ## Heading, ### Heading, etc.
        heading_match = re.match(r'^#{1,6}\s+(.*?)(?:\s+#+)?$', stripped)
        if heading_match:
            heading_text = heading_match.group(1).strip()
            # Ensure blank line before heading if preceding line has content
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
            cleaned_lines.append(heading_text)
            # Ensure blank line after heading if following line has content
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                cleaned_lines.append('')
            continue

        # Check for standalone bold line acting as a heading: **Heading Title** or **Heading Title:**
        bold_heading_match = re.match(r'^\*{2}([^*\n]+?)\*{2}:?$', stripped)
        if bold_heading_match:
            content = bold_heading_match.group(1).strip()
            if stripped.endswith(':'):
                content += ':'
            if cleaned_lines and cleaned_lines[-1] != '':
                cleaned_lines.append('')
            cleaned_lines.append(content)
            if i + 1 < len(lines) and lines[i + 1].strip() != '':
                cleaned_lines.append('')
            continue

        # Bullet lists: lines starting with *, -, +, --, or ---
        bullet_match = re.match(r'^(?:[ \t]*)(?:[-*+]|-{2,3})[ \t]+(.*)$', line)
        if bullet_match:
            item_text = bullet_match.group(1).strip()
            cleaned_lines.append(item_text)
            continue

        # Numbered lists: 1. Item or 1) Item
        numbered_match = re.match(r'^(?:[ \t]*)(\d+)[.)][ \t]+(.*)$', line)
        if numbered_match:
            num = numbered_match.group(1)
            rest = numbered_match.group(2).strip()
            # Remove redundant bullet if present after number like '1. - item'
            rest = re.sub(r'^(?:[-*+]|-{2,3})[ \t]+', '', rest)
            cleaned_lines.append(f"{num}. {rest}")
            continue

        cleaned_lines.append(line.rstrip())

    t = '\n'.join(cleaned_lines)

    # Clean inline markdown symbols:
    # Bold-italic: ***text***
    t = re.sub(r'\*\*\*(?!\s)([^*\n]+?)(?<!\s)\*\*\*', r'\1', t)
    # Bold: **text**
    t = re.sub(r'\*\*(?!\s)([^*\n]+?)(?<!\s)\*\*', r'\1', t)
    # Bold with double underscores: __text__ (ensuring word boundaries)
    t = re.sub(r'(?<!\w)__(?!_)([^_\n]+?)(?<!_)__(?!\w)', r'\1', t)
    # Italic: *text* (avoiding mathematical multiplication like 5 * 10 or wildcards like *.py)
    t = re.sub(r'(?<![\w*])\*(?!\s)([^*\n]+?)(?<![\s*])\*(?![\w*])', r'\1', t)
    # Italic with underscores: _text_ (avoiding snake_case identifiers like user_id)
    t = re.sub(r'(?<!\w)_(?!_)([^_\n]+?)(?<!_)_(?!\w)', r'\1', t)
    # Strikethrough: ~~text~~
    t = re.sub(r'~~(?!\s)(.+?)(?<!\s)~~', r'\1', t)
    # Inline code backticks: `code` -> code
    t = re.sub(r'`([^`\n]+)`', r'\1', t)

    # Normalize multiple consecutive blank lines (limit to 1 blank line = 2 newlines)
    t = re.sub(r'\n{3,}', '\n\n', t)

    return t.strip()

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
            model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
            chat = client.chats.create(
                model=model_name,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                ),
                history=history_msgs
            )
            
            response = chat.send_message(user_message)
            return clean_ai_response(response.text)
            
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
