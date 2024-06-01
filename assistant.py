import streamlit as st
from fetchScheduleData import scheduleQuestions
from openAIFunction import bot_calling_functions

st.title("Krish's Meeting Scheduler")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] == "user":
        st.write(f"User: {message['content']}")
    elif message["role"] == "assistant":
        st.write(f"Assistant: {message['content']}")

# Accept user input
prompt = st.text_input("Hello, how are you doing today?")
if prompt:
    # Display user message in chat message container
    st.write(f"User: {prompt}")
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.spinner("Thinking..."):
        print("Hello")
        response = bot_calling_functions(prompt)
        if response:
            st.write(f"Assistant: {response}")
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            st.warning("Sorry, I couldn't generate a response. Please try again.")



