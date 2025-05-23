FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# least-privilege container user
RUN useradd -m collector
USER collector

ENTRYPOINT ["python", "main.py"]
