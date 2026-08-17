import os
import re
import json
import random
import requests

FB_PAGE_ID = os.environ.get("FB_PAGE_ID")
FB_PAGE_ACCESS_TOKEN = os.environ.get("FB_PAGE_ACCESS_TOKEN")

CONTENT_THEMES = [
    {
        "type": "emotional_family",
        "guidance": "Write an emotional storytelling post in Bengali about sending mangoes as a heartfelt gift to mothers, fathers, or family back home from Probashi/expats. Mention handwritten message card. Tone: Loving, poetic, warm.",
        "image_prompt": "cinematic photorealistic shot of an open craft cardboard gift box with ripe golden himsagar mangoes and a handwritten greeting letter card on wooden table, warm sunbeam, 8k",
        "fallback_caption": "মা, এবার আমটা তোমার জন্য। ❤️\n\nকখনো কখনো কথা বলা যায় না… কিন্তু অনুভূতি পাঠানো যায়। চাঁদপুর আমঘর-এর প্রতিটি আমের সাথে আপনি পাঠাতে পারেন একটি ছোট ভালোবাসার চিঠি।\n\n✨ সারা দেশে হোম ডেলিভারি\n✨ ফ্রি পার্সোনাল মেসেজ কার্ড\n\n#চাঁদপুরআমঘর #Probashi #SendLoveHome #MothersLove #BangladeshiMango"
    },
    {
        "type": "children_health",
        "guidance": "Write a post in Bengali highlighting that our mangoes are 100% formalin-free, chemical-free, and perfectly safe for kids and toddlers. Tone: Caring, trust-building, parenting focused.",
        "image_prompt": "photorealistic commercial food shot of a cute happy toddler eating sweet juicy mango slice, bright clean natural sunlight, healthy lifestyle, appetizing vibrant yellow mangoes",
        "fallback_caption": "সন্তানের হাসিমুখ আর নিরাপদ স্বাস্থ্যের চেয়ে দামী আর কী হতে পারে? 🥭👶\n\nচাঁদপুর আমঘর নিশ্চিত করে ১০০% ফরমালিন ও কেমিক্যালমুক্ত গাছপাকা আম। কোনো ভেজাল নেই, কোনো বিষ নেই—শিশুদের জন্য সম্পূর্ণ নিরাপদ ও স্বাস্থ্যসম্মত।\n\nঅর্ডার করতে এখনই ইনবক্সে বার্তা দিন।\n\n#চাঁদপুরআমঘর #HealthyKids #ChemicalFree #OrganicMango #ChildSafety"
    },
    {
        "type": "trending_engaging",
        "guidance": "Write a trendy, fun, humorous, and relatable Facebook post in Bengali about mango cravings, summer vibes, and the unmatched love Bangladeshis have for ripe sweet mangoes. Include lots of fun emojis and conversational language.",
        "image_prompt": "creative dynamic food photography of fresh golden amrapali and himsagar mangoes arranged aesthetically with green leaves and water splashes, vibrant pop colors, modern social media visual",
        "fallback_caption": "আমের মৌসুমে যার মুখে হাসি নেই, সে কি আর খাঁটি বাঙালি? 😂🥭\n\nফ্রিজ খুললেই ঠান্ডা মিষ্টি আমের সুবাস—এই লোভ সামলানো কি মুখের কথা! আপনার প্রতিদিনের ম্যাঙ্গো ক্রেভিং মেটাতে চাঁদপুর আমঘর আছে আপনার পাশে।\n\nকার কার এখনই এক বাটি কাটা আম লাগবে? কমেন্টে জানান! 👇\n\n#চাঁদপুরআমঘর #Trending #MangoLover #SummerVibes #BangladeshiFood"
    },
    {
        "type": "variety_spotlight",
        "guidance": "Write a premium product showcase post in Bengali introducing our top varieties (Himsagar, Lengra, Amrapali) freshly harvested from Rajshahi/Chapainawabganj orchards. Focus on aroma, sweetness, and garden freshness.",
        "image_prompt": "commercial luxury fruit photography of freshly harvested ripe himsagar and lengra mangoes in a traditional woven bamboo basket, morning orchard daylight, sharp 8k focus",
        "fallback_caption": "গাছপাকা হিমসাগর নাকি মিষ্টি সুবাসের আম্রপালি—আপনার পছন্দের আম কোনটি? 🥭✨\n\nসরাসরি বাগান থেকে বাছাই করে প্রিমিয়াম কোয়ালিটির তাজা আম পৌঁছে দেওয়া হচ্ছে আপনার বাসায়। কোনো কেমিক্যাল ছাড়া আসল মিষ্টি স্বাদের নিশ্চয়তা!\n\nসীমিত স্টক—অর্ডার করতে দ্রুত ইনবক্স করুন। 📦\n\n#চাঁদপুরআমঘর #Himsagar #Amrapali #FreshFromGarden #PureTaste"
    }
]

