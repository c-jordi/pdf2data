.PHONY: help prepare-dev test lint run doc

VENV_NAME?=venv
VENV_ACTIVATE=. $(VENV_NAME)/bin/activate
PYTHON=${VENV_NAME}/bin/python3

.DEFAULT: help
help:
	@echo "make prepare-dev"
	@echo "prepare development environment, use only once"
	@echo "make test"
	@echo "run tests"
	@echo "make lint"
	@echo "run pylint and mypy"
	@echo "make run"
	@echo "run project"
	@echo "make doc"
	@echo "build sphinx documentation"

venv:
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -r server/requirements.txt
	touch $(VENV_NAME)/bin/activate

test: venv
	${PYTHON} -m pytest

lint: venv
	${PYTHON} -m pylint
	${PYTHON} -m mypy

run-server: venv
	${PYTHON} server/run.py

run-all:
	sudo docker-compose up

add-worker: venv
	celery -A server.application.tasks worker
	 
doc: venv
	$(VENV_ACTIVATE) && cd docs; make html