import streamlit as st
import requests
import ast


# =========================================================
# CONFIG
# =========================================================

API_URL = "http://localhost:8000"

# User whose department is "Admin" gets Admin Dashboard
ADMIN_DEPARTMENT = "Admin"

st.set_page_config(
    page_title="SecureRAG",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "token": None,
    "logged_in": False,
    "email": "",
    "name": "",
    "department": "",
    "chat_history": [],
    "query_count": 0,
    "source_count": 0,
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CHECK ADMIN
# =========================================================

def is_admin_user():

    department = st.session_state.get(
        "department",
        ""
    )

    return (
        str(department).strip().lower()
        == ADMIN_DEPARTMENT.lower()
    )


# =========================================================
# LOGIN API
# =========================================================

def login_user(email, password):

    try:

        response = requests.post(
            f"{API_URL}/auth/login",
            json={
                "email": email,
                "password": password
            },
            timeout=30
        )

        if response.status_code == 200:

            return response.json()

        return {
            "error": response.text,
            "status": response.status_code
        }

    except requests.exceptions.RequestException as e:

        return {
            "error": str(e)
        }


# =========================================================
# CREATE USER API
# =========================================================

def add_user(
    name,
    email,
    password,
    department
):

    headers = {
        "Authorization": (
            f"Bearer {st.session_state.token}"
        )
    }

    try:

        response = requests.post(
            f"{API_URL}/admin/add-user",

            json={
                "name": name,
                "email": email,
                "password": password,
                "department": department
            },

            headers=headers,

            timeout=30
        )

        try:

            return response.json()

        except ValueError:

            return {
                "error": response.text
            }

    except requests.exceptions.RequestException as e:

        return {
            "error": str(e)
        }


# =========================================================
# RAG QUERY API
# =========================================================

def ask_question(query):

    headers = {
        "Authorization": (
            f"Bearer {st.session_state.token}"
        )
    }

    try:

        response = requests.post(
            f"{API_URL}/rag/query",

            json={
                "query": query
            },

            headers=headers,

            timeout=120
        )

        try:

            return response.json()

        except ValueError:

            return {
                "error": response.text
            }

    except requests.exceptions.RequestException as e:

        return {
            "error": str(e)
        }


# =========================================================
# RENDER SOURCE
# =========================================================

def render_source(source):

    if not source:
        return

    file_name = source.get(
        "file_name",
        "Unknown file"
    )

    department = source.get(
        "department",
        "Unknown"
    )

    # -----------------------------------------------------
    # Handle stringified metadata
    # -----------------------------------------------------

    text_data = source.get(
        "text",
        ""
    )

    if isinstance(
        text_data,
        str
    ):

        try:

            parsed_data = ast.literal_eval(
                text_data
            )

            if isinstance(
                parsed_data,
                dict
            ):

                file_name = parsed_data.get(
                    "file_name",
                    file_name
                )

                department = parsed_data.get(
                    "department",
                    department
                )

        except (
            ValueError,
            SyntaxError,
            TypeError
        ):

            pass

    # -----------------------------------------------------
    # Display source
    # -----------------------------------------------------

    with st.expander(
        "📚 View Retrieved Source"
    ):

        st.write(
            f"**Document:** {file_name}"
        )

        st.write(
            f"**Department:** {department}"
        )


# =========================================================
# LOGOUT
# =========================================================

def logout():

    st.session_state.clear()

    st.rerun()


# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.logged_in:

    

    # -----------------------------------------------------
    # LOGIN
    # -----------------------------------------------------

    st.subheader(
        "🔐 Login"
    )

    email = st.text_input(
        "Email",
        placeholder="Enter your email"
    )

    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter your password"
    )

    login_button = st.button(
        "🔐 Login",
        type="primary",
        use_container_width=True
    )

    # -----------------------------------------------------
    # LOGIN PROCESS
    # -----------------------------------------------------

    if login_button:

        if not email:

            st.warning(
                "Please enter your email."
            )

        elif not password:

            st.warning(
                "Please enter your password."
            )

        else:

            with st.spinner(
                "Logging in..."
            ):

                result = login_user(
                    email,
                    password
                )

            # -------------------------------------------------
            # TOKEN
            # -------------------------------------------------

            token = (
                result.get("token")
                or result.get("access_token")
            )

            if token:

                # ---------------------------------------------
                # SAVE TOKEN
                # ---------------------------------------------

                st.session_state.token = token

                # ---------------------------------------------
                # SAVE EMAIL
                # ---------------------------------------------

                st.session_state.email = result.get(
                    "email",
                    email
                )

                # ---------------------------------------------
                # SAVE NAME
                # ---------------------------------------------

                st.session_state.name = result.get(
                    "name",
                    email
                )

                # ---------------------------------------------
                # SAVE DEPARTMENT
                # ---------------------------------------------

                st.session_state.department = result.get(
                    "department",
                    "General"
                )

                # ---------------------------------------------
                # LOGIN SUCCESS
                # ---------------------------------------------

                st.session_state.logged_in = True

                st.rerun()

            else:

                st.error(
                    result.get(
                        "error",
                        "Invalid email or password"
                    )
                )


