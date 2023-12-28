import streamlit as st
import extra_streamlit_components as stx
import time

class Cookie:
    def __init__(self):
        self.cookie_manager = self.init()

    def init(self):
        return stx.CookieManager()

    @st.cache_data(ttl=86400, experimental_allow_widgets=True)
    def get_manager(_self):
        return _self.cookie_manager
    
    def get_all_cookies(self):
        return self.cookie_manager.get_all()

    def set_cookie(self, key, value):
        self.cookie_manager.set(key, value)
        time.sleep(0.5)

    def del_cookie(self, cookies, key):
        if key in cookies:
            self.cookie_manager.delete(key)
            time.sleep(0.5)