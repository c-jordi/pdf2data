FROM python:3.9-slim

WORKDIR /worker

COPY . .
RUN pip install -r requirements.txt
CMD ["celery", "-A", "application.tasks" , "worker"]