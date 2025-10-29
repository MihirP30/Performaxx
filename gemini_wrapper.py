import os
from google import genai

class GeminiClientWrapper:
    """
    A simple wrapper class for the Google GenAI Client.
    """
    def __init__(self, model_name: str = 'gemini-2.5-flash'):
        """
        Initializes the client. It automatically looks for the API key 
        in the GEMINI_API_KEY environment variable.
        """
        # The genai.Client() automatically picks up the API key 
        # from the GEMINI_API_KEY environment variable.
        try:
            self.client = genai.Client()
        except Exception as e:
            # Handle case where API key is not set
            if "API key is not set" in str(e):
                raise ValueError("GEMINI_API_KEY environment variable is not set. Please set your API key.")
            else:
                raise e
        
        self.model_name = model_name
        
    def generate_text(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Sends a text prompt to the Gemini model and returns the response text.

        Args:
            prompt: The user's text prompt.
            temperature: The generation temperature (0.0 to 2.0).
        
        Returns:
            The generated response text.
        """
        config = genai.types.GenerateContentConfig(
            temperature=temperature
        )
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
            config=config,
        )
        
        return response.text

    # --- You can add more methods here for other functionalities ---
    
    def start_chat_session(self, system_instruction: str = None):
        """
        Starts a new chat session to maintain conversation history.
        """
        config = None
        if system_instruction:
            config = genai.types.GenerateContentConfig(
                system_instruction=system_instruction
            )
            
        chat = self.client.chats.create(
            model=self.model_name, 
            config=config
        )
        return chat