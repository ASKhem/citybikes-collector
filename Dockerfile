FROM python:3.13.1-slim

WORKDIR /app

COPY requirements.txt src/fetch_data.py ./

RUN mkdir -p data && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ENV MONGODB_URL=""

CMD ["python", "fetch_data.py"]