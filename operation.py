import streamlit as st
import pandas as pd
import datetime as dt
from datetime import datetime
import plotly.express as px
import database as db


if "username" not in st.session_state:
    st.session_state.username = ""



PROJECT_LIST = db.get_project_name()



def add_task():
    
    st.write("Please enter the task details below:")
    with st.form("Add Task"):
    
        username = st.session_state.username
        project_name = st.selectbox("Project Name",PROJECT_LIST)
        task_name = st.text_input("Task name:",placeholder="Please enter your task name here...")
        start_date = st.date_input("Start date", dt.date.today())
        end_date = st.date_input("End date", dt.date.today()+dt.timedelta(days=7))
        task_complete = False

        submitted = st.form_submit_button("Add Task")

        if start_date > end_date:
            st.warning("Please enter a valid date range!")
            return

        if task_name == "":
            st.warning("Please enter a task name!")
            return

        # Convert the date objects to strings
        start_date_str = start_date.strftime("%Y-%m-%d")
        end_date_str = end_date.strftime("%Y-%m-%d")
            
        item = dict(Project= project_name,Task=task_name, Start=start_date_str, Finish=end_date_str, Completed=task_complete)

        

        if submitted:
            #st.session_state.Tasks.append(item)

            update_database(username, item)

            st.success("Task was added successfully!")

def update_database(username, item):
    existing_work_content = db.get_user_info(username)[0]['work content']
    existing_work_content.append(item)
    db.update_user(username,updates={"work content":existing_work_content})


@st.cache_data(experimental_allow_widgets=True)
def display_ganntt_chart(content):
        # Convert the task list to a DataFrame
        df = pd.DataFrame(content)

        # Specify the order of the columns
        columns = ['Project','Task', 'Start', 'Finish','Completed']

        # Create the chart
        df['Task Completion'] = df['Completed'].map({True: 'Yes', False: 'No'})
        color_map = {"Yes": 'rgb(144, 238, 144)', "No": 'rgb(135, 206, 235)'}
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task",color="Task Completion",color_discrete_map=color_map)
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(side='top')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        # Customize the chart layout
        fig.update_layout(
            title="My Gantt Chart",
            margin=dict(t=100),
            xaxis_title="Date",
            yaxis_title="Task"
        )

       

        # Display the chart using Streamlit
        st.plotly_chart(fig)

        # Display the list of tasks as a table
        st.write("Task List:")
        st.dataframe(df[columns])

        st.button("Update Gannt Chart")
        st.cache_data.clear()

def display_team_ganntt_chart(content):
        # Convert the task list to a DataFrame
        df = pd.DataFrame(content)

        # Create the chart
        fig = px.timeline(df, x_start="Start", x_end="Finish", y="Project",color="Resource")
        fig.update_yaxes(autorange="reversed")
        fig.update_xaxes(side='top')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

        # Customize the chart layout
        fig.update_layout(
            title="Team Gantt Chart",
            xaxis_title="Date",
            yaxis_title="Project"
        )       

        # Display the chart using Streamlit
        st.plotly_chart(fig)

def get_task_list():
    task_list = db.get_user_info(st.session_state.username)[0]['work content']
    options = []
    for task in task_list:
        finish = task.get('Finish')
        project = task.get('Project')
        start = task.get('Start')
        taskname = task.get('Task')
        completed = task.get('Completed')
        if finish and project and start and taskname:
            options.append((project,taskname))
    return task_list, options
        
def delete_task():
    task_list, options = get_task_list()
            
    selected_task = st.selectbox("Select a task to delete:",options)
    
    if st.button("Delete Task"):
        
        for task in task_list:
            if task['Project'] == selected_task[0] and task['Task'] == selected_task[1]:
                task_list.remove(task)
                db.update_user(st.session_state.username,updates={"work content":task_list})
                st.success("Selected Task has been deleted!")
                break
        # If the loop finishes without finding a matching task, show an error message
        else:
            st.error("Selected task not found!")

def update_dates(selected_task, task_list):
    current_start_date = datetime.now().date() # default value for start date
    current_end_date = datetime.now().date() # default value for end date
    current_completion = True  # default value for completion checkbox
    for task in task_list:
        if task['Project'] == selected_task[0] and task['Task'] == selected_task[1]:
            current_start_date = datetime.strptime(task['Start'], '%Y-%m-%d').date()
            current_end_date = datetime.strptime(task['Finish'], '%Y-%m-%d').date()
            current_completion = task['Completed']
            break
    return current_start_date, current_end_date,current_completion

def update_task():
    task_list, options = get_task_list()
    selected_task = st.selectbox("Select a task to update:", options, key="task_select")
    current_start_date, current_end_date,current_completion = update_dates(selected_task, task_list)
    #current_completion = True  # default value for completion checkbox

    #st.selectbox("This one should be hidden:", options, key="task_select2", on_change=lambda x: update_dates(selected_task, task_list))

    new_start_date = st.date_input("New Start date", current_start_date)
    new_end_date = st.date_input("New Due date", current_end_date)
    new_completion = st.checkbox("Task Completed", value=current_completion)

    if st.button("Update Task"):
        for task in task_list:
            if task['Project'] == selected_task[0] and task['Task'] == selected_task[1]:
                task['Start'] = new_start_date.strftime('%Y-%m-%d')
                task['Finish'] = new_end_date.strftime('%Y-%m-%d')
                task['Completed'] = new_completion
                db.update_user(st.session_state.username, updates={"work content": task_list})
                st.success("Selected Task has been updated!")
                break
        else:
            st.error("Selected task not found!")



     

               
                
               
     
               
    



