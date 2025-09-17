# Console TTS Utility

A command-line utility for generating TTS (Text-to-Speech) audio from a text file. It converts text to speech with support for various languages and voice genders, prioritizing edge-tts for better quality and falling back to gTTS if needed.

## Table of Contents (TOC)

- [Features](#features)
- [Libraries Used](#libraries-used)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)

## Features

- **Text-to-Audio Generation**: Reads text from a specified .txt file and converts it to an MP3 audio file.
- **Language Support**: Available languages: ru (Russian), en (English), es (Spanish), fr (French), de (German), it (Italian), pt (Portuguese), ja (Japanese), ko (Korean), zh (Chinese).
- **Voice Gender Selection**: Choose between male or female voices for more natural sounding output.
- **Edge-TTS Priority**: Uses edge-tts for higher quality voices; automatically installs it if missing and prompts to restart the script.
- **gTTS Fallback**: Switches to gTTS if edge-tts is unavailable for basic audio generation.
- **CLI Interface**: Convenient flags for input file path, output, language, and voice gender.
- **Error Handling**: Checks for file existence, empty text, and other common issues.

## Libraries Used

- **subprocess**: For running system commands (e.g., installing packages).
- **sys**: For system parameters and exit handling.
- **asyncio**: For asynchronous operations with edge-tts.
- **argparse**: For parsing command-line arguments.
- **os**: For file system operations (checking directories, paths).
- **gtts**: Google Text-to-Speech library for fallback audio generation.
- **edge_tts**: Microsoft Edge TTS library for high-quality speech synthesis (installed automatically if absent).

## Installation

1. **Requirements**: Ensure you have Python 3.8+ installed.
2. Download these project
```bash
git clone https://github.com/davy1ex/textToSpeech
cd textToSpeech
```
3. **Install Dependencies**:
   - (Optional u can make virtualenv for these step) Manually nstall gTTS or u can use `pip install -r requirements.txt`

## Usage

Run the script using Python:

```
python tts.py --input <path_to_txt_file> [options]
```

Available flags:
- `--input` (required): Path to the input .txt file containing the text.
- `--output` (optional, default: `output.mp3`): Path to save the output MP3 file.
- `--lang` (optional, default: `ru`): Language code (ru, en, es, fr, de, it, pt, ja, ko, zh).
- `--gender` (optional, default: `female`): Voice gender (male or female).

The script will create the output directory if it doesn't exist and process the text from the file.

## Examples

1. Basic run (Russian, female voice):
   ```
   python tts.py --input example.txt
   ```
   Output: `output.mp3` with TTS audio.

2. Specifying language and gender:
   ```
   python tts.py --input hello.txt --output hello_en.mp3 --lang en --gender male
   ```
   Generates English male voice in `hello_en.mp3`.

3. For Japanese language:
   ```
   python tts.py --input text_ja.txt --output audio_ja.mp3 --lang ja --gender female
   ```
