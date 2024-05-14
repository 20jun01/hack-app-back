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