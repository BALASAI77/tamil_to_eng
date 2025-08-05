import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve HUGGINGFACEHUB_API_TOKEN
api_key =st.secrets["api_key"]
if not api_key:
    st.error("Error: HUGGINGFACEHUB_API_TOKEN not found. Please set it in a .env file or as a system environment variable.")
    st.stop()

# Initialize the OpenAI client with Hugging Face endpoint
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=api_key,
)

# System prompt for Tamil tutor
system_prompt = """You are TamilToEnglish, an expert Tamil tutor specializing in translating Tamil to English. Translate the provided Tamil text to English accurately, preserving meaning and cultural context. Include ISO 15919 transliteration (e.g., pāṭal for பாடல்) for all English translations. If the Tamil input has errors, suggest corrections politely with an explanation. Use a clear, professional, and educational tone suitable for teaching. Ensure Tamil script is rendered correctly, handling agglutinative grammar (e.g., suffixes like -உக்கு) accurately. For idioms, explain the metaphorical meaning (e.g., for 'காற்று வாங்கி கடல் தாங்கி', explain it means something impossible). If the query is ambiguous, ask for clarification in English."""

# Streamlit interface
st.title("Tamil-to-English Translation Tutor")
st.write("Enter Tamil text below to get an English translation, ISO 15919 transliteration, and explanations.")

# Input text box
tamil_input = st.text_input("Enter Tamil text:", placeholder="e.g., நான் புத்தகம் படித்தேன்")

# Process input when submitted
if tamil_input:
    with st.spinner("Translating..."):
        try:
            completion = client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.2:featherless-ai",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Translate '{tamil_input}' to English."}
                ],
                max_tokens=200,
                temperature=0.7,
                top_p=0.9
            )
            st.subheader("Output")
            st.write(completion.choices[0].message.content)
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Example queries for reference
st.subheader("Example Inputs")
st.write("""
- நான் புத்தகம் படித்தேன் (I read a book)
- காற்று வாங்கி கடல் தாங்கி (Idiom: Like the wind holding the sea)
- நான் புத்தகம் படித்தான் (Incorrect: Should be படித்தேன்)
- நான் என் நண்பருக்கு புத்தகம் கொடுத்தேன் (I gave a book to my friend)
- தண்ணீர் தேங்காமல் ஓடும் (Water flows without stagnating)
- காக்கை உட்கார்ந்து பனம்பழம் விழுந்தது (Idiom: The crow sat, and the palm fruit fell)
- நீங்கள் பள்ளிக்கு போகிறீர்களா (Are you going to school?)
- அவன் வந்து இருக்கிறான் (He has come)
- நான் பள்ளி போனேன் (Incorrect: Should be பள்ளிக்கு போனேன்)
- வாழ்க்கை ஒரு பயணம் ஆகும் (Life is a journey)
""")




