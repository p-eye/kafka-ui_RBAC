import logging
import traceback
import pandas as pd
import json
import streamlit as st
from tools.kafkaui_tool import Kafkaui

kafkaui = Kafkaui()


KAFKAUI_ACTIONS = {
    "applicationconfig": ["view", "edit"],
    "clusterconfig": ["view", "edit"],
    "topic": ["view", "create", "edit", "delete", "messages_read", "messages_produce", "messages_delete"],
    "consumer": ["view", "delete", "reset_offsets"],
    "schema": ["view", "create", "delete", "edit", "modify_global_compatibility"],
    "connect": ["view", "edit", "create", "restart"],
    "ksql": ["execute"],
    "acl": ["view", "edit"],
}

KAFKAUI_NO_VALUES = ["applicationconfig", "clusterconfig", "ksql", "acl"]


def show_roles(roles, col):
    show_role_list = []
    for role in roles:
        show_role_list.append(role.get("name"))
    curr_role_name = col.selectbox(
            'Select Role',
            show_role_list, 
            key='subjects')
    return curr_role_name

def show_role_permission(curr_data):
    """
    role/cluster dataframe
    """
    df = pd.json_normalize(
        curr_data,
        ).rename(columns={'name':'role'})
    st.dataframe(
        df,
        column_order=('role', 'clusters'),
        width=800,
        hide_index=True,
        )
    """
    permission dataframe
    """
    df = pd.json_normalize(
        curr_data, 
        record_path=['permissions'],
        )
    st.dataframe(
        df,           
        column_order=('resource', 'actions', 'value'),
        width=800,
        hide_index=True,
        column_config={
            "resource": st.column_config.Column(width="small"),
            "actions": st.column_config.ListColumn(width="medium"),
            "values": st.column_config.Column(width="medium"),
        }
        )
    
def show_user(curr_data, col):
    """
    user dataframe
    """
    if len(curr_data[0]["subjects"]) == 0: # if no user in role
        st.session_state["role_user_data"] = {'user': []}
    else:
        df = pd.json_normalize(
            curr_data,
            record_path=['subjects'],
        ).sort_values(by=['value']).rename(columns={'value':'user'})

        col.dataframe(
            df,           
            column_order=('type', 'user'),
            width=700,
            hide_index=True,
            )
        st.session_state["role_user_data"] = df

def show_edit_user(curr_role_name, roles, col):
    """
    del user form
    """
    with col:
        delForm = st.form(key='delForm', clear_on_submit=True)
        with delForm:
            st.selectbox(
                "delete user from role", 
                index=None,
                options=st.session_state["role_user_data"]["user"], 
                key="delete_user_from_role_key"
            )
            st.form_submit_button(
                label="DELETE", 
                on_click=del_user_from_role,
                args=(curr_role_name, roles),
                )
    """
    add user form
    """
    with col:
        add_user_form = st.form(key='add_user_form_key', clear_on_submit=True)
        with add_user_form:
            st.text_input('new user to role', key='add_user_to_role_key')
            st.form_submit_button(
                on_click=add_user,
                label='ADD',
                args=(curr_role_name, roles),
                )

def add_user(curr_role_name, roles):
    new_user: str = st.session_state["add_user_to_role_key"]
    new_user_json: json = {
        "provider": "oauth_google",
        "type": "user",
        "value": new_user
    }
    for x_role in roles:
        if (x_role["name"] == curr_role_name):
            x_role['subjects'].append(new_user_json)
    return kafkaui.change(roles)

def del_user_from_role(curr_role_name, roles):
    del_user: str = st.session_state["delete_user_from_role_key"]
    for x_role in roles:
        if (x_role["name"] == curr_role_name):
            x_role['subjects'] = [x for x in x_role['subjects'] if x['value'] != del_user]
    return kafkaui.change(roles)

def del_role(curr_role_name, roles):
    for role in roles:
        if role["name"] == curr_role_name:
            roles.remove(role)
    kafkaui.change(roles)

