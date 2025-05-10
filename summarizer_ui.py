from transformers import pipeline
import tkinter as tk
from tkinter import scrolledtext
from gtts import gTTS
import pygame
import os

class ContentSummarizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ajay's Content Summarizer, Q&A chatbot")
        self.root.geometry("600x600")

        # Pipelines
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")

        # Audio Control
        self.is_playing = False
        self.paused = False
        self.audio_file = "temp_audio.mp3"
        self.latest_output = ""

        # UI Elements
        tk.Label(root, text="Enter Text to Summarize:").pack()
        self.text_input = scrolledtext.ScrolledText(root, height=5, width=50)
        self.text_input.pack()

        tk.Button(root, text="Summarize", command=self.generate_summary).pack()

        tk.Label(root, text="Output (Summary, Questions, Answers):").pack()
        self.output_display = scrolledtext.ScrolledText(root, height=15, width=50)
        self.output_display.pack()

        tk.Label(root, text="Ask a Question:").pack()
        self.question_input = tk.Entry(root, width=50)
        self.question_input.pack()

        tk.Button(root, text="Ask Question", command=self.answer_question).pack()

        tk.Label(root, text="Status:").pack()
        self.status = tk.Text(root, height=1, width=50)
        self.status.pack()
        self.status.insert(tk.END, "Ready")

        tk.Button(root, text="Play/Pause", command=self.toggle_play_pause).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Repeat", command=self.repeat_output).pack(side=tk.LEFT, padx=5)
        tk.Button(root, text="Save Output", command=self.save_output).pack(pady=10)

        pygame.mixer.init()

    def update_status(self, message):
        self.status.delete("1.0", tk.END)
        self.status.insert(tk.END, message)

    def stop_audio(self):
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        self.is_playing = False
        self.paused = False

    def generate_audio(self, text):
        try:
            if os.path.exists(self.audio_file):
                os.remove(self.audio_file)
            tts = gTTS(text=text, lang='en')
            tts.save(self.audio_file)
        except Exception as e:
            self.update_status(f"Error generating audio: {e}")

    def play_audio(self):
        try:
            pygame.mixer.music.load(self.audio_file)
            pygame.mixer.music.play()
            self.is_playing = True
            self.paused = False
            self.update_status("Playing audio...")
        except Exception as e:
            self.update_status(f"Error playing audio: {e}")

    def toggle_play_pause(self):
        if self.is_playing and not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.is_playing = False
            self.update_status("Speech paused.")
        else:
            if not self.latest_output:
                self.update_status("Error: No output to play!")
                return
            if self.paused:
                pygame.mixer.music.unpause()
                self.is_playing = True
                self.paused = False
                self.update_status("Resuming audio...")
            else:
                self.stop_audio()
                self.generate_audio(self.latest_output)
                self.play_audio()

    def repeat_output(self):
        if not self.latest_output:
            self.update_status("Error: No output to repeat!")
            return
        self.stop_audio()
        self.update_status("Repeating audio...")
        self.generate_audio(self.latest_output)
        self.play_audio()

    def generate_summary(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text:
            self.output_display.insert(tk.END, "Error: Please enter text!\n")
            return
        if len(text) > 2500:
            self.output_display.insert(tk.END, "Error: Text exceeds 2500 characters. Please shorten it.\n")
            return
        try:
            summary = self.summarizer(text, max_length=50, min_length=20, do_sample=False)[0]['summary_text']
            self.output_display.delete("1.0", tk.END)
            self.output_display.insert(tk.END, f"Summary: {summary}\n\n")
            self.latest_output = f"Summary: {summary}"
        except Exception as e:
            self.output_display.insert(tk.END, f"Error generating summary: {e}\n")

    def answer_question(self):
        text = self.text_input.get("1.0", tk.END).strip()
        if not text or not self.latest_output.startswith("Summary: "):
            self.output_display.insert(tk.END, "Error: Please generate a summary first!\n")
            return
        question = self.question_input.get().strip()
        if not question:
            self.output_display.insert(tk.END, "Error: Please enter a question!\n")
            return
        try:
            full_context = text + " " + self.latest_output[9:]  # Remove "Summary: " prefix
            answer = self.qa_pipeline(question=question, context=full_context)['answer']
            self.output_display.insert(tk.END, f"Question: {question}\nAnswer: {answer}\n\n")
            self.latest_output = f"Answer: {answer}"
            self.question_input.delete(0, tk.END)
        except Exception as e:
            self.output_display.insert(tk.END, f"Error answering question: {e}\n")

    def save_output(self):
        output_text = self.output_display.get("1.0", tk.END).strip()
        if not output_text:
            self.output_display.insert(tk.END, "Error: No output to save!\n")
            return
        try:
            with open("summary_output.txt", "w", encoding="utf-8") as file:
                file.write(output_text)
            self.update_status("Output saved to summary_output.txt")
            self.latest_output = "Output saved to summary output dot text file"
        except Exception as e:
            self.update_status(f"Error saving output: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContentSummarizerApp(root)
    root.mainloop()