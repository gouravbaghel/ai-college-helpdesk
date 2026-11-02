import streamlit as st
from utils.api import get, post, delete
from components.header import render_header
import pandas as pd

def render_admin_timetable():
    render_header("Timetable Management", "Manage class schedules")
    
    # Add entry
    st.subheader("Add Timetable Entry")
    with st.form("create_tt_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            department = st.text_input("Department", value="Computer Science")
            semester = st.number_input("Semester", min_value=1, max_value=10, value=5)
        with col2:
            day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
            subject = st.text_input("Subject")
        with col3:
            start_time = st.text_input("Start Time (HH:MM)", value="09:00")
            end_time = st.text_input("End Time (HH:MM)", value="10:00")
        
        col4, col5 = st.columns(2)
        with col4:
            faculty = st.text_input("Faculty Name")
        with col5:
            room = st.text_input("Room Number")
        
        submit = st.form_submit_button("Add Entry", use_container_width=True)
        if submit and subject and faculty:
            result = post("/admin/timetable", data={
                "department": department,
                "semester": semester,
                "day_of_week": day,
                "subject": subject,
                "start_time": start_time,
                "end_time": end_time,
                "faculty_name": faculty,
                "room_number": room
            })
            if result:
                st.success("Timetable entry added!")
                st.rerun()
    
    st.markdown("---")
    
    # List timetable
    st.subheader("Current Timetable")
    timetable = get("/admin/timetable")
    
    if timetable:
        df = pd.DataFrame(timetable)
        if not df.empty:
            # Filter
            col1, col2 = st.columns(2)
            with col1:
                dept_filter = st.selectbox("Filter by Department", ["All"] + sorted(df["department"].unique().tolist()))
            with col2:
                day_filter = st.selectbox("Filter by Day", ["All"] + sorted(df["day_of_week"].unique().tolist()))
            
            filtered = df.copy()
            if dept_filter != "All":
                filtered = filtered[filtered["department"] == dept_filter]
            if day_filter != "All":
                filtered = filtered[filtered["day_of_week"] == day_filter]
            
            display_cols = ["day_of_week", "start_time", "end_time", "subject", "faculty_name", "room_number", "semester"]
            available_cols = [c for c in display_cols if c in filtered.columns]
            st.dataframe(filtered[available_cols], use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.subheader("Delete Entry")
            entry_id = st.number_input("Enter Entry ID to delete", min_value=1, step=1)
            if st.button("Delete Entry"):
                result = delete(f"/admin/timetable/{entry_id}")
                if result:
                    st.success("Entry deleted.")
                    st.rerun()
    else:
        st.info("No timetable entries found.")
