import streamlit as st
import requests
import uuid

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Financial Budget Assistant")

# Chat interface
st.write("Welcome! Let me help you organize your budget.")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display user message
    with st.chat_message("user"):
        st.write(prompt)

    try:
        # Send message to FastAPI backend
        response = requests.post(
            "http://localhost:8000/chat/",
            json={"message": prompt, "session_id": st.session_state.session_id},
        )

        if response.status_code == 200:
            bot_message = response.json()["bot_response"]

            # Add bot response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": bot_message}
            )

            # Display bot response
            with st.chat_message("assistant"):
                st.write(bot_message)
        else:
            st.error("Error communicating with the chatbot")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Add a button to clear chat history
if st.button("Clear Chat"):
    st.session_state.messages = []
    # Clear backend chat history
    requests.delete(f"http://localhost:8000/chat/{st.session_state.session_id}")
    st.rerun()
