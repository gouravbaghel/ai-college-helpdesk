import streamlit as st
import pandas as pd
from utils.api import get
from components.header import render_header

def render_timetable():
    render_header("Academic Timetable", "View daily course schedules by department and semester")
    
    col1, col2 = st.columns(2)
    with col1:
        dept = st.text_input("Department", value="Computer Science")
    with col2:
        sem = st.number_input("Semester", min_value=1, max_value=10, value=5)
        
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    tabs = st.tabs(days)
    
    for i, day in enumerate(days):
        with tabs[i]:
            timetable = get(f"/student/timetable?department={dept}&semester={sem}&day={day}")
            if timetable and len(timetable) > 0:
                rows = []
                for entry in timetable:
                    rows.append({
                        "Time Slot": f"{entry.get('start_time', '')} - {entry.get('end_time', '')}",
                        "Course Subject": entry.get("subject", ""),
                        "Faculty": entry.get("faculty_name", ""),
                        "Room": entry.get("room_number", "")
                    })
                df = pd.DataFrame(rows)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info(f"No classes scheduled for {day} in {dept} (Semester {sem}).")
