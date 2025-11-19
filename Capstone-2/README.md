# 🎤 → Voice to Image App (DALL·E 3) — Capstone Project 2

Convert speech into safe, creative AI-generated images.

🔗 **Live Demo:**
👉 [https://furqon2077-master-ai-capstone-2main-rdypls.streamlit.app/](https://furqon2077-master-ai-capstone-2main-rdypls.streamlit.app/)

---

## 🚀 Overview

The **Voice to Image App** transforms spoken audio into AI-generated images using OpenAI Whisper, GPT-4.1, and DALL·E.
It ensures all outputs are **safe, family-friendly, and image-generation-compliant** by rewriting transcripts through a strict safety prompt system.

---

## 🧩 Features

* 🎙 **Upload Audio** (mp3, wav, m4a, etc.)
* 📝 **Whisper Transcription**
* 🛡 **GPT-4.1 Safe Prompt Rewriting**
* 🎨 **Image Generation (DALL·E 3 / DALL·E 2)**
* 💾 **Download Real Image File** (no corruption)
* 🔁 **Session Persistence** (no content reset on download)
* ⚠️ **Automatic Safety Filtering**

---

## 🛠 Tech Stack

* **Python 3.13**
* **Streamlit**
* **OpenAI Whisper (audio → text)**
* **GPT-4.1 (safe prompt generation)**
* **DALL·E 3 (image generation)**
* **requests** for image downloading

---

## 📦 Installation

```bash
git clone <your-repo-url>
cd your-project-folder

pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run main.py
```

Your app will open automatically at:

```
http://localhost:8501
```

---

## 📁 Project Structure

```
.
├── main.py            # Streamlit application
├── README.md
├── requirements.txt   # Python dependencies
└── .env               # OpenAI API key
```

---

## 🧪 How It Works (Flow)

1️⃣ Upload an audio file
2️⃣ Whisper transcribes speech into text
3️⃣ GPT-4.1 rewrites text into a **safe, child-friendly image prompt**
4️⃣ DALL·E generates an image from that safe prompt
5️⃣ Image is displayed and can be downloaded

---

## 🛡 Safety Compliance

The app automatically removes unsafe elements:

* ❌ Violence
* ❌ Explicit content
* ❌ Real people / political figures
* ❌ Illegal or harmful activity

All outputs become **positive, harmless image descriptions**.
You can download generated image at the end.