import tkinter as tk
from tkinter import messagebox, simpledialog
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import pygame
import io

# Initialize Pygame for audio handling
pygame.init()
pygame.mixer.init()

class TextToSpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Text to Speech Converter")
        
        # URL Entry
        self.url_label = tk.Label(root, text="Enter Blog URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.pack()
        
        # Control Buttons
        self.play_button = tk.Button(root, text="Play", command=self.play_audio)
        self.play_button.pack()
        
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_audio)
        self.pause_button.pack()

        self.stop_button = tk.Button(root, text="Stop", command=self.stop_audio)
        self.stop_button.pack()

        self.save_button = tk.Button(root, text="Save Audio", command=self.save_audio)
        self.save_button.pack()

        # Status label
        self.status = tk.Label(root, text="Status: Waiting for URL...", fg="blue")
        self.status.pack()

    def fetch_text(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        try:
            print("Fetching webpage...")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            text = ' '.join(p.get_text() for p in soup.find_all('p'))
            if not text:
                raise ValueError("No text could be extracted from the page.")
            print(f"Extracted text: {text[:100]}...")  # Print the first 100 characters of the text
            return text
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")
            return None

    def play_audio(self):
        url = self.url_entry.get()
        if not url:
            messagebox.showinfo("Info", "Please enter a URL.")
            return
        text = self.fetch_text(url)
        if text:
            print("Converting text to speech...")
            tts = gTTS(text=text, lang='en', tld='com', slow=False)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            print("Starting playback...")
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            self.status.config(text="Status: Playing", fg="green")

    def pause_audio(self):
        pygame.mixer.music.pause()
        self.status.config(text="Status: Paused", fg="yellow")

    def stop_audio(self):
        pygame.mixer.music.stop()
        self.status.config(text="Status: Stopped", fg="red")

    def save_audio(self):
        url = self.url_entry.get()
        text = self.fetch_text(url)
        if text:
            file_path = simpledialog.askstring("Input", "Enter filename to save as MP3:")
            if file_path:
                print("Saving audio file...")
                tts = gTTS(text=text, lang='en', tld='com', slow=False)
                tts.save(file_path + ".mp3")
                messagebox.showinfo("Success", "Audio saved successfully.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextToSpeechApp(root)
    root.mainloop()

main.py
Displaying main.py.
