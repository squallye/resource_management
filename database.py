from deta import Deta
import streamlit as st

# Connect to Deta Base with your Data Key
deta = Deta(st.secrets["data_key"])

db = deta.Base("resource_management")
pm_db = deta.Base("Project_manage")

def add_userdata(username,password):
    return db.put({"key":username,
                   "password":password,
                   "work content":[]
               
                })

def add_projectdata(projectname,description,project_type):
    return pm_db.put({"key":projectname,
                      "description":description,
                      "type":[project_type]
                      })

def get_project_name():
    data = pm_db.fetch()
    return [item['key'] for item in data.items]

def get_project_info():
    data = pm_db.fetch()
    return data.items



#add_userdata("admin","123456")

def view_all_users():
    data = db.fetch()
    return [user['key'] for user in data.items]

def login_user(username,password):
    data = db.fetch({"key":username,"password":password})
    return data.items

def update_user(username, updates):
    return db.update(updates,username)

#update_user("david",updates={"work content":[{"Finish":"","Project":"","Start":"","Task":"","Completed":False}]})


def unique_user(username):
    if username !="":
        return db.get(username)
    else:
        st.stop()

def get_user_info(username):
    data = db.fetch({"key":username})
    return data.items

