# Content Summarizer, Q&A GUI Chatbot

A GUI-based AI-powered tool to summarize text, answer questions, and convert summaries to audio.

## Features
- Summarize text using the `facebook/bart-large-cnn` model.
- Answer questions based on the text and summary using the `deepset/roberta-base-squad2` model.
- Convert summaries or answers to audio using `gTTS`.
- Play, pause, and repeat audio output.
- Save summarized output and Q&A to a file (`summary_output.txt`).

## Installation
1. Clone the repository: git clone https://github.com/srisaiajay11/ContentSummarizerGUI.git
    `cd ContentSummarizer`
2. Install dependencies:
    `pip install -r requirements.txt`
3. Run the application:
    `python summarizer_ui.py`

## Requirements
- Python 3.6+
- See `requirements.txt` for dependencies.

## Usage
1. Enter the content you want to summarize in the input box.
2. Click "Summarize" to generate a summary.
3. Ask questions about the content using the "Ask Question" feature.
4. Use "Play/Pause" and "Repeat" buttons to listen to the summary or answers.
5. Click "Save Output" to save the summary and Q&A to `summary_output.txt`.

## Limitations
- Maximum input text length: 2500 characters.
- Requires internet connection for `gTTS` (text-to-speech).
- Audio file (`temp_audio.mp3`) is temporarily created and deleted during operation.

## License
MIT License
