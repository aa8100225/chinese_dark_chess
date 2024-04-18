.PHONY: install run clean convert_svgs test

VENV = pipenv run

install:
	pipenv install

run:
	$(VENV) python main.py $(if $(AI),--ai)

clean:
	pipenv --rm
	rm -rf __pycache__

convert_svgs:
	pipenv run python scripts/convert_svgs.py ./assets/images --overwrite

test:
	pipenv run python -m unittest discover