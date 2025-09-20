import streamlit as st
import random
from google.cloud import aiplatform
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
import os

# Custom CSS for navy blue and white theme
st.markdown("""
<style>
    /* Global styles */
    body {
        background-color: #1A2A44; /* Navy blue background */
        font-family: 'Noto Sans', sans-serif;
        color: #FFFFFF;
    }
    .main {
        background-color: #FFFFFF; /* White main content */
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
        color: #1A2A44; /* Navy text on white */
    }
    /* Header styling */
    .stTitle {
        color: #1A2A44; /* Navy title */
        font-size: 3em;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.1em;
    }
    .stSubheader {
        color: #2E8B88; /* Teal accent for subheader */
        font-size: 1.8em;
        text-align: center;
        margin-top: 0.3em;
        font-style: italic;
    }
    /* Sidebar styling with navy and light mood tracker */
    .css-1d391kg {
        background-color: #1A2A44; /* Navy sidebar */
        border-right: 3px solid #2E8B88; /* Teal border */
        padding: 20px;
        border-radius: 10px 0 0 10px;
    }
    .stSidebar .stSelectbox {
        background-color: #E6F0FA; /* Light blue for mood tracker */
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border: 2px solid #2E8B88;
        color: #1A2A44;
    }
    .stSidebar .stButton {
        background-color: #FFFFFF;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 20px;
        border: 2px solid #2E8B88;
    }
    .stSidebar .stButton button {
        background-color: #2E8B88; /* Teal button */
        color: #FFFFFF;
        border-radius: 12px;
        width: 100%;
        font-weight: 600;
        transition: transform 0.3s ease;
    }
    .stSidebar .stButton button:hover {
        background-color: #1A2A44; /* Navy on hover */
        transform: scale(1.05);
    }
    /* Chat interface */
    .stChatMessage {
        border-radius: 15px;
        margin-bottom: 20px;
        padding: 20px;
        animation: fadeIn 0.5s ease-in-out;
        background: #F9FAFB; /* Light gray background for chat */
        border: 2px solid #2E8B88;
        color: #1A2A44;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .stChatMessage[data-testid="chatAvatarIcon-assistant"] {
        border-left: 5px solid #2E8B88;
    }
    .stChatMessage[data-testid="chatAvatarIcon-user"] {
        border-right: 5px solid #2E8B88;
    }
    .stChatInput input {
        border: 2px solid #2E8B88;
        border-radius: 12px;
        padding: 12px;
        background-color: #FFFFFF;
        color: #1A2A44;
        font-size: 1em;
        transition: border-color 0.3s ease;
    }
    .stChatInput input:focus {
        border-color: #1A2A44;
        outline: none;
    }
    /* Resource section */
    .stMarkdown h2 {
        color: #1A2A44;
        font-size: 2.2em;
        margin-top: 30px;
        border-bottom: 3px solid #2E8B88;
        padding-bottom: 8px;
        text-align: center;
    }
    .stMarkdown p {
        color: #1A2A44;
        font-size: 1.2em;
        line-height: 1.8;
        text-align: justify;
    }
    /* Button for personalized tip */
    .stButton button {
        background-color: #2E8B88; /* Teal button */
        color: #FFFFFF;
        border-radius: 12px;
        padding: 15px 30px;
        font-size: 1.2em;
        font-weight: 600;
        box-shadow: 0 4px 15px rgba(46, 139, 136, 0.4);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #1A2A44; /* Navy on hover */
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26, 42, 68, 0.6);
    }
    /* Footer */
    .stCaption {
        color: #2E8B88;
        text-align: center;
        margin-top: 40px;
        font-size: 1em;
        font-style: italic;
    }
    /* Custom styling for info box */
    .stInfo {
        background-color: #E6F0FA;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #2E8B88;
        color: #1A2A44;
    }
</style>
""", unsafe_allow_html=True)

