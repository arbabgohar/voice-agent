import speech_recognition as sr
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import io
import wave

class VoiceInput:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.sample_rate = 44100  # Standard sample rate
        self.channels = 1  # Mono audio
        
    def record_audio(self, duration=5):
        """Record audio from microphone using sounddevice."""
        print("Listening... (Speak now)")
        audio_data = sd.rec(
            int(self.sample_rate * duration),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=np.int16
        )
        sd.wait()  # Wait until recording is finished
        return audio_data
        
    def create_audio_data(self, audio_array):
        """Convert numpy array to audio data compatible with speech_recognition."""
        byte_io = io.BytesIO()
        
        # Create WAV file in memory
        with wave.open(byte_io, 'wb') as wav_file:
            wav_file.setnchannels(self.channels)
            wav_file.setsampwidth(2)  # 2 bytes for int16
            wav_file.setframerate(self.sample_rate)
            wav_file.writeframes(audio_array.tobytes())
            
        # Create AudioData object
        byte_io.seek(0)
        with sr.AudioFile(byte_io) as source:
            audio_data = self.recognizer.record(source)
        return audio_data
    
    def listen(self):
        """
        Listen to microphone input and convert speech to text.
        Returns the recognized text or None if recognition failed.
        """
        try:
            # Record audio
            audio_array = self.record_audio()
            
            # Convert to format compatible with speech_recognition
            audio_data = self.create_audio_data(audio_array)
            
            print("Processing speech...")
            text = self.recognizer.recognize_google(audio_data)
            print(f"You said: {text}")
            return text
            
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except Exception as e:
            print(f"Error during recording: {e}")
            return None 