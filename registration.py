import streamlit as st
import database as db

with st.form("Registration Form"):
    new_user = st.text_input("username")
    new_password = st.text_input("passowrd", type = 'password')
    submitted = st.form_submit_button("Registration")


    if submitted:
        user_exist = db.unique_user(new_user)
        if user_exist:
            st.warning("User name alredy exists, please pick a different one")
            
        else:
            
            db.add_userdata(new_user,new_password)
            st.success("New accout setup successfuly")

st.markdown(
    """
    Back to [Home](https://resource-management.streamlit.app/)

"""
)