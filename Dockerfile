FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY backend/app backend/app
COPY frontend frontend
COPY requirements.txt backend/app

RUN pip install -r backend/app/requirements.txt
