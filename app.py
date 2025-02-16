import streamlit as st
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Validate API Key
if not api_key:
    st.error("⚠️ OpenAI API key not found! Please check your .env file.")
    st.stop()  # Stop execution if API key is missing

# ---- Authentication Setup ----
# Hardcoded credentials (For testing only! Use a database in production)
USER_CREDENTIALS = {
    "admin": "password123",
    "guest": "joketopushero"
}

# Check if user is authenticated
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

def login():
    """Authenticate user"""
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", type="password", key="password")

    if st.button("Login"):
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"✅ Welcome, {username}!")
            st.experimental_rerun()  # Refresh page after login
        else:
            st.error("❌ Invalid username or password")

def logout():
    """Logout function"""
    st.session_state.authenticated = False
    st.session_state.username = ""
    st.experimental_rerun()

# ---- App Authentication Logic ----

if not st.session_state.authenticated:
    login()
else:
    # Show logout button
    st.sidebar.button("Logout", on_click=logout)

# Initialize OpenAI Client
client = openai.OpenAI(api_key=api_key)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.title('Hey there! I am Joktopus')
    st.header('Eight arms, infinite punchlines')

with col2:
    st.image('Joktopus.png', use_container_width=False, width=300)

# User Inputs
comedian_style = st.selectbox(
    'First, choose your favorite comedian style', 
    ["", "Ali Wong", "Chris Rock", "Dave Chappelle", "George Carlin", 
     "Jon Stewart", "Kevin Hart", "Ricky Gervais", "Robin Williams"]
)

joke_topic = st.text_input('What do you want me to joke about?')
PG_setting = st.checkbox('Keep it clean?')

# Generate jokes on button press
if st.button('Kraken me up!'):
    if comedian_style and joke_topic:  # Ensure both fields are filled
        try:
            # Construct Prompt
            pg_instruction = " Keep the content family-friendly and PG-rated." if PG_setting else ""
            prompt = (
                f"Generate 5 distinct jokes about {joke_topic} in the comedy style of {comedian_style}."
                f"{pg_instruction} Make the jokes creative and unique. Format them as a numbered list from 1 to 5."
            )

            # API Call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a comedy writer who specializes in mimicking the styles of famous comedians."},
                    {"role": "user", "content": prompt}
                ]
            )

            # Display Jokes
            st.subheader("Here are your jokes!")
            st.markdown(response.choices[0].message.content)  # Markdown for better formatting
        
        except Exception as e:
            st.error(f"❌ Oops! Something went wrong: {e}")

    else:
        st.warning("⚠️ Please select a comedian style and enter a joke topic!")
