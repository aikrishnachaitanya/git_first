import streamlit as st

st.title("Chatbot with Agent Selection")

# Agent options
agents = {
    "Friendly Bot": "Hi there! How can I help you today?",
    "Tech Support": "Please describe your technical issue.",
    "Joke Bot": "Why did the computer go to the doctor? Because it had a virus!"
}

# Agent selection
agent = st.selectbox("Choose your agent:", list(agents.keys()))

# User input
user_input = st.text_input("You:", "")

if user_input:
    # Simple agent response logic
    if agent == "Friendly Bot":
        response = f"Friendly Bot: {agents[agent]} You said: {user_input}"
    elif agent == "Tech Support":
        response = f"Tech Support: {agents[agent]} (You: {user_input})"
    elif agent == "Joke Bot":
        response = f"Joke Bot: {agents[agent]}"
    else:
        response = "Agent not found."
    st.write(response)