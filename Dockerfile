FROM python:3.12
RUN pip install poetry
COPY . /app
WORKDIR /app
RUN poetry install
EXPOSE 8501
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health
ENTRYPOINT ["poetry","run", "streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
