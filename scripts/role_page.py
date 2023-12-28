import logging
import traceback

import streamlit as st

from scripts.role_list_page import role_list_page
from scripts.role_new_page import role_new_page
from streamlit_option_menu import option_menu

def role_page():
    try:
        selected_tab = option_menu(
                    None,
                    ["Roles", "Create New Role"], 
                    icons= ['hdd-stack', 'plus-circle-fill'],
                    orientation= "horizontal"
                    ) 

        if selected_tab == 'Roles':
            role_list_page()
        if selected_tab == "Create New Role":
            role_new_page()

    except Exception as e:
        logging.error(f"streamlit : scripts : role_page : Exception : {str(e)}")
        logging.error(f"streamlit : scripts : role_page : traceback : {traceback.format_exc()}")
        st.exception(e)