.PHONY: install run clean convert_svgs

VENV = pipenv run

install:
	pipenv install

run:
	$(VENV) python main.py

clean:
	pipenv --rm
	rm -rf __pycache__

convert_svgs:
	pipenv run python scripts/convert_svgs.py ./assets --overwrite