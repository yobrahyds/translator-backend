from flask import Flask, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=os.environ.get("Gemini_api_key"))

# Translation function using Gemini
def translate_shembeteng(text):
    shembeteng_protocol = """
    INSERT YOUR FULL PROTOCOL PROMPT HERE (TRIMMED FOR SPACE)
    """
    model = genai.GenerativeModel('gemini-1.5-flash')
    full_prompt = f"{shembeteng_protocol}\n{text}"
    response = model.generate_content(full_prompt)
    return response.text

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({'error': 'Missing text field'}), 400
    try:
        result = translate_shembeteng(data['text'])
        # Extract final translation
        import re
        match = re.search(r'Final Shembeteng Translation:\s*\*\*([^\*]+?)\*\*', result)
        translated = match.group(1).strip() if match else "Translation not found."
        return jsonify({'translation': translated})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)