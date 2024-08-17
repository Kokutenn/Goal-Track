import streamlit as st

# Initialize session state for goals
if 'goals' not in st.session_state:
    st.session_state.goals = []

# Function to add a new goal
def add_goal():
    goal_name = st.text_input("Goal Name")
    goal_unit = st.text_input("Unit (e.g., points, hours, etc.)")
    goal_total = st.number_input("Total Amount", min_value=1, value=100)

    if st.button("Add Goal"):
        st.session_state.goals.append({
            'name': goal_name,
            'unit': goal_unit,
            'total': goal_total,
            'progress': 0
        })
        st.experimental_rerun()

# Function to remove a goal
def remove_goal(goal_name):
    st.session_state.goals = [goal for goal in st.session_state.goals if goal['name'] != goal_name]
    st.experimental_rerun()

# Function to update progress
def update_progress(goal_name, amount):
    for goal in st.session_state.goals:
        if goal['name'] == goal_name:
            goal['progress'] += amount
            if goal['progress'] < 0:
                goal['progress'] = 0
            elif goal['progress'] > goal['total']:
                goal['progress'] = goal['total']
            break

# UI for managing goals
st.title("Goal Tracker")

if st.button("Add New Goal"):
    add_goal()

st.write("## Your Goals")
for goal in st.session_state.goals:
    st.write(f"### {goal['name']} ({goal['unit']})")
    progress_bar = st.progress(goal['progress'] / goal['total'])
    st.write(f"{goal['progress']} / {goal['total']} {goal['unit']}")

    col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

    with col1:
        if st.button("+1", key=f"add_1_{goal['name']}"):
            update_progress(goal['name'], 1)
            st.experimental_rerun()

    with col2:
        if st.button("-1", key=f"sub_1_{goal['name']}"):
            update_progress(goal['name'], -1)
            st.experimental_rerun()

    with col3:
        amount = st.number_input("Amount", value=0, step=1, key=f"amount_{goal['name']}")
        if st.button("Add/Subtract", key=f"custom_add_{goal['name']}"):
            update_progress(goal['name'], amount)
            st.experimental_rerun()

    with col4:
        if st.button("Remove Goal", key=f"remove_{goal['name']}"):
            remove_goal(goal['name'])

st.write("### Add a New Goal")
add_goal()

