import streamlit as st
from datetime import date
from sqlalchemy import create_engine, text


# Load environment variables
#load_dotenv(".env_supabase")

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
        # Create connection string for supabase
        #db_url = f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASS']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}"
        db_url = f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASS']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"

        # Create sqlalchemy engine
        engine = create_engine(db_url)

        # Define the sql query
        query = text(
            f"""
            INSERT INTO logs
            VALUES
            (:log_date, :pain, :flexion, :mood, :rehab_done, :notes);
            """
        )
        
        params = {
            "log_date": log_date,
            "pain": pain,
            "flexion": flexion,
            "mood": mood,
            "rehab_done": rehab_done,
            "notes": notes
        }

        with engine.connect() as conn:
            conn.execute(query, params)
            conn.commit()

        st.write("Saved to database.")