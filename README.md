# Web TTS Utility

A Flask-based web service and command-line utility for generating TTS (Text-to-Speech) audio from a text file. It converts text to speech with support for various languages and voice genders, prioritizing `edge-tts` for better quality and falling back to `gTTS` if needed.

## Table of Contents (TOC)

- [Features](#features)
- [Libraries Used](#libraries-used)
- [Installation](#installation)
- [Usage](#usage)
- [API Usage](#api-usage)
- [Examples](#examples)

## Features

- **Text-to-Audio Generation**: Reads text from a specified `.txt` file and converts it to an MP3 audio file.
- **Language Support**: Available languages include: 
  - Russian (ru)
  - English (en)
  - Spanish (es)
  - French (fr)
  - German (de)
  - Italian (it)
  - Portuguese (pt)
  - Japanese (ja)
  - Korean (ko)
  - Chinese (zh)
- **Voice Gender Selection**: Choose between male or female voices for more natural-sounding output.
- **Edge-TTS Priority**: Uses `edge-tts` for higher-quality voices; automatically installs it if missing and prompts to restart the server.
- **gTTS Fallback**: Falls back to `gTTS` if `edge-tts` is unavailable for basic audio generation.
- **Flask Web Service**: Provides a convenient API for generating TTS audio from uploaded text files.
- **Error Handling**: Checks for file existence, empty text, and other common issues during the TTS generation process.

## Libraries Used

- **subprocess**: For running system commands (e.g., installing packages).
- **sys**: For system parameters and exit handling.
- **asyncio**: For asynchronous operations with `edge-tts`.
- **Flask**: For serving the TTS generation as a web API.
- **werkzeug**: For handling file uploads and secure file names.
- **gtts**: Google Text-to-Speech library for fallback audio generation.
- **edge_tts**: Microsoft Edge TTS library for high-quality speech synthesis (installed automatically if absent).

## Installation

1. **Requirements**: Ensure you have Python 3.8+ installed.
2. **Clone the repository**:
    ```bash
    git clone https://github.com/davy1ex/textToSpeech
    cd textToSpeech
    ```
3. **Install Dependencies**:
    - (Optionally, you can create a virtual environment for the dependencies)
    - Install required packages using pip:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the Flask web service using Python:

```bash
python app.py
````

The server will start running on `http://localhost:5000`.

### API Usage

You can use the `/generate-tts` endpoint to generate speech from a `.txt` file. The endpoint accepts a POST request with the file and additional form data:

**Endpoint**: `/generate-tts`
**Method**: `POST`

### Request

* **file** (required): The text file (`.txt`) to convert to speech.
* **lang** (optional, default: `ru`): The language code for the TTS. Supported languages: `ru`, `en`, `es`, `fr`, `de`, `it`, `pt`, `ja`, `ko`, `zh`.
* **gender** (optional, default: `female`): Choose the voice gender: `male` or `female`.

### Response

* **Success**:

  ```json
  {
    "message": "Audio generated successfully",
    "output_path": "outputs/example.mp3"
  }
  ```
* **Error**:

  ```json
  {
    "error": "Error message"
  }
  ```

### Example Request

**cURL example:**

```bash
curl -X POST -F "file=@example.txt" -F "lang=en" -F "gender=male" http://localhost:5000/generate-tts
```

## Examples

### Basic Run (Russian, female voice)

Send a `.txt` file to generate an audio file with Russian language and a female voice:

```bash
curl -X POST -F "file=@example.txt" http://localhost:5000/generate-tts
```

Output: `outputs/example.mp3` with TTS audio in Russian (female).

### Specifying Language and Gender (English, Male Voice)

Specify the language and voice gender for the generated audio:

```bash
curl -X POST -F "file=@hello.txt" -F "lang=en" -F "gender=male" http://localhost:5000/generate-tts
```

Output: `outputs/hello.mp3` with TTS audio in English (male).

### Specifying Japanese Language and Female Voice

Generate audio in Japanese with a female voice:

```bash
curl -X POST -F "file=@text_ja.txt" -F "lang=ja" -F "gender=female" http://localhost:5000/generate-tts
```

Output: `outputs/audio_ja.mp3` with TTS audio in Japanese (female).

