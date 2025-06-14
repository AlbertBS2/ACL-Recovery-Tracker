import streamlit as st
from datetime import date
import pymysql
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv(".env")

# Set web app title
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

if submit:
    with st.spinner("Saving to database..."):
        # Save to db
        with pymysql.connect(
            host=os.environ["DB_ADDRESS"],
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASS"],
            port=int(os.environ["DB_PORT"]),
            db=os.environ["DB_NAME"]
        ) as mydb:
            
            cursor = mydb.cursor()

            query = f"""
                    INSERT INTO logs
                    VALUES
                    (%s, %s, %s, %s, %s, %s);
                    """
            cursor.execute(query, (log_date, pain, flexion, mood, rehab_done, notes))
            mydb.commit()
            st.write("Saved to database.")