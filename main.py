import os
import random
import urllib.parse
import requests
import google.generativeai as genai

# Read secrets from GitHub Actions environment
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

def generate_bengali_post_text():
    print("🧠 Generating Bengali text with Gemini...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = (
            "চাঁদপুর আমঘর এর জন্য ফ্রেশ আম, হিমসাগর, আম্রপালি, এবং হাড়িভাঙ্গা আমের অফার নিয়ে "
            "একটি আকর্ষণীয় ছোট ফেসবুক ক্যাপশন বাংলায় লিখে দাও। পোস্টের শেষে #চাঁদপুরআমঘর এবং #তাজাআম হ্যাশট্যাগ ব্যবহার কর।"
        )
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini generation fallback triggered: {e}")
        return (
            "🥭 চাঁদপুর আমঘর - আসল স্বাদের নিশ্চয়তা! 🥭\n\n"
            "বাগান থেকে সরাসরি বাছাই করা একদম ফরমালিন ও কেমিক্যালমুক্ত মিষ্টি ও রসালো আম পৌঁছে যাচ্ছে আপনার দরজায়।\n\n"
            "অর্ডার করতে এখনই ইনবক্সে মেসেজ দিন।\n\n#চাঁদপুরআমঘর #তাজাআম"
        )

def get_ai_image_url():
    print("🎨 Generating dynamic AI image URL...")
    # List of varied prompts so every post gets a different AI photo
    prompts = [
        "fresh ripe sweet yellow mangoes in a traditional bamboo basket, natural sunlight, professional food photography, 4k",
        "delicious sliced yellow himsagar mangoes on a rustic wooden table, bright daylight, high resolution",
        "organic amrapali mangoes hanging on tree branch with green leaves, sunny orchard, crisp photography",
        "a wooden crate full of fresh golden mangoes in an open village market, ultra realistic",
        "freshly harvested sweet green and yellow fazli mangoes close up shot, vibrant colors, aesthetic lighting"
    ]
    selected_prompt = random.choice(prompts)
    encoded_prompt = urllib.parse.quote(selected_prompt)
    seed = random.randint(1, 999999)
    # Free high-resolution AI image generation endpoint
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?seed={seed}&width=1080&height=1080&nologo=true"

def publish_to_facebook(image_url, message_text):
    print("🚀 Publishing to Facebook Page...")
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    payload = {
        "url": image_url,
        "caption": message_text,
        "access_token": FB_PAGE_ACCESS_TOKEN
    }
    response = requests.post(url, data=payload, timeout=60)
    result = response.json()
    if response.status_code == 200 and "id" in result:
        print(f"🎉 Successfully posted! Post ID: {result.get('id')}")
    else:
        print(f"❌ Failed to publish: {result}")
        raise Exception("Facebook publishing failed")

if __name__ == "__main__":
    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        print("❌ Missing Facebook credentials!")
    else:
        caption = generate_bengali_post_text()
        img_url = get_ai_image_url()
        publish_to_facebook(img_url, caption)
   