# Define varied culturally sensitive responses
responses = {
    "sad": [
        "Take heart, as the Bhagavad Gita (Chapter 18, Verse 66) teaches us to surrender our sorrows to a higher wisdom. Try a gentle Pranayama breathing exercise: inhale for 4, hold for 4, exhale for 4.",
        "In times of sadness, remember Krishna’s guidance in the Gita—focus on the present moment. A short meditation can bring peace; sit quietly for 5 minutes.",
        "The Gita (Chapter 6, Verse 5) reminds us to uplift ourselves. If you’re feeling down, try chanting 'Om' softly to restore calm."
    ],
    "anxious": [
        "Like Arjuna’s anxiety in the Gita, yours too shall pass with action. Practice deep breathing: inhale for 4, hold for 4, exhale for 6, to ease your mind.",
        "The Gita (Chapter 2, Verse 38) teaches equanimity. When anxious, try a 5-minute mindfulness walk, focusing on your steps.",
        "Ayurveda suggests calming with warm water and tulsi tea. The Gita also guides us to let go of worry—trust in your strength."
    ],
    "happy": [
        "Wonderful to hear! The Gita (Chapter 12, Verse 13) celebrates joy in helping others. Share your happiness with a kind act today!",
        "Your happiness shines like the wisdom in the Gita. Maintain it with a gratitude meditation—list 3 things you’re thankful for.",
        "As the Gita teaches balance, enjoy your joy! Try a light yoga stretch to keep the energy flowing."
    ],
    "calm": [
        "Your calm reflects the Gita’s teaching of inner peace (Chapter 6, Verse 10). Deepen it with 5 minutes of silent meditation.",
        "The Gita (Chapter 2, Verse 64) praises steady minds. Stay calm with a mindful tea ritual—sip slowly and breathe.",
        "Ayurveda values your tranquility. Enhance it with a walk in nature, as the Gita suggests harmony with all."
    ],
    "default": [
        "Like in the Bhagavad Gita, Chapter 2, Verse 47, focus on action, not results. Try meditating for calm.",
        "The Gita (Chapter 18, Verse 13) guides us through life’s actions. Take a moment to breathe deeply and reflect.",
        "Draw strength from the Gita’s wisdom—act with purpose. A short Pranayama session can ground you."
    ]
}
# Define mood-specific insights
insights = {
    "😊 Happy": "Celebrate your joy—share it with someone today, as the Gita (Ch. 12, V. 13) suggests.",
    "😢 Sad": "Let the Gita’s wisdom (Ch. 18, V. 66) guide you—try a 5-minute meditation.",
    "😟 Anxious": "Ease your mind with Pranayama: inhale for 4, hold for 4, exhale for 4, per Gita’s calm.",
    "😌 Calm": "Deepen your peace with a mindful walk, as the Gita (Ch. 6, V. 10) teaches.",
    "Other": "Reflect quietly—find balance with the Gita’s inner strength."
}

# Initialize Vertex AI (falls back to mock if API fails)
def generate_response(prompt):
    if 'GOOGLE_APPLICATION_CREDENTIALS' in os.environ:
        try:
            aiplatform.init(project='vertex-ai-demo-472710', location='us-central1')
            model = aiplatform.gapic.PredictionServiceClient()
            endpoint = f"projects/vertex-ai-demo-472710/locations/us-central1/models/gemini-1.0-pro"
            content = {
                "instances": [{"content": prompt}],
                "parameters": {
                    "temperature": 0.7,
                    "maxTokens": 1024,
                    "topP": 0.95,
                },
            }
            request = json_format.ParseDict(content, Value())
            response = model.predict(endpoint=endpoint, instances=[request])
            return response.predictions[0].content if hasattr(response.predictions[0], 'content') else "No valid response."
        except Exception as e:
            mood = next((m for m in responses if m in prompt.lower()), "default")
            return f"API Error: {str(e)}. Fallback: {random.choice(responses[mood])}"
    else:
        mood = next((m for m in responses if m in prompt.lower()), "default")
        return f"Mock response: {random.choice(responses[mood])}"

# Streamlit App
st.title("MindMitra: Your Mental Wellness Companion")
st.subheader("Empowering Indian Youth with Cultural Wisdom")

# Sidebar for Mood Tracker
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.write("🌸 Mood Tracker")
    mood = st.selectbox("How are you feeling today? 😊", ["😊 Happy", "😢 Sad", "😟 Anxious", "😌 Calm", "Other"], help="Select your current mood to log it.")
    if st.button("Log Mood"):
        st.session_state.current_mood = mood
        st.success(f"Mood logged: {mood}. {insights[mood]}")
    st.markdown('</div>', unsafe_allow_html=True)

# Main Chatbot
st.header("💬Chat with Your Mitra")
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    full_prompt = f"Respond empathetically as a companion for Indian youth mental health. Reference Bhagavad Gita, meditation (e.g., Pranayama), or Ayurveda if relevant. Keep it supportive, non-diagnostic. User: {prompt}"
    with st.chat_message("assistant"):
        response = generate_response(full_prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Resource Page
if st.button("Generate Personalized Tip"):
    tip_prompt = "Generate a short, culturally sensitive mental health tip with Gita reference."
    tip = generate_response(tip_prompt)
    st.info(tip)