from google import genai
import os
from google.genai import types
from PIL import Image
from io import BytesIO

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

image_response = None

# *** IMPORTANT: Change the path to your actual image file ***
IMAGE_PATH = r"C:\Users\zambe\Downloads\20251029_102651.jpg"
PROMPT = "Analyse the perfomative maleness of this image, from 1 to 100. Assess it ONLY on presence of items from this list: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing. Higher scores indicate a stronger presence of these items. Provide a score and a brief explanation. Return a list of all items that could be added from the list and REAL links to purchase them."
GENERATION_PROMPT = "Generate a more performative male version of this image. Make sure all these items are somehow included in the image unless they already are: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing. Keep background the same"

def analyze_image(image_path: str) -> str:
    try:
        input_image = Image.open(image_path)
        
        analysis_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[input_image, PROMPT]
        )
        
        image_response = analysis_response.text
        print("\n Analysis Complete:")
        print(image_response)


    except FileNotFoundError:
        print(f"Error: Image file not found at {image_path}")
        exit() 
    except Exception as e:
        print(f"An error occurred during analysis: {e}")
        exit()

def generate_more_performative_image(image_path: str):

    input_image = Image.open(image_path)

    try:

        generation_response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=[input_image, GENERATION_PROMPT]
        )
        
        # Extract, save, and show the generated image
        for part in generation_response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                generated_image = Image.open(BytesIO(image_data))
                
                generated_image.save("more_performative_image.png")
                generated_image.show()
                break
                
    except Exception as e:
        print(f"An error occurred during image generation: {e}")

if __name__ == "__main__":
    
    analyze_image(IMAGE_PATH)
    generate_more_performative_image(IMAGE_PATH)