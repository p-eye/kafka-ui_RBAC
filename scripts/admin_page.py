import logging
import traceback
import pandas as pd
import streamlit as st

from tools.db_tool import DB

db = DB()

def del_user():
    email: str = st.session_state["delete_admin_user"]
    db.delete_user(email)

def add_user():
    email = st.session_state["user_email"]
    type = st.session_state["user_type"]
    db.add_user(email, type)

def show_del_user(col):
    with col:
        delAdminForm = st.form(key='delAdminForm', clear_on_submit=True)
    with delAdminForm:
        st.selectbox(
            "delete email from admin", 
            index=None,
            options=st.session_state["admin_user_data"]["email"], 
            key="delete_admin_user"
        )
        st.form_submit_button(
            label="DELETE", 
            on_click=del_user,
            )

def show_add_user(col):
    add_user_form = col.form(key='add_user_form_key', clear_on_submit=True)
    with add_user_form:
        col1, col2 = st.columns([2, 1])
        col1.text_input('email', key='user_email')
        col2.selectbox("type", ["admin"], key="user_type")
        st.form_submit_button(
            on_click=add_user,
            label="ADD",
            # disabled=not writable,
            # help="For Admin" if not writable else None
            )

def show_users(users, col):
    df = pd.json_normalize(users)
    col.dataframe(
        df,
        width=800,
        hide_index=True,)
    st.session_state["admin_user_data"] = df

def admin_page():
    try:
        users = db.get_users()
        col1, col2 = st.columns([3, 2])
        
        show_users(users, col1)
        show_del_user(col2)
        show_add_user(col2)

    except Exception as e:
        logging.error(f"streamlit : K8S Control Panel : main : Exception : {str(e)}")
        logging.error(f"streamlit : K8S Control Panel : main : traceback : {traceback.format_exc()}")
        st.exception(e)        

