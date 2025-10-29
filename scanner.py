from google import genai
import os
from google.genai import types
from PIL import Image
from io import BytesIO

# --- Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY") 
client = genai.Client(api_key=API_KEY)

performative_items = {
    "matcha": {
        "name": "Otsuka Green Tea Co Shizuoka Matcha Powder",
        "price": 13.00
    },
    "labubu": {
        "name": "POP MART Kasing Labubu The Monsters Exciting Macarons Figure",
        "price": 37.99
    },
    "feminine_literature": {
        "name": "Pride and Prejudice",
        "price": 6.99
    },
    "flannel": {
        "name": "Legendary Whitetails Men's Flannel Cedarwood Plaid Shirt",
        "price": 58.09
    },
    "baggy_jeans": {
        "name": "Baggy Skater Vintage Casual Jeans",
        "price": 25.00
    },
    "tote_bag": {
        "name": "Tote Bag",
        "price": 17.99
    },
    "wired_headphones": {
        "name": "Apple Wired Headphones",
        "price": 19.99
    },
    "vintage_clothing": {
        "name": "Thrifted Vintage Clothing",
        "price": 0.00
    },
    "rings": {
        "name": "Rings",
        "price": 13.99
    }
}

PROMPT = "Analyse the perfomative maleness of this image, from 1 to 100. Assess it ONLY on presence of items from this list: matcha, labubu, feminine_literature, baggy_jeans, rings, tote_bag, wired_headphones, vintage_clothing. Higher scores indicate a stronger presence of these items. Return ONLY the tuple of 1) the score, as an integer 2) the list of all items that could be added, with underscores instead of spaces"
GENERATION_PROMPT = "Generate a more performative male version of this image. Make sure all these items are somehow included in the image unless they already are: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing. Keep background the same"
AI_IMAGE_OUTPUT_PATH = r"more_ performative_image.jpg"


def analyze_image(image_path: str) -> str:
    try:
        input_image = Image.open(image_path)
        
        analysis_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[input_image, PROMPT]
        )

        score, items_to_add = eval(analysis_response.text)

        shopping_list = []
        for item in items_to_add:
            item_info = performative_items.get(item)
            if item_info:
                shopping_list.append(item_info)

        print("\n Analysis Complete:")
        return input_image, analysis_response.text, shopping_list


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
                
                generated_image.save(AI_IMAGE_OUTPUT_PATH)
                return True
                break 
        
    except Exception as e:
        print(f"An error occurred during image generation: {e}")
        return False