def show_del_role(curr_role_name, roles):
    st.divider()
    cols = st.columns([4, 1])
    cols[1].button("DELETE ROLE",
              type="primary", 
              on_click=del_role,
              args=(curr_role_name, roles),
    )

def edit_role(curr_role_name, roles):
    form_data = {}
    for key, value in st.session_state.items():
        if "edit_role_" in key:
            trimmed_key = key.split("edit_role_")[1]
            form_data[trimmed_key] = value

    edited_role = {}
    # set clusters, role_name
    edited_role["clusters"] = form_data["clusters"]
    edited_role["name"] = form_data["role"]

    # set permissions
    edited_role["permissions"] = []
    for form_key, form_value in form_data.items(): 
        # form으로부터 action 값이 들어온 resource 설정
        if "action" in form_key and (form_value != None and len(form_value) != 0):
            resource = form_key.split("_")[0]
            permission = {
                "actions": form_value,
                "resource": resource
            }
            edited_role["permissions"].append(permission)

    # set value
    for form_key, form_value in form_data.items():
        # form으로부터 value 값이 들어온 resource에 value 설정 
        if "value" in form_key and (form_value != None and len(form_value) != 0):
            resource = form_key.split("_")[0]
            for permission in edited_role["permissions"]:
                if resource == permission["resource"]:
                    permission["value"] = form_value

    for role in roles:
        if role["name"] == curr_role_name:
            role["name"] = edited_role["name"]
            role["clusters"] = edited_role["clusters"]
            role["permissions"] = edited_role["permissions"]

    return kafkaui.change(roles)

def show_edit_role(curr_role_data, roles):
    cols = st.columns([3, 2])
    edit_role_form = cols[0].form(key='edit_role_form_key', clear_on_submit=True)
    with edit_role_form:
        clusters = kafkaui.get_kafka_clusters()
        st.text_input('role name', curr_role_data["name"], key='edit_role_role')
        st.multiselect("clusters", clusters, key="edit_role_clusters", default=curr_role_data["clusters"])
        st.divider()

        curr_permission = curr_role_data["permissions"]
        curr_resource_list = [x["resource"] for x in curr_permission]

        for key, value in KAFKAUI_ACTIONS.items():
            sub_cols = st.columns([1, 1])
            with sub_cols[0]:
                if key in curr_resource_list:
                    curr_action = [x['actions'] for x in curr_permission if x['resource'] == key][0]
                    if curr_action == ['all']:
                        curr_action = KAFKAUI_ACTIONS[key]
                else:
                    curr_action = None
                st.multiselect(f"{key}_action", value, key=f"edit_role_{key}_action", default=curr_action)

            with sub_cols[1]:
                if key in KAFKAUI_NO_VALUES:
                    st.text_input(f"{key}_value", disabled=True, placeholder="No Value")
                else:
                    if key in curr_resource_list:
                        curr_value = [x['value'] for x in curr_permission if x['resource'] == key][0]
                    else:
                        curr_value = None
                    st.text_input(f"{key}_value", curr_value, key=f"edit_role_{key}_value")

        st.form_submit_button(on_click=edit_role, 
                              label="EDIT",
                              args=(curr_role_data["name"], roles),
                              )

def role_list_page():
    try:
        cols = st.columns([1, 4])
        roles = kafkaui.get_role()
        curr_role_name = show_roles(roles, cols[0])
        curr_role_data = [x_role for x_role in roles if x_role["name"] == curr_role_name]

        tabs = st.tabs(["Permissions", "Users", "Edit"])
        with tabs[0]:
            show_role_permission(curr_role_data)
        with tabs[1]:
            col1, col2 = st.columns([2, 1])
            show_user(curr_role_data, col1)
            show_edit_user(curr_role_name, roles, col2)
        with tabs[2]:
            show_edit_role(curr_role_data[0], roles)
            show_del_role(curr_role_name, roles)

    except Exception as e:
        logging.error(f"streamlit : scripts : role_page : Exception : {str(e)}")
        logging.error(f"streamlit : scripts : role_page : traceback : {traceback.format_exc()}")
        st.exception(e)