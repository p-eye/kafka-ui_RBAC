import mysql.connector as connector
from datetime import datetime
import streamlit as st

class DB:
    def __init__(self):
        self.SECRET_KEY = "mysql"
        self.conn = self.init()

    def init(self):
        config = st.secrets[self.SECRET_KEY]
        conn = connector.connect(host=config.host,
                                 port=config.port,
                                 database=config.database,
                                 user=config.user,
                                 password=config.password)
        conn.autocommit = True
        return conn

    @st.cache_resource(ttl=864000)
    def get_users(_self):
        sql = "SELECT email, type, created_at from streamlit;"
        cursor = _self.conn.cursor(buffered=True, dictionary=True)
        cursor.execute(sql)
        users = cursor.fetchall()
        cursor.close()
        return users
    
    def add_user(self, email, type):
        created_at = datetime.now()
        sql = f"""INSERT INTO `streamlit` VALUES ('{email}', '{type}', '{created_at}');"""
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        cursor.close()
        st.cache_resource.clear()

    def delete_user(self, email):
        sql = f"""DELETE FROM `streamlit` WHERE email = '{email}';"""
        cursor = self.conn.cursor(buffered=True)
        cursor.execute(sql)
        cursor.close()
        st.cache_resource.clear()    