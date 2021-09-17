FROM python:3.9-slim

WORKDIR /web

COPY . .
RUN pip install -r requirements.txt
CMD ["python", "run.py"]