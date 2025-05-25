import streamlit as st

# --- Simulated user database ---
USERS = {
    "alice": "password1",
    "bob": "password2",
    "charlie": "password3"
}

AGENTS = {
    "Friendly Bot": "Hi there! How can I help you today?",
    "Tech Support": "Please describe your technical issue.",
    "Joke Bot": "Why did the computer go to the doctor? Because it had a virus!"
}

# --- Session State Initialization ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "show_chat" not in st.session_state:
    st.session_state.show_chat = False
if "selected_user" not in st.session_state:
    st.session_state.selected_user = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

# --- Login Form ---
def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

if not st.session_state.logged_in:
    login()
    st.stop()

# --- Floating Chat Icon ---
chat_icon_style = """
    <style>
    #chat-float {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 100;
    }
    </style>
    <div id="chat-float">
        <button onclick="window.location.reload();" style="background-color:#008CBA;color:white;border:none;padding:15px 20px;border-radius:50%;font-size:24px;cursor:pointer;">💬</button>
    </div>
"""
st.markdown(chat_icon_style, unsafe_allow_html=True)

# Add a regular Streamlit button to open chat
if st.button("Open Chat", key="open_chat"):
    st.session_state.show_chat = True

if st.session_state.show_chat:
    # --- Sidebar with users ---
    st.sidebar.title("Team Members")
    users = [u for u in USERS if u != st.session_state.username]
    selected_user = st.sidebar.radio("Select user to chat", users)
    st.session_state.selected_user = selected_user

    # --- Chat Window ---
    st.title(f"Chat with {selected_user}")

    # Initialize chat history
    chat_key = tuple(sorted([st.session_state.username, selected_user]))
    if chat_key not in st.session_state.chat_history:
        st.session_state.chat_history[chat_key] = []

    # Display chat history
    for sender, msg in st.session_state.chat_history[chat_key]:
        st.write(f"**{sender}:** {msg}")

    # Agent selection and message input
    with st.form("chat_form", clear_on_submit=True):
        agent = st.selectbox("Choose an agent", list(AGENTS.keys()))
        message = st.text_input("Your message")
        submitted = st.form_submit_button("Send")
        if submitted and message:
            # Save user message
            st.session_state.chat_history[chat_key].append((st.session_state.username, message))
            # Agent response
            if agent == "Friendly Bot":
                response = f"{AGENTS[agent]} You said: {message}"
            elif agent == "Tech Support":
                response = f"{AGENTS[agent]} (You: {message})"
            elif agent == "Joke Bot":
                response = AGENTS[agent]
            else:
                response = "Agent not found."
            st.session_state.chat_history[chat_key].append((agent, response))