import subprocess
import sys
import asyncio
import argparse
import os
from gtts import gTTS

VOICE_MAP = {
    'ru': {'male': 'ru-RU-DmitryNeural', 'female': 'ru-RU-SvetlanaNeural'},
    'en': {'male': 'en-US-GuyNeural', 'female': 'en-US-JennyNeural'},
    'es': {'male': 'es-ES-AlvaroNeural', 'female': 'es-ES-ElviraNeural'},
    'fr': {'male': 'fr-FR-HenriNeural', 'female': 'fr-FR-DeniseNeural'},  # Note: Swapped male/female for fr as per original map
    'de': {'male': 'de-DE-ConradNeural', 'female': 'de-DE-KatjaNeural'},
    'it': {'male': 'it-IT-DiegoNeural', 'female': 'it-IT-ElsaNeural'},
    'pt': {'male': 'pt-BR-AntonioNeural', 'female': 'pt-BR-FranciscaNeural'},
    'ja': {'male': 'ja-JP-KeitaNeural', 'female': 'ja-JP-NanamiNeural'},  # Updated to valid voices
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

def read_text_from_file(file_path):
    """Reads text from the given file path and returns it as a string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read().strip()
        if not text:
            raise ValueError("The input file is empty.")
        return text
    except FileNotFoundError:
        print(f"⚠️ File not found: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"⚠️ Error reading file: {e}")
        sys.exit(1)

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
            print("✅ Edge TTS installed. Please run the script again.")
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

def main():
    parser = argparse.ArgumentParser(description="Console TTS utility: Generate audio from a text file.")
    parser.add_argument('--input', required=True, help="Path to the input .txt file.")
    parser.add_argument('--output', default='output.mp3', help="Path to save the output audio file (default: output.mp3).")
    parser.add_argument('--lang', default='ru', choices=VOICE_MAP.keys(), help="Language code (default: ru).")
    parser.add_argument('--gender', default='female', choices=['male', 'female'], help="Voice gender (default: female).")
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    output_dir = os.path.dirname(args.output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    text = read_text_from_file(args.input)
    success = generate_tts_audio(text, args.output, lang=args.lang, voice_gender=args.gender)
    
    if success:
        print(f"🎉 Audio saved to {args.output}")
    else:
        print("❌ Failed to generate audio.")

if __name__ == "__main__":
    main()
