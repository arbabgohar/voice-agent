import os
from dotenv import load_dotenv
from speech_input import VoiceInput
from speech_output import VoiceOutput
from agent import Agent

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Error: OPENAI_API_KEY environment variable is not set.")
        print("Please create a .env file with your OpenAI API key:")
        print("OPENAI_API_KEY='your api key here'")
        return

    print("Initializing voice assistant...")
    voice_input = VoiceInput()
    voice_output = VoiceOutput()
    agent = Agent()

    print("\nVoice Assistant is ready!")
    print("Speak 'goodbye' or 'exit' to end the conversation.")

    while True:
        # Get speech input
        user_text = voice_input.listen()
        
        if user_text:
            # Check for exit commands
            if user_text.lower() in ['goodbye', 'exit', 'quit', 'bye']:
                voice_output.speak("Goodbye! Have a great day!")
                break
            
            # Get AI response
            response = agent.get_response(user_text)
            
            # Convert response to speech
            voice_output.speak(response)

if __name__ == "__main__":
    main() 
