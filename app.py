import streamlit as st
import requests
import ast


# =========================================================
# CONFIG
# =========================================================

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",  # force sidebar open by default
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "token": None,
    "logged_in": False,
    "email": "",
    "department": "",
    "chat_history": [],
    "query_count": 0,
    "source_count": 0,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# API FUNCTIONS
# =========================================================

def login_user(email, password):
    try:
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": email, "password": password},
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()
        return {"error": response.text, "status": response.status_code}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def add_user(name, email, password, department):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        response = requests.post(
            f"{API_URL}/admin/add-user",
            json={
                "name": name,
                "email": email,
                "password": password,
                "department": department,
            },
            headers=headers,
            timeout=30,
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def ask_question(query):
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        response = requests.post(
            f"{API_URL}/rag/query",
            json={"query": query},
            headers=headers,
            timeout=120,
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def render_source(source):
    """Render a single source block inside an expander."""
    file_name = source.get("file_name", "Unknown file")
    department = source.get("department", "Unknown")
    

    text_data = source.get("text", "")
    if isinstance(text_data, str):
        try:
            parsed_data = ast.literal_eval(text_data)
            if isinstance(parsed_data, dict):
                file_name = parsed_data.get("file_name", file_name)
                department = parsed_data.get("department", department)
                
        except ( SyntaxError, TypeError):
            pass


    with st.expander("📚 View Retrieved Source"):
        st.write(f"**Document:** {file_name}")
        st.write(f"**Department:** {department}")
        


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:



    st.subheader("🔐 Login")

    email = st.text_input("Email", placeholder="Enter your email")
    password = st.text_input(
        "Password", type="password", placeholder="Enter your password"
    )

    login_button = st.button("🔐 Login", type="primary", use_container_width=True)

    if login_button:
        if not email or not password:
            st.warning("Please enter email and password.")
        else:
            with st.spinner("Logging in..."):
                result = login_user(email, password)

            # Accept either "token" or "access_token" from the backend
            token = result.get("token") or result.get("access_token")

            if token:
                st.session_state.token = token
                st.session_state.email = result.get("email", email)
                st.session_state.department = result.get("department", "General")
                
                
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error(result.get("error", "Invalid email or password"))


# =========================================================
# LOGGED-IN APPLICATION (SIDEBAR + MAIN CHAT WINDOW)
# =========================================================

else:

    # -----------------------------------------------------
    # SIDEBAR
    # -----------------------------------------------------
    with st.sidebar:

        
        st.title("SecureRAG")
        st.info("Role-Based Access Control • Semantic Search • BM25 • Re-Ranking • RAG")
        
        st.divider()

        st.subheader("👤 User Profile")
        

        st.write("**Email**")
        st.caption(st.session_state.email or "Not available")

        st.write("**Department**")
        st.info(st.session_state.department or "General")

        

        st.divider()

        st.subheader("🛠️ Technologies Used")
        st.write("🔎 **BM25**")
        st.caption("Keyword-based document retrieval")
        st.write("🧠 **Semantic Search**")
        st.caption("Pinecone + Sentence Transformers")
        st.write("🎯 **Re-ranking**")
        st.caption("Improves relevance of retrieved documents")
        st.write("📚 **RAG**")
        st.caption("Retrieval-Augmented Generation")
        

        st.divider()

        col_a = st.columns(1)

        

        with col_a[0]:
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.clear()
                st.rerun()

        st.divider()
        st.caption("🔒 RBAC Protected")
        st.caption("Users can access only authorized department knowledge.")

    # -----------------------------------------------------
    # MAIN AREA: HEADER + STATUS
    # -----------------------------------------------------

    st.write(
        f"Welcome, **{st.session_state.email or 'User'}**!\n "
        f"Ask questions about your "
        f"**{st.session_state.department or 'department'}** documents."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Department", st.session_state.department or "General")
    with col2:
        st.metric("Questions", st.session_state.query_count)
    with col3:
        st.metric("Status", "Online")

    st.divider()

    # -----------------------------------------------------
    # MAIN AREA: CHAT WINDOW
    # -----------------------------------------------------

    chat_container = st.container()

    with chat_container:

        if not st.session_state.chat_history:
            st.info(
                "🧠 Your intelligent knowledge assistant is ready."
            )

        col_a = st.columns(1)

        with col_a[0]:
            if st.button("🗑️ Clear", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.query_count = 0
                st.session_state.source_count = 0
                st.rerun()    

        for chat in st.session_state.chat_history:
            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):
                st.markdown(chat["answer"])
                source = chat.get("source")
                if source:
                    render_source(source)

    # -----------------------------------------------------
    # CHAT INPUT (pinned to bottom by Streamlit automatically)
    # -----------------------------------------------------

    query = st.chat_input("Ask anything about your available documents..")

    if query:
        with st.chat_message("user"):
            st.write(query)

        with st.chat_message("assistant"):
            with st.spinner("🔎 Searching knowledge base..."):
                result = ask_question(query)

            if "error" in result:
                st.error(result["error"])
            else:
                answer = result.get("answer", "No answer found.")
                sources = result.get("sources", [])
                source = sources[0] if sources else None

                st.markdown(answer)
                if source:
                    render_source(source)

                st.session_state.query_count += 1
                st.session_state.source_count = 1 if source else 0

                st.session_state.chat_history.append(
                    {"question": query, "answer": answer, "source": source}
                )

                st.rerun()