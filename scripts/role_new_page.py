import logging
import traceback

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

def create_role():
    form_data = {}
    for key, value in st.session_state.items():
        if "create_role_" in key:
            trimmed_key = key.split("create_role_")[1]
            form_data[trimmed_key] = value

    new_role = {}
    # set clusters, role_name
    new_role["clusters"] = form_data["clusters"]
    new_role["name"] = form_data["role"]

    # set permissions
    new_role["permissions"] = []
    for form_key, form_value in form_data.items(): 
        # form으로부터 action 값이 들어온 resource 설정
        if "action" in form_key and len(form_value) != 0:
            resource = form_key.split("_")[0]
            permission = {
                "actions": form_value,
                "resource": resource
            }
            new_role["permissions"].append(permission)

    # set value
    for form_key, form_value in form_data.items():
        # form으로부터 value 값이 들어온 resource에 value 설정 
        if "value" in form_key and len(form_value) != 0:
            resource = form_key.split("_")[0]
            for permission in new_role["permissions"]:
                if resource == permission["resource"]:
                    permission["value"] = form_value

    # set empty subject
    new_role["subjects"]=[]

    kafkaui.add(new_role)

def show_create_role(col):
    create_role_form = col.form(key='create_role_form_key', clear_on_submit=True)
    with create_role_form:
        clusters = kafkaui.get_kafka_clusters()
        st.text_input('role name', key='create_role_role')
        st.multiselect("clusters", clusters, key="create_role_clusters")
        st.divider()

        for key, value in KAFKAUI_ACTIONS.items():
            sub_cols = st.columns([1, 1])
            with sub_cols[0]:
                st.multiselect(f"{key}_action", value, key=f"create_role_{key}_action")
            with sub_cols[1]:
                if key in KAFKAUI_NO_VALUES:
                    st.text_input(f"{key}_value", disabled=True, placeholder="No Value")
                else:
                    st.text_input(f"{key}_value", key=f"create_role_{key}_value")

        st.form_submit_button(on_click=create_role, 
                              label="CREATE",
                              )

def role_new_page():
    try:
        cols = st.columns([3, 2])
        show_create_role(cols[0])

    except Exception as e:
        logging.error(f"streamlit : scripts : role_new_page : Exception : {str(e)}")
        logging.error(f"streamlit : scripts : role_new_page : traceback : {traceback.format_exc()}")
        st.exception(e)