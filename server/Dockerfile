FROM python:latest

WORKDIR .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN pip install psycopg2-binary

COPY . .

CMD python server.py
