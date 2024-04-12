.PHONY: install run clean

VENV = pipenv run

install:
	pipenv install

run:
	$(VENV) python main.py

clean:
	pipenv --rm
	rm -rf __pycache__