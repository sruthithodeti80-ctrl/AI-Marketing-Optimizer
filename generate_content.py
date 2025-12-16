# ============================================================
# ✨ generate_content.py — Groq LLaMA-3.1 Integration (Fixed)
# ============================================================

from dotenv import load_dotenv
load_dotenv()

import os
from groq import Groq

# Initialize Groq client using API key from .env
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_marketing_content(topic, platform="twitter", tone="engaging"):
    """
    Generate marketing content using Groq’s free LLaMA-3.1-8B-Instant model.
    Equivalent functionality to the original OpenAI GPT version.
    """
    prompt = f"""
    You are a professional marketing content creator.
    Generate a {tone} {platform} post about '{topic}'.
    The post should be concise, engaging, audience-focused,
    and include 2–3 relevant hashtags with emojis.
    """

    print("🚀 Generating content using Groq LLaMA-3.1 …")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # ✅ Correct model
        messages=[
            {"role": "system", "content": "You are an expert marketing copywriter."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=250
    )

    content = response.choices[0].message.content.strip()
    print("✅ Content generated successfully.")
    return content
