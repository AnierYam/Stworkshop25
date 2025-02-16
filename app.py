import streamlit as st
import openai
import os
import json
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Validate API Key
if not api_key:
    st.error("⚠️ OpenAI API key not found! Please check your .env file.")
    st.stop()  # Stop execution if API key is missing

# ---- Authentication Setup ----
USER_DB_FILE = "users.json"

def load_users():
    """Load user credentials from JSON file."""
    if not Path(USER_DB_FILE).exists():
        return {}
    with open(USER_DB_FILE, "r") as file:
        return json.load(file)

def save_users(users):
    """Save updated user credentials to JSON file."""
    with open(USER_DB_FILE, "w") as file:
        json.dump(users, file, indent=4)

def signup():
    """Signup new users and save credentials securely."""
    st.subheader("Sign Up")
    new_username = st.text_input("Choose a Username", key="signup_username")
    new_password = st.text_input("Choose a Password", type="password", key="signup_password")

    if st.button("Sign Up"):
        users = load_users()
        
        if new_username in users:
            st.error("❌ Username already exists. Try a different one.")
        elif new_username and new_password:
            users[new_username] = new_password  # Store password (Note: Hashing needed for production)
            save_users(users)
            st.success("✅ Signup successful! Please log in.")
            st.experimental_rerun()
        else:
            st.error("⚠️ Both fields are required!")

def login():
    """Authenticate existing users."""
    st.subheader("Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        users = load_users()

        if username in users and users[username] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.success(f"✅ Welcome back, {username}!")
            st.experimental_rerun()  # Refresh page after login
        else:
            st.error("❌ Invalid username or password")

def logout():
    """Logout function"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.experimental_rerun()

# ---- App Authentication Logic ----
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.sidebar.title("🔐 Authentication")
    auth_choice = st.sidebar.radio("Choose an option:", ["Login", "Sign Up"])

    if auth_choice == "Login":
        login()
    else:
        signup()
else:
    # Show logout button
    st.sidebar.button("Logout", on_click=logout)

    # ---- Main App Layout ----
    col1, col2 = st.columns(2)

    with col1:
        st.title('Hey there! I am Joktopus')
        st.header('Eight arms, infinite punchlines')

    with col2:
        st.image('Joktopus.png', use_container_width=True, width=300)

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

                # Initialize OpenAI Client
                client = openai.OpenAI(api_key=api_key)

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
