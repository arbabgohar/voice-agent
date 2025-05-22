from openai import OpenAI
import os

class Agent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('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'))
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
            
            # Extract assistant's response
            assistant_response = response.choices[0].message.content
            
            # Add assistant's response to conversation history
            self.conversation_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            print(f"Error in getting response from OpenAI: {e}")
            return "I encountered an error. Please make sure your OpenAI API key is set correctly." 