import os
import requests
import google.generativeai as genai

# --- CONFIGURATION (Load Secrets) ---
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY") # We are using this key for Gemini to write the text
IMAGE_API_KEY = os.environ.get("IMAGE_API_KEY")   # <-- Add your separate Image Generation Key here

# API Configuration
genai.configure(api_key=GEMINI_API_KEY)
# Assuming you set up an image API key secret as 'IMAGE_API_KEY' for Vertex AI or similar
IMAGE_GEN_ENDPOINT = "https://example-image-generation-api.com/generate" # Replace this with the actual endpoint

# --- STEP 1: GENERATE UNIQUE BENGALI TEXT (Gemini API) ---
def generate_bengali_post_text():
    print("Generating Bengali text with Gemini...")
    model = genai.GenerativeModel('gemini-pro')
    prompt = "চাঁদপুর আমঘর এর জন্য ফ্রেশ আম, হিমসাগর, আম্রপালি, এবং হাড়িভাঙ্গা আমের অফার নিয়ে একটি আকর্ষণীয় ফেসবুক পোস্ট বাংলায় লিখে দাও। পোস্টের শেষে #চাঁদপুরআমঘর এবং #তাজাআম ব্যবহার কর।"
    response = model.generate_content(prompt)
    bengali_text = response.text.strip()
    return bengali_text

# --- STEP 2: GENERATE UNIQUE IMAGE (Vertex AI / Dall-E API) ---
def generate_unique_mango_image():
    print("Generating a new, unique mango image...")
    # This step requires a separate call to an image API.
    # Replace this with the actual request structure of your image API.
    
    headers = {
        "Authorization": f"Bearer {IMAGE_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Define a different prompt for variety (e.g., focus on different mango types)
    image_prompt = "A high-resolution photograph of fresh, ripe Himsagar and Amrapali mangoes displayed beautifully in a traditional bamboo basket, natural sunlight, vivid colors."

    data = {
        "prompt": image_prompt,
        "n": 1,
        "size": "1024x1024" # Standard square size
    }

    try:
        response = requests.post(IMAGE_GEN_ENDPOINT, headers=headers, json=data)
        response.raise_for_status() # Check for errors
        
        image_url = response.json()['data'][0]['url'] # The structure depends on the specific API response
        print(f"Generated Image URL: {image_url}")
        return image_url
        
    except requests.exceptions.RequestException as e:
        print(f"Error generating image: {e}")
        return None

# --- STEP 3: PUBLISH TO FACEBOOK PAGE (Meta Graph API) ---
def publish_photo_to_facebook(image_url, message_text):
    print("Publishing to Facebook Page with image and text...")
    
    # We are publishing a photo POST with the image URL and the Bengali caption
    post_url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    
    payload = {
        "url": image_url,
        "caption": message_text,
        "access_token": FB_PAGE_ACCESS_TOKEN
    }
    
    try:
        response = requests.post(post_url, data=payload)
        response.raise_for_status()
        
        print(f"Successfully published post to Facebook! Response: {response.json()}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error publishing to Facebook: {e}")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    bengali_text = generate_bengali_post_text()
    image_url = generate_unique_mango_image()
    
    if image_url:
        publish_photo_to_facebook(image_url, bengali_text)
    else:
        print("Image generation failed. Skipping Facebook post publishing.")
