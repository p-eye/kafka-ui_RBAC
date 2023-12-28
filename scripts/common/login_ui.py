import streamlit as st
import time
from tools.oauth_tool import OAuth
from tools.cookie_tool import Cookie
from scripts.common.navbar_ui import navbar

# set wide page
st.set_page_config(layout= "wide", menu_items= {}, page_icon= "media/K8s Control Panel.png")

_COOKIE_KEY = 'C_OAUTH'
SHOW_LOGOUT_BUTTON = False
LOGIN_STR = ""

oauth = OAuth()
cookie = Cookie()
config = oauth.read_config()

def logout():
    if _COOKIE_KEY in st.session_state:
        del st.session_state[_COOKIE_KEY]
    SHOW_LOGOUT_BUTTON = False
    cookies = cookie.get_all_cookies()
    cookie.del_cookie(cookies, _COOKIE_KEY)

def login_ui():    
    global LOGIN_STR

    cookies = cookie.get_all_cookies() 
    if _COOKIE_KEY in cookies:
        token = cookies[_COOKIE_KEY]
        SHOW_LOGOUT_BUTTON = True
        valid, msg = oauth.validate_token(token, config)
        if valid is False:
            st.error(msg)
            LOGIN_STR = msg
            cookie.del_cookie(cookies, _COOKIE_KEY)
        else:
            st.session_state[_COOKIE_KEY] = token
            LOGIN_STR = msg

    else:
        SHOW_LOGOUT_BUTTON = False
        request_url = oauth.create_auth_request_url(config)
        LOGIN_STR = f'<a href="{request_url}" target="_self">LOGIN GOOGLE</a>'

    navbar(LOGIN_STR)
    time.sleep(0.5)

    # url에서 token을 요청하기 위한 code와 state 가져오기
    if 'code' in st.experimental_get_query_params():
        # 신규 토큰 요청 및 유효성 검사
        token = oauth.request_token(config, "google")
        valid, msg = oauth.validate_token(token, config)
        if valid:
            cookie.set_cookie(_COOKIE_KEY, token)
            st.session_state[_COOKIE_KEY] = token
            SHOW_LOGOUT_BUTTON = True

        else:
            st.error(msg)
            LOGIN_STR = msg
            SHOW_LOGOUT_BUTTON = True

    if SHOW_LOGOUT_BUTTON:
        return st.sidebar.button("Log out", on_click=logout)
    return True

def get_login_user():
    return LOGIN_STR





    # # if 'code' not in st.experimental_get_query_params():
    # #     show_auth_link(config, label)

    # # url에서 token을 요청하기 위한 code와 state 가져오기
    # if 'code' in st.experimental_get_query_params():
    # #     code = st.experimental_get_query_params()['code'][0]
    # #     state = st.experimental_get_query_params()['state'][0]

    # # # url에서 쿼리 파라미터 지우기
    # #     oauth.remove_query_params(state)

    # # 신규 토큰 요청 및 유효성 검사
    #     token = oauth.request_token(config, "google")
    #     valid, msg = oauth.validate_token(token, config)
    #     if valid:
    #         cookie.set_cookie("token", token)
    #         st.session_state["token"] = token
    #         SHOW_LOGOUT_BUTTON = True
    #         # hide_pages([])
    #     else:
    #         cookie.del_cookie(cookies, "token")
    #         st.error(msg)
    #         login_str = "None"

    # if SHOW_LOGOUT_BUTTON:
    #     return st.sidebar.button("Log out", on_click=logout)
    # return True
    # # else:
    # #     st.sidebar.link_button("Login", request_url)

