FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main/ main/
COPY codex.md readme.txt ./

EXPOSE 8000

CMD ["uvicorn", "main.app:app", "--host", "0.0.0.0", "--port", "8000"]
