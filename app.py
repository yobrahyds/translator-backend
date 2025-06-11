from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
import re
from langdetect import detect, DetectorFactory

# Ensure consistent language detection
DetectorFactory.seed = 0

app = Flask(__name__)
CORS(app)

# Configure Gemini API
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# 🧠 FULL Shembeteng Rule Prompt
shembeteng_prompt = """
***STRICT ADHERENCE PROTOCOL: SHEMBETENG LANGUAGE ENGINE***

PRIMARY DIRECTIVE: Use all 59 Shembeteng rules exactly. NEVER deviate. If unsure, Shembetengify by flow.

--- INSERT FORMULA ---
a → ambata
e → embete
i → imbiti
o → omboto
u → umbutu

--- PHONETIC EMPHASIS (PE) ---
Insert pattern at PE point (last vowel for French; stress for others).
DO NOT remove original letters. Maintain original root structure.

--- FOUNDATIONAL (15) ---
1. Keep root meaning. 2. Drop final vowel if any. 3. Add “sh” to start of slangified words.
4. Reverse short words. 5. Insert “mb” for rhythm. 6. Repeat syllables in verbs.
7. r ↔ l swap allowed. 8. Replace “s” with “z”. 9. ch → sh unless it ruins flow.
10. Contract compounds. 11. Use numbers (e.g., 4 = for). 12. Rhythm over spelling.
13. Create rhyme. 14. Shrink adjectives. 15. Idioms = new creations.

--- VERBS (7) ---
1. Verbs must bounce: add -eng, -ish, -o. 2. Double action verbs. 3. Reduplication = style.
4. “ku-” → “sh-”. 5. Create suffixes: -ify, -olize. 6. Make up verbs if needed. 7. Match tense to vibe.

--- NOUNS (8) ---
1. Break down compounds. 2. Brutally shorten. 3. Swagify names (e.g., Nairobi → Nai-beng).
4. “mb” replaces “m” or “b”. 5. Use sound-words. 6. Alienize names. 7. Fuse numbers. 8. Flip dull nouns.

--- PRONOUNS (5) ---
1. “I” → “me” or “mi”. 2. “they” → “deyy”, “him” → “heem”. 3. No passive structure. 4. Use street form. 5. Subject always dominates.

--- PREPOSITIONS / CONJUNCTIONS (5) ---
1. “And” → “na”, “n”, “en”. 2. “With” → “shwi” or “whif”. 3. “Of” → drop or “o”. 4. Drop “a”/“the” if off-beat. 5. Fuse prepositions to verbs.

--- STYLISTIC (7) ---
1. Slang > grammar. 2. Inspired by African languages. 3. Dirty > clean. 4. Use “z” for strength.
5. Break rules for flow. 6. Repeat endings. 7. Rhyme > syntax.

--- CULTURAL (5) ---
1. Nairobi slang is canon. 2. Blend Swahili, English, Sheng. 3. Tribe tones matter.
4. Use rebellion slang. 5. Rap = grammar.

--- PHONETIC (4) ---
1. Consonants > vowels. 2. Use glottal stops. 3. Drop soft ends. 4. Use tone markers.

--- CREATIVE (3) ---
1. Break rules if doper. 2. If it sounds sick, it’s valid. 3. Every sentence should slap.

---

Format like this per input:
1. Explain PE placement per word
2. Apply correct insertions
3. Follow all rules above
4. End clearly with:

Final Shembeteng Translation: **[final translation]**

Translate this:
"""

def translate_shembeteng(text):
    prompt = f"{shembeteng_prompt}\n{text}"
    response = model.generate_content(prompt)
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
