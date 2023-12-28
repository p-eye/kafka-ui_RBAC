import streamlit as st

def navbar(login_str):
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    st.markdown(f"""
    <nav class="navbar navbar-expand navbar-light fixed-top bg-light">
        <div class="pt-5 container">
            <div class="navbar-collapse collapse order-3" id="navbarCollapse">
                <ul class="navbar-nav mr-auto">
                    <li class="nav-item active">
                        <span class="nav-link py-0 px-5 mx-5 mb-0 h4">Kafka UI RBAC</span>
                    </li>
                </ul>
                <ul class="navbar-nav ml-auto">
                    <li class="nav-item active">
                        <a class="nav-link py-0" href="#">{login_str}</a>
                    </li>
                <!--
                    <li class="nav-item">
                        <a class="nav-link py-0" href="#">Product</a>
                    </li>
                -->
                </ul>
            </div>
        </div>
    </nav>
    """, unsafe_allow_html=True)