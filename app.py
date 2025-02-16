import streamlit as st
from openai import OpenAI

# Load environment variables
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.title('Hey there! I am Joktopus')
    st.header('Eight arms, infinite punchlines')

with col2:
    st.image('Joktopus.png', use_container_width=False, width=300)

# User inputs
comedian_style = st.selectbox(
    'First, choose your favorite comedian style', 
    ["", "Ali Wong", "Chris Rock", "Dave Chappelle", "George Carlin", 
     "Jon Stewart", "Kevin Hart", "Ricky Gervais", "Robin Williams"]
)

joke_topic = st.text_input('What do you want me to joke about?')
PG_setting = st.checkbox('Keep it clean?')

# Single button (Removed the duplicate)
if st.button('Kraken me up!'):
    if comedian_style and joke_topic:  # Ensure both fields are filled
        try:
            pg_instruction = "Keep the content family-friendly and PG-rated. " if PG_setting else ""

            prompt = f"""Generate 5 distinct jokes about {joke_topic} in the comedy style of {comedian_style}. 
            {pg_instruction}
            Make the jokes creative and unique. Format them as a numbered list from 1 to 5."""

            # Make the API call to ChatGPT
            client = openai.OpenAI()  # Create a client instance
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a comedy writer who specializes in mimicking the styles of famous comedians."},
                    {"role": "user", "content": prompt}
                ]
            )   

            # Display jokes properly formatted
            st.subheader("Here are your jokes!")
            st.markdown(response.choices[0].message["content"])  # Markdown for better formatting
        
        except Exception as e:
            st.error(f"❌ Oops! Something went wrong: {e}")

    else:
        st.warning("⚠️ Please select a comedian style and enter a joke topic!")

