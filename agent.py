from openai import OpenAI
import os

class Agent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history = [
            {"role": "system", "content": "You are a helpful voice-enabled AI assistant. Provide clear and concise responses."}
        ]
    
    def get_response(self, user_input):
        """
        Send user input to OpenAI API and get the response.
        Returns the assistant's response text.
        """
        if not user_input:
            return "I didn't receive any input. Could you please try again?"
        
        # Add user message to conversation history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        try:
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=self.conversation_history,
                max_tokens=150
            )
            
            # Extract and store assistant's response
            assistant_response = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            print(f"Error in OpenAI API call: {e}")
            return "I encountered an error. Please try again." 