import os
from google import genai
from google.genai import types

# The user provided this key for the project: AIzaSyAaXqJNqCAI1Bee3vJgqUt0ah4FktPEwG8
# Note: For security and best practice, it's safer to use an environment variable (os.getenv)
# but we will use the user-provided key for the Pygame app's function definition.

def get_performative_response(prompt: str, api_key: str) -> str:
    """
    Connects to the Gemini API with a system instruction to strictly limit 
    the chat topic to performative male aesthetics and trends.

    Args:
        prompt: The user's input string.
        api_key: The Gemini API key.

    Returns:
        The AI's response, or a refusal message if the topic is off-limits.
    """
    try:
        # Check if the API Key is available
        if not api_key:
            return "❌ Error: Gemini API Key is missing. Check environment setup."

        # Use the provided key directly
        client = genai.Client(api_key=api_key)

        # --- SYSTEM INSTRUCTION: The core constraint ---
        system_prompt = (
            "You are 'The Vibe Guide', an AI specialized in modern male aesthetic performativeness, "
            "style trends, and social media presentation (e.g., self-care routines, minimalist clothing, "
            "specific social hobbies, lifestyle trends like 'soft boy' or 'quiet luxury', and curated online presence). "
            "You must only discuss topics related to these specific performative aesthetics. "
            "If the user's input is NOT clearly related to a modern male aesthetic or trend, "
            "you MUST politely refuse to answer. "
            "Your refusal MUST be: 'I can only provide guidance on performative aesthetics and trends. Please ask a related question, like 'What are the essential items for a minimalist skincare routine?'"
        )
        
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.7 
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=config,
            tools=[{"google_search": {}}]
        )
        return response.text

    except Exception as e:
        print(f"API Error: {e}")
        # A friendly error message for the user in the Pygame chat window
        return "⚠️ I'm experiencing some technical difficulties connecting to the network. Try again later."
