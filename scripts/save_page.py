
import logging
import traceback

import streamlit as st
from tools.kafkaui_tool import Kafkaui

kafkaui = Kafkaui()

def show_kafkaui_resource(namespace, pod, configmap):
    col1, col2, col3 = st.columns(3)
    col1.selectbox('Namespace', [namespace])
    col2.selectbox('Pod', [pod])
    col3.selectbox('ConfigMap', [configmap])
    st.divider()

def show_kafkaui_role_raw(role_raw, col):
    col.text("config.yml")
    col.code(role_raw)

def show_kafkaui_restart_pod(col):
    if col.button("Restart Pod",
                   type="primary",
                   ):
        kafkaui.restart_pod()

def save_page():
    try:
        namespace, pod, configmap  = kafkaui.get_resource()
        role_raw = kafkaui.get_role_raw()

        show_kafkaui_resource(namespace, pod, configmap)
        col1, col2 = st.columns([4, 1])
        show_kafkaui_role_raw(role_raw, col1)
        show_kafkaui_restart_pod(col2)

    except Exception as e:
        logging.error(f"streamlit : scripts : k8s_page : Exception : {str(e)}")
        logging.error(f"streamlit : scripts : k8s_page : traceback : {traceback.format_exc()}")
        st.exception(e)