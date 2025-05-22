import speech_recognition as sr

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
    
    def listen(self):
        """
        Listen to microphone input and convert speech to text.
        Returns the recognized text or None if recognition failed.
        """
        try:
            print("Listening... (Speak now)")
            with self.microphone as source:
                audio = self.recognizer.listen(source)
                
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
            
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None 