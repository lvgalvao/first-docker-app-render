FROM python:3.12
RUN pip install poetry
COPY . /app
WORKDIR /app
RUN poetry install
ENTRYPOINT ["poetry", "run", "streamlit", "run", "main.py"]
