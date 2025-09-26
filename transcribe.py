import argparse
from pathlib import Path
import sys
import whisper

def main():
    parser = argparse.ArgumentParser(
        description="Minimal Whisper CLI: transcribe audio to text"
    )
    parser.add_argument("audio", help="Path to audio file (wav/mp3/m4a/ogg, etc.)")
    parser.add_argument(
        "--lang", "-l",
        default="ru",
        help="Language code (ISO-639-1), e.g. ru, en"
    )
    args = parser.parse_args()

    # Download model relative to project folder
    project_dir = Path(__file__).resolve().parent
    models_dir = project_dir / "models"

    # Load base model; change to 'small'/'medium' if needed
    model = whisper.load_model("base", download_root=str(models_dir))

    # Transcribe with an explicit language (defaults to Russian)
    result = model.transcribe(args.audio, language=args.lang)

    # Print only the transcript text to stdout
    print(result["text"].strip())

if __name__ == "__main__":
    sys.exit(main())
