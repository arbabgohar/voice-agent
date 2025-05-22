import subprocess

class VoiceOutput:
    def __init__(self):
        pass
    
    def speak(self, text):
        """
        Convert text to speech using macOS say command.
        """
        if text:
            print("Assistant:", text)
            subprocess.run(['say', text]) 