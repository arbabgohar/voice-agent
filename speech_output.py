import pyttsx3

class VoiceOutput:
    def __init__(self):
        self.engine = pyttsx3.init()
        
        # Configure voice properties
        self.engine.setProperty('rate', 175)  # Speed of speech
        self.engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
        
        # Get available voices and set a default one
        voices = self.engine.getProperty('voices')
        if voices:
            self.engine.setProperty('voice', voices[0].id)
    
    def speak(self, text):
        """
        Convert text to speech and play it.
        """
        if text:
            print("Assistant:", text)
            self.engine.say(text)
            self.engine.runAndWait() 