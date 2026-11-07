import streamlit as st
from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from database.schema import Users
from database.setup import DB_setup

@st.cache_resource
def get_db_setup():
    return DB_setup()

# Create Database Setup 
db = get_db_setup()
db.create_tables()

def login_page():
    with st.form("login", clear_on_submit=False, border=False):
        st.title("Login into RAG System")
        st.text("Login using your organizations id to use this system")
        email = st.text_input(placeholder="Enter email", label="Email", type="email")
        password = st.text_input(placeholder="Enter password", label="Password", type="password")
        submit = st.form_submit_button(label="Submit", width="stretch")
        signup = st.form_submit_button(label="No account? Sign Up", type="tertiary")

        if submit:
            with Session(db.engine) as session:
                user = session.query(Users).filter_by(email_address=email).first()
                if user and user.password == password:
                    st.session_state.email_address = user.email_address
                    st.session_state.name = user.name
                    st.success("Login Successfull!!")
                    st.switch_page(st.Page(RAG_page, title="RAG"))
                elif user.password != password:
                    st.error("Invalid password entered !!")
                else:
                    st.error("User not found !!")
                

        if signup:
            st.switch_page(st.Page(signup_page, title="signup"))

def signup_page():
    with st.form("signup", clear_on_submit=False, border=False):
        st.title("Sign Up into RAG System")
        st.text("Add account to our RAG System")
        name = st.text_input(placeholder="Enter your name", label="Name", type="default")
        input_email = st.text_input(placeholder="Enter email", label="Email", type="email")
        input_password = st.text_input(placeholder="Enter password", label="Password", type="password")
        submit = st.form_submit_button(label="Submit", width="stretch")
        signin = st.form_submit_button(label="Already have an account? Sign In", type="tertiary")

        if submit:
            try:
                with Session(db.engine) as session:
                    user_input = Users(name=name, email_address=input_email, password=input_password)
                    session.add(user_input)
                    session.commit()
                    st.session_state.email_address = input_email
                    st.session_state.name = name
                    st.success("Account creation successfull !!")
            except Exception as e:
                st.empty()
                st.error(f"Unable to create user account. {e}")

        if signin:
            st.switch_page(st.Page(login_page, title="login"))

def RAG_page():
    st.title("RAG QA System")
    st.text("A RAG system designed for organization specific document data retreival")
    with st.sidebar:
        st.button(label=f"{st.session_state.name}", icon=":material/person:")
    
    user_input = st.chat_input("Message here")

    if user_input:
        with st.chat_message(name="user"):
            st.write(user_input)

pages = [login_page, signup_page, RAG_page]

pg = st.navigation(pages, position="hidden")
pg.run()