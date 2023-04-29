import streamlit as st
import operation as op
import database as db
import pandas as pd

sh = st.subheader("Please login at side bar")

with st.sidebar:
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type='password')
        submitted = st.form_submit_button("Login") 
        
        if submitted:
            user_exist = db.login_user(username,password)
            
            if not user_exist:
                st.warning("User doesn't exist!")
            else:
                st.session_state.username = username
        
# Code block outside the st.form()
if 'username' in st.session_state:
    sh.subheader("Welcome Back {}{}".format(st.session_state.username,"!"))
    

    if username != 'admin':
        work_content = db.get_user_info(st.session_state.username)[0]['work content']            
        if work_content ==[]:
            op.add_task()
            #op.display_ganntt_chart(work_content)

        else:
            op.display_ganntt_chart(work_content)
            option = st.selectbox(
                'Choose your options below:',
                ('-- Select an option --','Add Task', 'Delete Task', 'Update Task'),label_visibility="hidden")

            if option == "Add Task":
                op.add_task()
            elif option == "Delete Task":
                op.delete_task()
            elif option == "Update Task":
                op.update_task()

    else:
        st.write("This is admin page!")

        option = st.selectbox(
        'Admin Options',
        ('-- Select an option --','Check individual Workload', 'Check Team Workload','Manage Project'),label_visibility="hidden")

        if option == "Check individual Workload":
    
            username_list = db.view_all_users()

            if len(username_list) > 0:
                # Exclude "admin" from the username list
                username_list = [username for username in username_list if username != "admin"]
                username = st.selectbox("Pick a user name:", options=username_list)                
                work_content = db.get_user_info(username)[0]['work content']
                #columns = ['Project','Task', 'Start', 'Finish']
                op.display_ganntt_chart(work_content)                
                    
            else:
                st.warning("No users found in the database.")

                
        elif option == "Check Team Workload":
            st.write("Check team workload here")
            username_list = db.view_all_users()
            # Create an empty DataFrame to hold the team workload
            team_workload = pd.DataFrame(columns=['Project', 'Start', 'Finish', 'Resource'])

            # Display checkboxes for each user
            selected_users = []
            for username in username_list:
                if username == "admin":
                    continue
                selected = st.checkbox(username)
                if selected:
                    selected_users.append(username)

            # If at least one checkbox is selected, show the team workload
            if st.button("Show Team workload"):
                for user in selected_users:
                    work_content = db.get_user_info(user)[0]['work content']
                    for task in work_content:
                        task['Resource'] = user
                    team_workload = team_workload.append(work_content)

                if not team_workload.empty:
                    op.display_team_ganntt_chart(team_workload)
                else:
                    st.warning("No tasks found for the selected users.")

        elif option == 'Manage Project':
            st.write("This is page to manage projects")
            with st.form("Add Project"):
                project_name = st.text_input("Project Name",placeholder="pleaes enter project name here")
                description = st.text_area("Project description",placeholder="please enter project description here(optional)")
                project_type = st.selectbox("Project type",options=["---Select a Porject Type---","NPD","CI","TD","Other"])
                submitted = st.form_submit_button()

                if submitted:
                    if project_name!="" and project_type!="---Select a Porject Type---":
                        db.add_projectdata(project_name,description,project_type)
                        st.success("Project has been created!")
                    else:
                        st.warning("Please enter project name!")

            df = pd.DataFrame(db.get_project_info())
            #rename the column
            df = df.rename(columns={'key': 'Project Name','description':'Description','type':'Type'})
            new_order = ['Project Name', 'Description','Type' ]
            df = df.reindex(columns=new_order)
            st.dataframe(df)

    
                 


