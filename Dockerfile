FROM python:3.13

WORKDIR /app

COPY requirements.txt .
COPY data_collection_supabase.py .
COPY .streamlit/ ./.streamlit/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "data_collection_supabase.py", "--server.port=8501", "--server.address=0.0.0.0"]