def generate_multi_theme_content():
    selected_theme = random.choice(CONTENT_THEMES)
    print(f"🎯 Selected Post Theme: {selected_theme['type']}")
    
    prompt = (
        f"Brand: চাঁদপুর আমঘর (Chandpur Ammghor) - Premium chemical-free mango seller.\n"
        f"Instruction: {selected_theme['guidance']}\n"
        f"Also write a 1-sentence photographic English prompt for an AI image generator matching this theme.\n"
        f"Format strictly as JSON with keys 'caption' and 'image_prompt'. Return ONLY raw JSON without markdown ticks."
    )
    
    caption = ""
    img_prompt = ""
    
    try:
        encoded_prompt = requests.utils.quote(prompt)
        url = f"https://text.pollinations.ai/{encoded_prompt}?json=true"
        res = requests.get(url, timeout=30)
        if res.status_code == 200:
            raw = res.text.strip()
            cleaned = re.sub(r"^```(json)?", "", raw, flags=re.IGNORECASE)
            cleaned = re.sub(r"```$", "", cleaned).strip()
            data = json.loads(cleaned)
            if isinstance(data, dict):
                caption = data.get("caption") or ""
                img_prompt = data.get("image_prompt") or ""
    except Exception as e:
        print(f"⚠️ Text AI fallback: {e}")
        
    if not caption:
        caption = selected_theme["fallback_caption"]
    if not img_prompt:
        img_prompt = selected_theme["image_prompt"]
        
    return caption, img_prompt

def generate_image(prompt):
    print(f"🎨 Generating visual for prompt: {prompt}")
    quality_enhancers = "photorealistic, commercial food photography, 8k, sharp focus, vibrant natural colors, cinematic lighting, no watermark"
    full_prompt = f"{prompt}, {quality_enhancers}"
    encoded = requests.utils.quote(full_prompt)
    seed = random.randint(1000, 999999)
    
    img_url = f"https://image.pollinations.ai/prompt/{encoded}?width=1080&height=1350&model=flux&nologo=true&seed={seed}"
    res = requests.get(img_url, timeout=90)
    
    path = "mango_post.jpg"
    with open(path, "wb") as f:
        f.write(res.content)
    return path

def post_to_facebook_feed(image_path, caption):
    print("🚀 Publishing post to Facebook Page Feed...")
    url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photos"
    with open(image_path, "rb") as img:
        payload = {
            "caption": caption,
            "access_token": FB_PAGE_ACCESS_TOKEN
        }
        files = {"source": img}
        response = requests.post(url, data=payload, files=files, timeout=45)
        
    result = response.json()
    photo_id = result.get("id")
    if photo_id:
        print(f"🎉 Feed Post successfully published! Photo ID: {photo_id}")
        return photo_id
    else:
        print(f"❌ Error publishing feed post: {json.dumps(result, indent=2)}")
        return None

def post_to_facebook_story(photo_id):
    if not photo_id:
        print("⚠️ No valid photo ID found to create story.")
        return

    print(f"📱 Publishing Photo ID {photo_id} to Facebook Page Story...")
    story_url = f"https://graph.facebook.com/v19.0/{FB_PAGE_ID}/photo_stories"
    payload = {
        "photo_id": photo_id,
        "access_token": FB_PAGE_ACCESS_TOKEN
    }
    
    res = requests.post(story_url, data=payload, timeout=30)
    result = res.json()
    
    if result.get("id") or result.get("post_id") or result.get("success"):
        print(f"🎉 Story successfully published! Result: {result}")
    else:
        print(f"⚠️ Story response: {json.dumps(result, indent=2)}")

def main():
    if not FB_PAGE_ID or not FB_PAGE_ACCESS_TOKEN:
        print("❌ Missing credentials.")
        return
        
    caption, img_prompt = generate_multi_theme_content()
    img_file = generate_image(img_prompt)
    
    # 1. Post to Feed (Returns the created Photo ID)
    photo_id = post_to_facebook_feed(img_file, caption)
    
    # 2. Automatically post the exact same image to Story
    if photo_id:
        post_to_facebook_story(photo_id)

if __name__ == "__main__":
    main()
