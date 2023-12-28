import logging
import traceback
import pandas as pd
from collections import defaultdict

import streamlit as st
from tools.kafkaui_tool import Kafkaui

kafka_ui = Kafkaui()

def show_users(users, col):
    df = pd.json_normalize(
        users,
    ).transpose().reset_index().rename(columns={'index':'user', 0: 'role'})

    col.dataframe(
        df,
        width=800,
        height=1000,
        hide_index=True
        )
    st.session_state["user_data"] = df

def del_user(roles):
    del_user: str = st.session_state["delete_account"]
    for role in roles:
        role['subjects'] = [x for x in role['subjects'] if x['value'] != del_user]
    return kafka_ui.change(roles)

def show_del_user(roles, col):
    with col:
        delForm = st.form(key='delForm', clear_on_submit=True)
    with delForm:
        st.selectbox(
            "delete user account", 
            index=None,
            options=st.session_state["user_data"]["user"], 
            key="delete_account"
        )
        st.form_submit_button(
            label="DELETE", 
            on_click=del_user,
            args=(roles),
            )

def roles2users(roles):
    '''
    role 기준으로 정렬된 리스트를 user 기준 리스트로 변환합니다.
    '''
    roles_arranged = [{role["name"]: [x["value"] for x in role["subjects"]]} 
                for role in roles if role["name"]]
    users = defaultdict(list)
    for role in roles_arranged:
        for role_name, user_list in role.items():
            for user in user_list:
                users[user].append(role_name)
    return users

def user_page():
    try:
        roles = kafka_ui.get_role()
        users = roles2users(roles)

        col1, col2 = st.columns([3, 2])
        show_users(users, col1)
        show_del_user(roles, col2)

    except Exception as e:
        logging.error(f"streamlit : scripts : user_page : Exception : {str(e)}")
        logging.error(f"streamlit : scripts : user_page : traceback : {traceback.format_exc()}")
        st.exception(e)