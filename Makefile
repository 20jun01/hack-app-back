.PHONY: init
init:
	python3 -m venv venv

.PHONY: activate
activate:
	. venv/bin/activate.fish

.PHONY: install
install:
	pip install -r requirements.txt	

.PHONY: run
run:
	python3 main.py	

.PHONY: deactivate
deactivate:
	deactivate

.PHONY: export
export:
	pip freeze > requirements.txt

.PHONY: fmt
fmt:
	black ./main.py
	black ./app

.PHONY: lint
lint:
	flake8 main.py
	flake8 ./app
