import streamlit as st
from datetime import time, datetime, timedelta
from sqlalchemy import create_engine, text
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch


# Create connection string for supabase
db_url = f"postgresql://{st.secrets['DB_USER']}:{st.secrets['DB_PASS']}@{st.secrets['DB_HOST']}:{st.secrets['DB_PORT']}/{st.secrets['DB_NAME']}"

# Create sqlalchemy engine
engine = create_engine(db_url)

# Set web app title
st.title("ACL Recovery Tracker")

## Select user from all existent users
# Display existent users on the db
users_query = text(
    """
    SELECT user_id, name
    FROM users
    """
)

with engine.connect() as conn:
    df = pd.read_sql(users_query, con=conn)
    
# Dropdown to select user
selected_user = st.selectbox("Select a user", df['name'], index=0)

# Get selected user id
selected_user_id = int(df[df['name'] == selected_user]['user_id'].values[0])

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
    flexion = None
    swelling = st.select_slider("Swelling level", ["None", "Mild", "Moderate", "Severe"])
    painkillers = st.checkbox("Painkillers")
    rehab_done = st.checkbox("Rehab done")
    mood = st.select_slider("Mood", ["Low", "Neutral", "Happy"], value="Happy")
    notes = st.text_area("Notes:")
    submit = st.form_submit_button("Submit")

if submit:
    with st.spinner("Saving to database..."):

        # Define the sql query
        insert_query = text(
            """
            INSERT INTO daily_logs (
                date, sleep_hours, steps_walked, user_id
            )
            VALUES (
                :date, :sleep_hours, :steps_walked, :user_id
            )
            ON CONFLICT (date, user_id) DO UPDATE SET
                sleep_hours = COALESCE(EXCLUDED.sleep_hours, daily_logs.sleep_hours),
                steps_walked = COALESCE(EXCLUDED.steps_walked, daily_logs.steps_walked);

            INSERT INTO periodic_logs (
                date, time, pain, flexion, swelling, painkillers,
                rehab_done, mood, notes, user_id
            )
            VALUES (
                :date, :time, :pain, :flexion, :swelling, :painkillers,
                :rehab_done, :mood, :notes, :user_id
            );
            """
        )
        
        params = {
            "date": log_date,
            "time": log_time,
            "sleep_hours": sleep_hours,
            "steps_walked": steps_walked,
            "pain": pain,
            "flexion": flexion,
            "swelling": swelling,
            "painkillers": painkillers,
            "rehab_done": rehab_done,
            "mood": mood,
            "notes": notes,
            "sleep_hours": sleep_hours,
            "steps_walked": steps_walked,
            "user_id": selected_user_id
        }

        with engine.begin() as conn:
            conn.execute(insert_query, params)  

        st.write("Saved to database.")

# Display table periodic_logs
select_query = text(
    f"""
    SELECT date, time, pain, flexion, swelling, painkillers, rehab_done, mood, notes
    FROM periodic_logs
    WHERE user_id = {selected_user_id}
    ORDER BY date, time
    """
)

with engine.connect() as conn:
    df_periodic = pd.read_sql(select_query, con=conn)
    st.dataframe(df_periodic)

# Display table daily_logs
select_query2 = text(
    f"""
    SELECT date, sleep_hours, steps_walked
    FROM daily_logs
    WHERE user_id = {selected_user_id}
    ORDER BY date
    """
)

with engine.connect() as conn:
    df_daily = pd.read_sql(select_query2, con=conn)
    st.dataframe(df_daily)

# Create and show pain vs days plot

#df_periodic_grouped = df_periodic[['date', 'pain']].groupby(['date']).mean()
df_periodic_grouped = df_periodic.groupby('date').agg(
    {
        'pain': 'mean',
        'painkillers': 'any'
    }
)

fig, ax = plt.subplots()

indices = range(len(df_periodic_grouped))
pain_values = df_periodic_grouped['pain']

colors = ['darkblue' if pk else 'blue' for pk in df_periodic_grouped["painkillers"]]

ax.bar(indices, pain_values, color=colors)
ax.bar(indices[1], pain_values.iloc[1], color='red')

legend_handles = [
    Patch(color='red', label='Operation day'),
    Patch(color='darkblue', label='Painkillers')
]

ax.set_title('Pain evolution over days')
ax.set_ylabel('Pain (0-10)')
ax.set_xlabel('Days')
ax.legend(handles=legend_handles)

st.pyplot(fig)
