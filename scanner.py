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
        "url": "https://www.amazon.ca/Otsuka-Green-Tea-Co-Shizuoka/dp/B07VLWBGKS",
        "price": 13.00
    },
    "labubu": {
        "name": "POP MART Kasing Labubu The Monsters Exciting Macarons Figure",
        "url": "https://www.amazon.ca/POP-MART-Big-into-Energy/dp/B0DT44TSM2",
        "price": 37.99
    },
    "feminine_literature": {
        "name": "Pride and Prejudice",
        "url": "https://www.amazon.ca/Pride-Prejudice-Collins-Classics-Austen/dp/0007350775",
        "price": 6.99
    },
    "flannel": {
        "name": "Legendary Whitetails Men's Flannel Cedarwood Plaid Shirt",
        "url": "https://www.amazon.ca/Legendary-Whitetails-Flannels-Cedarwood-Plaid/dp/B01K0ETB6E",
        "price": 58.09
    },
    "baggy_jeans": {
        "name": "Baggy Skater Vintage Casual Jeans",
        "url": "https://www.amazon.ca/Baggy-Skater-Vintage-Casual-2-grey/dp/B0C78LXRT7",
        "price": 25.00
    },
    "tote_bag": {
        "name": "BROADREAM Canvas Tote Bag Aesthetic",
        "url": "https://www.amazon.ca/BROADREAM-Canvas-Tote-Bag-Aesthetic/dp/B0CHMGWRKZ",
        "price": 17.99
    },
    "wired_headphones": {
        "name": "LORELEI X6 Wired Headphones with Microphone",
        "url": "https://www.amazon.ca/LORELEI-X6-Headphones-Microphone-Lightweight/dp/B083P1HG9S",
        "price": 19.99
    },
    "vintage_clothing": {
        "name": "Thrifted Vintage Clothing (External)",
        "url": "https://www.thrifted.com/",
        "price": 0.00
    },
    "rings": {
        "name": "Stainless Steel Fidget Spinner Ring",
        "url": "https://www.amazon.ca/Stainless-Fidget-Spinner-Anxiety-Relieving/dp/B09DJQ94KY",
        "price": 13.99
    }
}

PROMPT = "Analyse the perfomative maleness of this image, from 1 to 100. Assess it ONLY on presence of items from this list: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing. Higher scores indicate a stronger presence of these items. Provide a score and a bri. Return a list of all items that could be added from the list and REAL links to purchase them."
GENERATION_PROMPT = "Generate a more performative male version of this image. Make sure all these items are somehow included in the image unless they already are: matcha, labubu, feminine literature, baggy jeans, rings, tote bag, wired headphones, vintage clothing. Keep background the same"
AI_IMAGE_OUTPUT_PATH = r"more_ performative_image.jpg"


def analyze_image(image_path: str) -> str:
    try:
        input_image = Image.open(image_path)
        
        analysis_response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[input_image, PROMPT]
        )
        
        print("\n Analysis Complete:")
        return input_image,analysis_response.text


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