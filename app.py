from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import re
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

# Flask setup
app = Flask(__name__)
CORS(app)  # 🚨 This enables cross-origin access from your HTML page

# Gemini API key (set in Render dashboard as environment variable)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

# Define Gemini model
model = genai.GenerativeModel('gemini-1.5-flash')

# Shembeteng core prompt
shembeteng_prompt = """
***STRICT ADHERENCE PROTOCOL: SHEMBETENG LANGUAGE ENGINE***

**PRIMARY DIRECTIVE:** Translate input using 59 Shembeteng rules with total accuracy. NEVER deviate.

**KEY RULES:**

I. INSERT FORMULA:
  * a → ambata
  * e → embete
  * i → imbiti
  * o → omboto
  * u → umbutu

II. INSERTION PLACEMENT:
  * Insert at the **Phonetic Emphasis (PE)** point (stressed vowel).
  * PE for French = always last vowel of the word.

III. STRUCTURE RULE:
  * DO NOT add/remove letters.
  * All original letters must be retained around inserted pattern.

IV. MULTI-WORD INPUTS:
  * Treat each word individually, unless part of compound.

RESPONSE FORMAT:
Explain clearly the PE used per word, then end with:

Final Shembeteng Translation: **[translated string here]**

Translate this: 
"""

def translate_shembeteng(text):
    full_prompt = f"{shembeteng_prompt}\n{text}"
    response = model.generate_content(full_prompt)
    return response.text

@app.route('/')
def home():
    return "Shembeteng API is live! Use /translate"

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing input text.'}), 400

    user_text = data['text']
    try:
        raw_output = translate_shembeteng(user_text)
        match = re.search(r'Final Shembeteng Translation:\s*\*\*([^\*]+)\*\*', raw_output)
        translation = match.group(1).strip() if match else "Translation not found."

        return jsonify({
            'translation': translation,
            'original_language': detect(user_text)
        })
    except Exception as e:
        return jsonify({'error': f'Failed to translate: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
