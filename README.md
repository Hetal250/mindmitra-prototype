# MindMitra: Mental Wellness Companion for Indian Youth

MindMitra is a Streamlit-based web application designed to support the mental wellness of Indian youth. It provides culturally sensitive responses inspired by the Bhagavad Gita and mindfulness practices like Pranayama, using Google Cloud's Vertex AI for empathetic chatbot interactions.

## Features
- **Mood Tracker**: Log your mood (Happy, Sad, Anxious, Calm, Other) via a sidebar interface.
- **Chatbot**: Engage in supportive conversations with responses tailored to Indian cultural contexts.
- **Personalized Tips**: Generate mental health tips referencing the Gita and mindfulness practices.

## Prerequisites
- Python 3.8+
- Google Cloud account with Vertex AI API enabled
- Streamlit and Google Cloud SDK (`pip install -r requirements.txt`)

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/mindmitra-prototype.git
   cd mindmitra-prototype
   ```
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set Up Google Cloud**:
   - Save your service account key as `sukoon-ai-key.json` (do not commit to Git).
   - Set environment variable:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/sukoon-ai-key.json"  # Linux/macOS
     set GOOGLE_APPLICATION_CREDENTIALS=C:\path\to\sukoon-ai-key.json    # Windows
     ```
4. **Run Locally**:
   ```bash
   streamlit run app.py
   ```
   Access at `http://localhost:8501`.

## Deployment
- Deployed on Streamlit Community Cloud
- Add Google Cloud credentials to Streamlit secrets (see `app.py` for format).
