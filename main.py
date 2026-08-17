import os
import re
import json
import random
import requests

# Facebook Credentials from GitHub Secrets
FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")

DEFAULT_IMAGE_PROMPTS = [
    "close up of fresh ripe sweet yellow himsagar mangoes in a wooden basket on a rustic table 4k high quality photo",
    "fresh organic amrapali mangoes hanging on a tree branch morning sunlight crisp photography",
    "fresh ripe lengra mangoes sliced on a wooden board juicy and delicious professional food photography",
    "freshly harvested sweet green and yellow fazli mangoes in bamboo basket aesthetic lighting 4k"
]

def generate_mango_content():
    print("🧠 Generating Bengali mango promotional content...")
    
    prompt = (
        "Write an attractive, premium promotional Facebook post in Bengali for 'চাঁদপুর আমঘর' "
        "(selling 100% organic chemical-free fresh garden mangoes like Himsagar, Lengra, Amrapali). "
        "Include engaging emojis, a strong call to action to inbox for orders, and relevant hashtags (#চাঁদপুর_আমঘর #FreshMango #Chandpur). "
        "Also write a 1-sentence prompt in English for an AI image generator showing ripe fresh mangoes. "
        "Format strictly as JSON with keys 'caption' and 'image_prompt'. Return ONLY raw JSON without markdown code ticks."
    )
    
    caption = ""
    img_prompt = ""

    try:
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}?json=true"
        response = requests.get(url, timeout=30)
        
        if response.status_code == 200:
            raw_text = response.text.strip()
            cleaned = re.sub(r"^```(json)?", "", raw_text, flags=re.IGNORECASE)
            cleaned = re.sub(r"```$", "", cleaned).strip()
            data = json.loads(cleaned)
            if isinstance(data, dict):
                caption = data.get("caption") or ""
                img_prompt = data.get("image_prompt") or ""
    except Exception as e:
        print(f"⚠️ Text AI fallback triggered: {e}")

    # Fallback caption if network delays
    if not caption:
        caption = (
            "🥭 চাঁদপুর আমঘর - আসল স্বাদের নিশ্চয়তা! 🥭\n\n"
            "বাগান থেকে সরাসরি বাছাই করা একদম ফরমালিন ও কেমিক্যালমুক্ত মিষ্টি ও রসালো আম পৌঁছে যাচ্ছে আপনার দরজায়।\n\n"
            "✨ ১০০% খাঁটি ও তাজা\n"
            "🚚 দ্রুত হোম ডেলিভারি\n\n"
            "অর্ডার করতে এখনই ইনবক্সে মেসেজ দিন অথবা যোগাযোগ করুন!\n\n"
            "#চাঁদপুর_আমঘর #আম #FreshMango #OrganicFruit #Chandpur"
        )

    if not img_prompt:
        img_prompt = random.choice(DEFAULT_IMAGE_PROMPTS)

    return caption, str(img_prompt)

def generate_image(prompt):
    print(f"🎨 Generating unique AI image for prompt: {prompt}")
    encoded_img_prompt = requests.utils.quote(prompt)
    seed = random.randint(1000, 999999)
    img_url = f"https://image.pollinations.ai/prompt/{encoded_img_prompt}?width=1080&height=1080&nologo=true&seed={seed}"
    
    res = requests.get(img_url, timeout=60)
    img_path = "mango_post.jpg"
    with open(img_path, "wb") as f:
        f.write(res.content)
        
    print("✅ Image generated and saved successfully.")
    return img_path

def post_to_facebook(image_path, caption):
    print("🚀 Uploading to Facebook Page...")
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    
    with open(image_path, "rb") as img_file:
        payload = {
            "caption": caption,
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        files = {
            "source": img_file
        }
        response = requests.post(url, data=payload, files=files, timeout=40)
        
    result = response.json()
    if "id" in result:
        print(f"🎉 Post successfully published! Post ID: {result['id']}")
    else:
        print(f"❌ Error publishing to Facebook: {json.dumps(result, indent=2)}")
        raise Exception("Facebook posting failed")

def main():
    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        print("❌ Missing Facebook credentials in environment.")
        return

    caption, img_prompt = generate_mango_content()
    image_file = generate_image(img_prompt)
    post_to_facebook(image_file, caption)

if __name__ == "__main__":
    main()
