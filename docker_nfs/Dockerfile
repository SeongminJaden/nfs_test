FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# files 폴더는 호스트에서 마운트할 예정이라 복사하지 않음

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
