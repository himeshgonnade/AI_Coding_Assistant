import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def call_groq(system_prompt: str, user_message: str, model: str = "llama-3.3-70b-versatile") -> str:
    client = get_groq_client()
    if not client:
        return "⚠️ Please enter your Groq API key in the sidebar to activate AI features."
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {str(e)}"

def call_groq_stream(system_prompt: str, user_message: str, model: str = "llama-3.3-70b-versatile"):
    """Returns a generator for streaming responses."""
    client = get_groq_client()
    if not client:
        yield "⚠️ Please enter your Groq API key in the sidebar to activate AI features."
        return
    try:
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            temperature=0.4,
            max_tokens=2048,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta
    except Exception as e:
        yield f"❌ API Error: {str(e)}"
