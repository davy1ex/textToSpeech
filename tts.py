import subprocess
import sys
import asyncio
import os
from flask import Flask, request, jsonify
from gtts import gTTS
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
ALLOWED_EXTENSIONS = {'txt'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

VOICE_MAP = {
    'ru': {'male': 'ru-RU-DmitryNeural', 'female': 'ru-RU-SvetlanaNeural'},
    'en': {'male': 'en-US-GuyNeural', 'female': 'en-US-JennyNeural'},
    'es': {'male': 'es-ES-AlvaroNeural', 'female': 'es-ES-ElviraNeural'},
    'fr': {'male': 'fr-FR-HenriNeural', 'female': 'fr-FR-DeniseNeural'},
    'de': {'male': 'de-DE-ConradNeural', 'female': 'de-DE-KatjaNeural'},
    'it': {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
    'pt': {'male': 'pt-BR-AntonioNeural', 'female': 'pt-BR-FranciscaNeural'},
    'ja': {'male': 'ja-JP-KeitaNeural', 'female': 'ja-JP-NanamiNeural'},
    'ko': {'male': 'ko-KR-InJoonNeural', 'female': 'ko-KR-SunHiNeural'},
    'zh': {'male': 'zh-CN-YunxiNeural', 'female': 'zh-CN-XiaoxiaoNeural'}
}

GTTS_LANG_MAP = {
    'en': 'en',
    'ru': 'ru',
    'es': 'es',
    'fr': 'fr',
    'de': 'de',
    'it': 'it',
    'pt': 'pt',
    'ja': 'ja',
    'ko': 'ko',
    'zh': 'zh'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def read_text_from_file(file_path):
    """Reads text from the given file path and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().strip()
        if not text:
            raise ValueError("The input file is empty.")
        return text
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")

def generate_tts_audio(text, output_path, lang='ru', voice_gender='female'):
    """Generates TTS audio from text and saves it to output_path."""
    try:
        # Try to use edge-tts
        try:
            import edge_tts
            
            async def generate_edge_tts():
                voice = VOICE_MAP.get(lang, {}).get(voice_gender, f"{lang.upper()}-Neural")
                communicate = edge_tts.Communicate(text, voice)
                communicate.rate = "+0%"
                await communicate.save(output_path)
            
            asyncio.run(generate_edge_tts())
            print(f"✅ Generated audio with Edge TTS using {voice_gender} voice for language {lang}")
            return True
            
        except ImportError:
            print("⚠️ Edge TTS not installed. Installing now...")
            subprocess.run([sys.executable, "-m", "pip", "install", "edge-tts"])
            print("✅ Edge TTS installed. Please restart the server.")
            return False
        except Exception as e:
            print(f"⚠️ Edge TTS failed: {e}. Falling back to gTTS.")
        
        # Fallback to gTTS
        gtts_lang = GTTS_LANG_MAP.get(lang, lang)
        tts = gTTS(text, lang=gtts_lang, slow=False)
        tts.save(output_path)
        print(f"✅ Generated audio with gTTS for language {lang}")
        return True
        
    except Exception as e:
        print(f"⚠️ TTS error for \"{text[:30]}...\": {e}")
        return False

@app.route('/generate-tts', methods=['POST'])
def generate_tts():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        lang = request.form.get('lang', 'ru')
        gender = request.form.get('gender', 'female')
        
        if lang not in VOICE_MAP:
            return jsonify({'error': f'Invalid language: {lang}'}), 400
        if gender not in ['male', 'female']:
            return jsonify({'error': f'Invalid gender: {gender}'}), 400
        
        try:
            text = read_text_from_file(file_path)
            output_filename = f"{os.path.splitext(filename)[0]}.mp3"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            
            success = generate_tts_audio(text, output_path, lang=lang, voice_gender=gender)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            if success:
                return jsonify({'message': 'Audio generated successfully', 'output_path': output_path}), 200
            else:
                return jsonify({'error': 'Failed to generate audio'}), 500
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(debug=True)
