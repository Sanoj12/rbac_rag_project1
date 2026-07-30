import streamlit as st
import requests

# ---------------- CONFIG ---------------- #

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- SESSION ---------------- #

if "token" not in st.session_state:
    st.session_state.token = None

if "department" not in st.session_state:
    st.session_state.department = None

# ---------------- API FUNCTIONS ---------------- #

def login_user(email, password):

    response = requests.post(
        f"{API_URL}/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    if response.status_code == 200:
        return response.json()

    return {
        "error": response.text,
        "status": response.status_code
    }


def add_user(name, email, password, department):

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(
        f"{API_URL}/admin/add-user",
        json={
            "name": name,
            "email": email,
            "password": password,
            "department": department
        },
        headers=headers
    )

    return response.json()


def ask_question(query):

    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(
        f"{API_URL}/rag/query",
        json={
            "query": query
        },
        headers=headers
    )

    return response.json()

# ---------------- LOGIN PAGE ---------------- #

if st.session_state.token is None:

   

        st.markdown("<div class='card'>",unsafe_allow_html=True)

        st.subheader("Login")

        email=st.text_input("Email")

        password=st.text_input(
            "Password",
            type="password"
        )

        if st.button("Login"):

            with st.spinner("Authenticating..."):

                result=login_user(email,password)

            if "token" in result:

                st.success("Login Successful")

                st.session_state.token=result["token"]

                st.session_state.department=result["department"]
                
                st.session_state.user_name = email 
                
                st.rerun()

            else:

                st.error("Invalid Credentials")

        st.markdown("</div>",unsafe_allow_html=True)

# ---------------- AFTER LOGIN ---------------- #

else:

   # ---------------- MAIN PAGE ---------------- #

 if st.session_state.department == "admin":

    st.title("👨‍💼 Admin Dashboard")
    st.caption("Manage users for the Enterprise RBAC RAG System")

    # Dashboard Cards
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Role", "Administrator")

    with col2:
        st.metric("Departments", "5")

    with col3:
        st.metric("Status", "Active")

    st.divider()

    st.subheader("➕ Create New User")

    with st.container(border=True):

        with st.form("add_user_form"):

            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("👤 Full Name")

            with col2:
                email = st.text_input("📧 Email")

            password = st.text_input(
                "🔑 Password",
                type="password"
            )

            department = st.selectbox(
                "🏢 Department",
                [
                    "hr team",
                    "engineering",
                    "finance",
                    "general",
                    "marketing"
                ]
            )

            submitted = st.form_submit_button(
                "✅ Create User",
                use_container_width=True
            )

        if submitted:

            with st.spinner("Creating User..."):

                result = add_user(
                    name,
                    email,
                    password,
                    department
                )

            if "error" in result:

                st.error(result["error"])

            else:

                st.success("User Created Successfully 🎉")

                st.json(result)

 else:

    st.title("🤖 Enterprise AI Assistant")

    st.caption(
        f"Welcome **{st.session_state.user_name}**  |  Department: **{st.session_state.department.title()}**"
    )

    

    st.divider()

    st.subheader("💬 Ask AI")

    query = st.text_area(
        "",
        height=180,
        placeholder="Example: What is the leave policy?"
    )

    if st.button(
        "🚀 Ask AI",
        use_container_width=True
    ):

        if query.strip() == "":

            st.warning("Please enter a question.")

        else:

            with st.spinner("Searching Knowledge Base..."):

                result = ask_question(query)

            if "error" in result:

                st.error(result["error"])

            else:

                st.chat_message("user").write(query)

                st.chat_message("assistant").write(
                    result["answer"]
                )