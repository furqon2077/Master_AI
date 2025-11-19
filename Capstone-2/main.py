import streamlit as st
from openai import OpenAI
from pathlib import Path
import tempfile
import requests

st.set_page_config(page_title="Voice → Image App", layout="centered")
st.title("🎤 → Voice to Image App")

openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

with st.form("voice_form"):
    uploaded_audio = st.file_uploader("Upload voice file (mp3, wav, m4a)", type=["mp3", "wav", "m4a"])
    submitted = st.form_submit_button("Generate Image")

if submitted:
    if not openai_api_key or not openai_api_key.startswith("sk-"):
        st.warning("⚠ Please enter a valid OpenAI API key in the sidebar.")
        st.stop()

    if not uploaded_audio:
        st.warning("⚠ Please upload an audio file.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)

    suffix = Path(uploaded_audio.name).suffix  # keep .mp3 / .wav / .m4a

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(uploaded_audio.read())
        temp_path = Path(tmp.name)

    st.info("⏳ Transcribing audio…")
    with open(temp_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    st.success("✅ Transcription complete!")
    st.write("**Transcribed Text:**")
    st.write(transcript.text)

    st.info("⏳ Rewriting prompt for safe image generation…")
    safe_prompt = client.chat.completions.create(
        model="gpt-4.1-2025-04-14",
        messages=[
            {
                "role": "system",
                "content":
                        """Your job is to convert ANY input into a completely safe, neutral, non-violent,
                        non-political, non-sexual, family-friendly visual description that complies 100% with strict
                        image-generation safety rules.
                        
                        Rules:
                        - Remove or replace ANY violence, blood, weapons, harm.
                        - Remove ANY sexual or adult content.
                        - Remove political leaders, real people, public figures.
                        - Remove illegal activities.
                        - Remove sensitive demographics.
                        - If user text is unsafe, transform it into something peaceful.
                        - Final output must describe a harmless, positive, imaginative scene suitable for children.
                        
                        If the input cannot be safely converted as-is, reinterpret it creatively into a safe, cartoon-like scene.
                        Always return a safe description — NEVER mention the unsafe content in the final output.
                        """
            },
            {"role": "user", "content": transcript.text}
        ]
    )

    image_prompt = safe_prompt.choices[0].message.content

    st.success("✅ Prompt rewritten!")
    st.write("**Image Prompt:**")
    st.write(image_prompt)

    # Generate the image
    st.info("🎨 Generating image…")
    result = client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1024x1024",
        n=1
    )

    image_url = result.data[0].url

    st.success("✅ Image Generated!")
    st.image(image_url, caption="Generated Image", use_container_width=True)

    response = requests.get(image_url)
    image_bytes = response.content

    st.download_button(
        label="Download Image",
        data=image_bytes,
        file_name="generated_image.png",
        mime="image/png"
    )
