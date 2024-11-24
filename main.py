import os
import base64
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai

# Load environment variables
load_dotenv()

# Configure Streamlit page settings
st.set_page_config(
    page_title="GemAi- 2.0",
    page_icon="excited.png",  # Placeholder for favicon
    layout="wide",        # Use wide layout for better visuals
)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Load the logo image
def load_logo(file_path):
    with open(file_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_image

# Replace with your uploaded logo file path
logo_path = "excited.png"  # Header logo
logo_base64 = load_logo(logo_path)

# Custom header with logo and text
st.markdown(
    f"""
    <style>
    .header-font {{
        font-family: 'Courier New', monospace;
        font-size: 30px;
        color: #ADD8E6;
        text-align: center;
    }}
    .header-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }}
    .logo {{
        width: 50px;
        height: 50px;
        margin-right: 15px;
    }}
    </style>
    <div class="header-container">
        <img src="data:image/png;base64,{logo_base64}" class="logo" alt="Gemini Pro Logo">
        <span class="header-font">GemAi- 2.0<span>
    </div>
    """,
    unsafe_allow_html=True,
)

# Initialize chat session and history if not already present
if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])
    st.session_state.messages = []  # Store chat history

# Show welcome text only if there are no user messages
if not st.session_state.messages:
    st.markdown(
        """
        <div style="text-align: center; margin-top: 20px; font-family: 'Courier New', monospace; font-size: 24px; color: var(--text-color);">
            What secrets of the universe shall we unveil?
        </div>
        """,
        unsafe_allow_html=True,
    )

# Display the chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field for user's message
user_prompt = st.chat_input("Type your message here...")
if user_prompt:
    # Add user's message to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    st.chat_message("user").markdown(user_prompt)

    # Send user's message to Gemini-Pro and get the response
    gemini_response = st.session_state.chat_session.send_message(user_prompt)

    # Add Gemini-Pro's response to history
    st.session_state.messages.append({"role": "assistant", "content": gemini_response.text})
    with st.chat_message("assistant"):
        st.markdown(gemini_response.text)
