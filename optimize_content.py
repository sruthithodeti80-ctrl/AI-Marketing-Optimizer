# ============================================================
# ✨ optimize_content.py — Groq LLaMA-3.1 Integration (Optimized)
# ============================================================

import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def optimize_content(base_content, trending_topics):
    """
    Optimize generated marketing content using Groq’s LLaMA-3.1-8B-Instant model.
    Adds trending topics, improves tone and engagement, and enhances readability.
    """

    # Convert the trending topics list into a readable string
    trends = ", ".join(trending_topics)

    # Construct the optimization prompt
    prompt = f"""
    You are a professional social-media marketing strategist.

    Improve the following marketing post so it aligns with these current trends:
    {trends}

    Goals:
    - Make it short, catchy, and audience-focused.
    - Strengthen the call-to-action.
    - Add 2–3 relevant hashtags and emojis for higher engagement.
    - Preserve the original meaning.

    Original Post:
    {base_content}

    Optimized Version:
    """

    print("✨ Optimizing content using Groq LLaMA-3.1 …")

    # Call Groq’s chat completion endpoint
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",   # ✅ Supported Groq model
        messages=[
            {"role": "system", "content": "You are a marketing content optimization expert."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=250
    )

    optimized_text = response.choices[0].message.content.strip()
    print("✅ Optimization complete.")
    return optimized_text
