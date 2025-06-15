import streamlit as st
from datetime import date, datetime, time
from sqlalchemy import create_engine, text

# Set web app title
st.title("ACL Recovery Tracker")

log_date = st.date_input("Date")
log_time = st.time_input("Time")

# Form
with st.form("daily_log"):

    if log_time < time(12, 0):
        sleep_hours = st.number_input("Sleep time (hours)", 0.00, 24.00, value=8.00)
    else:
        sleep_hours = None

    if log_time > time(21, 0):
        steps_walked = st.number_input("Steps walked", 0, 100000, value=5000)
    else:
        steps_walked = None

    pain = st.slider("Pain level (0-10)", 0, 10)
    #flexion = st.number_input("Extension (degrees)", -10, 0)
    swelling = st.select_slider("Swelling level", ["None", "Mild", "Moderate", "Severe"])
    painkillers = st.checkbox("Painkillers")
    rehab_done = st.checkbox("Rehab done")
    mood = st.select_slider("Mood", ["Low", "Neutral", "Happy"])
    notes = st.text_area("Notes:")
    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner("Saving to database..."):
        # Create connection string for supabase
        db_url = f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASS']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"

        # Create sqlalchemy engine
        engine = create_engine(db_url)

        # Define the sql query
        query = text(
            f"""
            INSERT INTO logs
            VALUES
            (:date, :time, :sleep_hours, :steps_walked, :pain, :flexion, :swelling, :painkillers, :rehab_done, :mood, :notes);
            """
        )
        
        params = {
            "date": log_date,
            "time": log_time,
            "sleep_hours": sleep_hours,
            "steps_walked": steps_walked,
            "pain": pain,
            #"flexion": flexion,
            "swelling": swelling,
            "painkillers": painkillers,
            "rehab_done": rehab_done,
            "mood": mood,
            "notes": notes
        }

        with engine.connect() as conn:
            conn.execute(query, params)
            conn.commit()

        st.write("Saved to database.")