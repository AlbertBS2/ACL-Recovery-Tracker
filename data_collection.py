import streamlit as st
from datetime import date


st.title("ACL Recovery Tracker")

# Form
with st.form("daily_log"):
    log_date = st.date_input("Date", date.today())
    pain = st.slider("Pain Level (0-10)", 0, 10)
    flexion = st.number_input("Extension (degrees)", -10, 0)
    mood = st.selectbox("Mood", ["Happy", "Neutral", "Low"])
    rehab_done = st.checkbox("Rehab completed")
    notes = st.text_area("Notes:")
    submit = st.form_submit_button("Submit")

