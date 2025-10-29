from google import genai
import os
from google.genai import types
from PIL import Image
from io import BytesIO

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

# *** IMPORTANT: Change the path to your actual image file ***
IMAGE_PATH = r"C:\Users\zambe\Downloads\20251029_102651.jpg"
PROMPT = "Analyse the perfomative maleness of this image, from 1 to 100. Assess it on this list: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing. Provide a score and a brief explanation."
GENERATION_PROMPT = "Generate a more performative male version of this image. Make sure all these items are somehow included in the image unless they already are: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing."

# --- Step 1: Text Analysis (Use Gemini) ---
print("--- Step 1: Analyzing image with gemini-2.5-flash... ---")
try:
    input_image = Image.open(IMAGE_PATH)
    
    # 1. ANALYSIS CALL
    analysis_response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[input_image, PROMPT]
    )
    
    # Print the analysis score and text
    print("\n Analysis Complete:")
    print(analysis_response.text)

except FileNotFoundError:
    print(f"Error: Image file not found at {IMAGE_PATH}")
    # Stop execution if the file is not found
    exit() 
except Exception as e:
    print(f"An error occurred during analysis: {e}")
    exit()

# --- Step 2: Image Generation (Use Imagen) ---
print("\n--- Step 2: Generating new image with imagen-3.0-generate-002... ---")
try:
    # 2. GENERATION CALL
    # You need to pass the input image again for the image model to base its generation on.
    generation_response = client.models.generate_content(
        model='gemini-2.5-flash-image',
        contents=[input_image, GENERATION_PROMPT]
    )
    
    # Extract, save, and show the generated image
    for part in generation_response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            generated_image = Image.open(BytesIO(image_data))
            
            # Save and display
            generated_image.save("more_performative_image.png")
            generated_image.show() 
            print("Image Generation Complete: Saved and displayed 'more_performative_image.png'")
            break # Exit the loop after finding the first image
            
except Exception as e:
    print(f"An error occurred during image generation: {e}")
