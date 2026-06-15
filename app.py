import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Gemini Pro Chat", page_icon="🤖")

st.title("Gemini AI Assistant")

# Use Streamlit Secrets for the API Key
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Please set the GOOGLE_API_KEY in Streamlit Secrets.")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is on your mind?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # --- UPDATED PART: ERROR CATCHER ---
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        # This will now show the REAL error on your website screen
        st.error(f"⚠️ API Error: {e}")
    # -----------------------------------
