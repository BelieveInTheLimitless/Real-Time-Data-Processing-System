FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt . 

COPY test-requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt -r test-requirements.txt

COPY . .

COPY start.sh .

RUN chmod +x start.sh

CMD ["./start.sh"]