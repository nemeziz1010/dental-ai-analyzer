FROM python:3.11-slim

WORKDIR /app


RUN apt-get update && apt-get install -y libgl1-mesa-glx libglib2.0-0

COPY ./requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY ./api /app/api
COPY ./core /app/core
COPY ./models /app/models
COPY ./services /app/services
COPY ./main.py /app/

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
