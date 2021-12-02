clean-db:
	rm -f db.sqlite & rm -f ./application/storage/* & python3 ./application/models.py

worker:
	celery -A application.tasks worker -l INFO

run: 
	python3 run.py

env:
	source ./venv/bin/activate

pdf:
	python3 extractpdf.py