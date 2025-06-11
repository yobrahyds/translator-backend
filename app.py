from flask import Flask, request, jsonify from flask_cors import CORS import google.generativeai as genai import os import re from langdetect import detect, DetectorFactory

Ensure consistent language detection

DetectorFactory.seed = 0

Flask setup

app = Flask(name) CORS(app)  # 🚨 This enables cross-origin access from your HTML page

Gemini API key (set in Render dashboard as environment variable)

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") genai.configure(api_key=GEMINI_API_KEY)

Define Gemini model

model = genai.GenerativeModel('gemini-1.5-flash')

Full Shembeteng 59 rules prompt

shembeteng_prompt = """ STRICT ADHERENCE PROTOCOL: SHEMBETENG LANGUAGE ENGINE

PRIMARY DIRECTIVE: Translate input using the full 59 Shembeteng rules with absolute precision. NEVER deviate.


---

🧠 SHEMBETENG TRANSLATION RULES (ALL 59)

FOUNDATIONAL RULES

1. Keep root meaning.  2. Drop final vowels.  3. Add 'sh' prefix.  4. Reverse short words (<4 letters).  5. Insert 'mb' in longer nouns.  6. Emphasize verbs by syllable repetition.  7. Swap 'r' and 'l' if it flows better.  8. 'z' may replace 's'.  9. 'ch' becomes 'sh'. 10. Contract compound phrases.


2. Use numbers phonetically. 12. Prioritize rhythm. 13. Use rhymes. 14. Shrink long adjectives. 15. Idioms must be transformed.



VERB RULES

16. Verbs must bounce ('-eng', '-ish'). 17. Double verbs = emphasis. 18. Use reduplication ('run-run').


17. 'ku-' infinitives → drop and prefix 'sh'. 20. Invent suffixes like '-ify', '-olize'. 21. Invent verbs if needed. 22. Tense = mood driven.



NOUN RULES

23. Break compound nouns. 24. Shorten common nouns harshly. 25. Mash proper nouns with flair ('Nairobi' → 'Nai-beng').


24. Replace 'm/b' with 'mb'. 27. Use onomatopoeia. 28. Alien-sounding nouns are fine. 29. Merge numbers and nouns. 30. Flip boring nouns.



PRONOUN RULES

31. 'I' → 'me/mi'. 32. 'They' → 'deyy'. 33. Avoid colonial grammar (e.g. passive voice). 34. Use street forms. 35. Subject must dominate.



PREPOSITIONS & CONJUNCTIONS

36. 'And' → 'na/n/en'. 37. 'With' → 'whif/shwi'. 38. 'Of' → 'o' or omitted. 39. Drop articles if offbeat. 40. Blend prepositions into verbs.



STYLISTIC RULES

41. Slang > grammar. 42. Draw tone from African languages. 43. Dirty > clean. 44. Use 'z' for power. 45. Pause = valid syntax. 46. Repeat endings. 47. Rhyme > syntax.



CULTURAL RULES

48. Nairobi streets = root. 49. Combine English + Swahili + Sheng. 50. Local tribal tones. 51. Draw from Kenyan rebellion slang. 52. Spoken word & rap = valid structure.



PHONETIC PLAY RULES

53. Emphasize consonants. 54. Glottal stops okay. 55. Drop soft final letters ('love' → 'lof'). 56. Tone markers welcome.



CREATIVE RULES

57. Break rules if it hits harder. 58. If it sounds dope, it's correct. 59. Every line must hit.




---

INSERTION FORMULA: a → ambata | e → embete | i → imbiti | o → omboto | u → umbutu Use PE (Phonetic Emphasis) placement:

Replace only the stressed vowel.

Never remove or reorder original consonants or other letters.

In French words, the PE = last vowel.


MULTI-WORDS: Handle one word at a time unless idiomatic.

RESPONSE FORMAT: Start with explanation (word-by-word breakdown). End with:

Final Shembeteng Translation: [output here]

Translate this: """

def translate_shembeteng(text): full_prompt = f"{shembeteng_prompt}\n{text}" response = model.generate_content(full_prompt) return response.text

@app.route('/') def home(): return "Shembeteng API is live! Use /translate"

@app.route('/translate', methods=['POST']) def translate(): data = request.get_json() if not data or 'text' not in data: return jsonify({'error': 'Missing input text.'}), 400

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

if name == 'main': app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