# =========================================================
# LOGGED-IN APPLICATION
# =========================================================

else:

    # =====================================================
    # ADMIN CHECK
    # =====================================================

    is_admin = is_admin_user()


    # =====================================================
    # SIDEBAR
    # =====================================================

    with st.sidebar:

        # -------------------------------------------------
        # APPLICATION TITLE
        # -------------------------------------------------

        st.title(
            "🤖 SecureRAG"
        )

        st.caption(
            "Enterprise Knowledge Assistant"
        )

        st.divider()

        # -------------------------------------------------
        # USER PROFILE
        # -------------------------------------------------

        st.subheader(
            "👤 User Profile"
        )

        st.write(
            "**Email**"
        )

        st.caption(
            st.session_state.email
            or "Not available"
        )

        st.write(
            "**Department**"
        )

        st.info(
            st.session_state.department
            or "General"
        )

        # -------------------------------------------------
        # ADMIN INDICATOR
        # -------------------------------------------------

        if is_admin:

            st.success(
                "👑 Administrator"
            )

        else:

            st.caption(
                "👤 Employee"
            )

        st.divider()

        # -------------------------------------------------
        # TECHNOLOGIES
        # -------------------------------------------------

        st.subheader(
            "🛠️ Technologies Used"
        )

        st.write(
            "🔎 **BM25**"
        )

        st.caption(
            "Keyword-based document retrieval"
        )

        st.write(
            "🧠 **Semantic Search**"
        )

        st.caption(
            "Pinecone + Sentence Transformers"
        )

        st.write(
            "🎯 **Re-ranking**"
        )

        st.caption(
            "Improves relevance of retrieved documents"
        )

        st.write(
            "📚 **RAG**"
        )

        st.caption(
            "Retrieval-Augmented Generation"
        )

        st.write(
            "🔐 **JWT + Department Access**"
        )

        st.caption(
            "Department-based document access"
        )

        st.write(
            "⚡ **FastAPI**"
        )

        st.caption(
            "Backend API"
        )

        st.write(
            "🖥️ **Streamlit**"
        )

        st.caption(
            "Frontend interface"
        )

        st.divider()

        # -------------------------------------------------
        # CLEAR CHAT
        # -------------------------------------------------

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.chat_history = []

            st.session_state.query_count = 0

            st.session_state.source_count = 0

            st.rerun()

        # -------------------------------------------------
        # LOGOUT
        # -------------------------------------------------

        if st.button(
            "🚪 Logout",
            use_container_width=True
        ):

            logout()

        st.divider()

        st.caption(
            "🔒 Department Access Protected"
        )

        st.caption(
            "Users can access only authorized "
            "department knowledge."
        )


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    if is_admin:

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        st.title(
            "🛡️ Admin Dashboard"
        )

        st.write(
            f"Welcome, "
            f"**{st.session_state.name or st.session_state.email}**!"
        )

        st.write(
            "Create users and assign department access."
        )

        st.divider()

        # -------------------------------------------------
        # ADMIN METRICS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Account",
                "Administrator"
            )

        with col2:

            st.metric(
                "Department",
                "Admin"
            )

        with col3:

            st.metric(
                "Access",
                "Full"
            )

        st.divider()

        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        st.subheader(
            "👤 Create New User"
        )

        st.write(
            "Create an employee account and assign "
            "department-based access."
        )

        # -------------------------------------------------
        # FORM
        # -------------------------------------------------

        with st.form(
            "create_user_form"
        ):

            new_name = st.text_input(
                "Full Name",
                placeholder="Enter employee name"
            )

            new_email = st.text_input(
                "Email",
                placeholder="employee@company.com"
            )

            new_password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter temporary password"
            )

            new_department = st.selectbox(
                "Department",
                [
                    "HR",
                    "Engineering",
                    "Finance",
                    "Marketing",
                    "Sales",
                    "IT",
                    "General"
                ]
            )

            create_user_button = st.form_submit_button(
                "➕ Create User",
                use_container_width=True
            )

        # -------------------------------------------------
        # CREATE USER
        # -------------------------------------------------

        if create_user_button:

            if not new_name:

                st.warning(
                    "Please enter the user's name."
                )

            elif not new_email:

                st.warning(
                    "Please enter the user's email."
                )

            elif not new_password:

                st.warning(
                    "Please enter a password."
                )

            else:

                with st.spinner(
                    "Creating user..."
                ):

                    result = add_user(
                        name=new_name,
                        email=new_email,
                        password=new_password,
                        department=new_department
                    )

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                else:

                    st.success(
                        f"✅ User {new_email} "
                        f"created successfully!"
                    )

                    st.write(
                        f"**Department:** "
                        f"{new_department}"
                    )

        st.divider()

        st.info(
            "🔐 Administrator access is determined "
            "by department = Admin."
        )


    # =====================================================
    # NORMAL USER / RAG CHAT
    # =====================================================

    else:

        # -------------------------------------------------
        # HEADER
        # -------------------------------------------------

        st.title(
            "💬 Enterprise AI Assistant"
        )

        st.write(
            f"Welcome, "
            f"**{st.session_state.name or st.session_state.email}**!"
        )

        st.write(
            f"Ask questions about your "
            f"**{st.session_state.department or 'department'}** "
            f"documents."
        )

        st.divider()

        # -------------------------------------------------
        # STATUS
        # -------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Department",
                st.session_state.department
                or "General"
            )

        with col2:

            st.metric(
                "Questions",
                st.session_state.query_count
            )

        with col3:

            st.metric(
                "Status",
                "Online"
            )

        st.divider()

        # -------------------------------------------------
        # CHAT
        # -------------------------------------------------

        chat_container = st.container()

        with chat_container:

            # ---------------------------------------------
            # EMPTY CHAT
            # ---------------------------------------------

            if not st.session_state.chat_history:

                st.info(
                    "🧠 Your intelligent knowledge assistant "
                    "is ready. Ask a question below."
                )

            # ---------------------------------------------
            # CHAT HISTORY
            # ---------------------------------------------

            for chat in st.session_state.chat_history:

                # User message

                with st.chat_message(
                    "user"
                ):

                    st.write(
                        chat["question"]
                    )

                # Assistant message

                with st.chat_message(
                    "assistant"
                ):

                    st.markdown(
                        chat["answer"]
                    )

                    source = chat.get(
                        "source"
                    )

                    if source:

                        render_source(
                            source
                        )

        # -------------------------------------------------
        # CHAT INPUT
        # -------------------------------------------------

        query = st.chat_input(
            "Ask anything about your available documents..."
        )

        # -------------------------------------------------
        # PROCESS QUERY
        # -------------------------------------------------

        if query:

            # ---------------------------------------------
            # USER MESSAGE
            # ---------------------------------------------

            with st.chat_message(
                "user"
            ):

                st.write(
                    query
                )

            # ---------------------------------------------
            # ASSISTANT MESSAGE
            # ---------------------------------------------

            with st.chat_message(
                "assistant"
            ):

                with st.spinner(
                    "🔎 Searching knowledge base..."
                ):

                    result = ask_question(
                        query
                    )

                # -----------------------------------------
                # ERROR
                # -----------------------------------------

                if "error" in result:

                    st.error(
                        result["error"]
                    )

                # -----------------------------------------
                # SUCCESS
                # -----------------------------------------

                else:

                    answer = result.get(
                        "answer",
                        "No answer found."
                    )

                    sources = result.get(
                        "sources",
                        []
                    )

                    source = (
                        sources[0]
                        if sources
                        else None
                    )

                    # -------------------------------------
                    # ANSWER
                    # -------------------------------------

                    st.markdown(
                        answer
                    )

                    # -------------------------------------
                    # SOURCE
                    # -------------------------------------

                    if source:

                        render_source(
                            source
                        )

                    # -------------------------------------
                    # COUNTERS
                    # -------------------------------------

                    st.session_state.query_count += 1

                    st.session_state.source_count = (
                        1
                        if source
                        else 0
                    )

                    # -------------------------------------
                    # SAVE CHAT
                    # -------------------------------------

                    st.session_state.chat_history.append(
                        {
                            "question": query,
                            "answer": answer,
                            "source": source
                        }
                    )

                    # -------------------------------------
                    # REFRESH
                    # -------------------------------------

                    st.rerun()