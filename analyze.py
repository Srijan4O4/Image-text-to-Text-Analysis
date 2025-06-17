import os
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai import types
from google import genai
from PIL import Image
from google.generativeai.types import HarmCategory, HarmBlockThreshold

# Configure logging
logging.basicConfig(
    filename='gemini_analysis.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Load environment variables and configure Gemini
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# genai.configure(api_key=GEMINI_API_KEY)  # Removed: not needed for google.generativeai

def analyze_product(image_path, product_name, description):
    try:
        # Log incoming data
        logging.info(f"Analyzing product - Name: {product_name}")
        logging.info(f"Description: {description}")
        
        # Read image bytes
        with open(image_path, 'rb') as f:
            image_bytes = f.read()
        
        # Prepare prompt
        prompt = f"""Analyze this product image and determine:
        1. Is this image authentic or potentially manipulated? (Score 0-1)
        2. Does the image match the product name '{product_name}'? (Score 0-1)
        3. Are there signs this could be counterfeit? (Score 0-1)
        4. Does the image match the description: '{description}'?
        
        Format response as JSON with scores and explanation."""

        # Generate content using the correct type structure

        client = genai.Client(api_key=GEMINI_API_KEY)
        image = Image.open(image_path)
        response = client.models.generate_content(
            model='gemini-2.0-flash-exp',
            contents=[
                image,
                prompt
            ]
        )
        
        # Log Gemini's thought process
        logging.info(f"Gemini Analysis: {response.text}")
        
        # Parse response and make decision
        if response.text and ("counterfeit" in response.text.lower() or "fake" in response.text.lower()):
            logging.warning("Product flagged as suspicious")
            return {
                "status": "Flagged as suspicious",
                "analysis": response.text
            }
        
        logging.info("Product approved")
        return {
            "status": "Approved",
            "analysis": response.text
        }
        
    except Exception as e:
        logging.error(f"Error analyzing product: {str(e)}")
        return {
            "status": "Error",
            "message": str(e)
        }

# Example usage
if __name__ == "__main__":
    result = analyze_product(
        "path/to/your/image.jpg",
        "Example Product",
        "This is a sample product description"
    )
    print(result)