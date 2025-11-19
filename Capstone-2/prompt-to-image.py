from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

audio_path = Path("uploads/nil.mp3")

with open(audio_path, "rb") as audio_file:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )

print(transcript.text)

safe_prompt = client.chat.completions.create(
    model="gpt-4.1-2025-04-14",
    messages=[
        {
            "role": "system",
            "content": "Rewrite the following text into a safe, non-violent, non-explicit, image-friendly description:"
        },
        {"role": "user", "content": transcript.text}
    ]
)

image_prompt = safe_prompt.choices[0].message.content
print(image_prompt)


result = client.images.generate(
    model="dall-e-2",
    prompt=image_prompt,
    size="512x512",
    n=1
)

print(result.data[0].url)
