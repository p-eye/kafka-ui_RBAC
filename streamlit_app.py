import logging
import traceback

import streamlit as st
from streamlit_option_menu import option_menu

from scripts.save_page import save_page
from scripts.role_page import role_page
from scripts.user_page import user_page
from scripts.admin_page import admin_page
from scripts.common.login_ui import login_ui, get_login_user

from tools.db_tool import DB
from streamlit.errors import StreamlitAPIException 

# set wide page
try: 
    st.set_page_config(layout= "wide", menu_items= {}, page_icon= "media/K8s Control Panel.png")
except StreamlitAPIException as e:
    logging.info(e)

_COOKIE_KEY = 'C_OAUTH'
db = DB()

def show_unauthorized():
    st.error("Unauthorized")

def show_menu():
    menu_list = ["Role", "User", "Save Changes", "Admin"]
    icon_list = ["hdd-stack", "person-circle", "play-circle-fill", "gear"]
    
    with st.sidebar:
        selected_tab = option_menu(None, options=menu_list, icons=icon_list)
    if selected_tab == 'User':
        user_page()
    if selected_tab == 'Role':
        role_page()
    if selected_tab == 'Save Changes':
        save_page()
    if selected_tab == "Admin":
        admin_page()

def main():
    try:
        logout_clicked = login_ui()
        login_user = get_login_user()
        if (logout_clicked == False) and (_COOKIE_KEY in st.session_state):
            if login_user in [x['email'] for x in db.get_users()]:
                # viewer, admin 구분
                # user_type = [x['type'] for x in db.get_users() if x['email'] == login_user][0]
                # writable = True if user_type == 'admin' else False
                show_menu()
            else:
                show_unauthorized()

    except Exception as e:
        logging.error(f"streamlit : K8S Control Panel : main : Exception : {str(e)}")
        logging.error(f"streamlit : K8S Control Panel : main : traceback : {traceback.format_exc()}")
        st.exception(e)
    
if __name__ == '__main__':
    main()