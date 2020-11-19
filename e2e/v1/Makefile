all: run

env:
	python3 -m venv env
	. env/bin/activate && \
	pip3 install -r requirements.txt

upgrade:
	. env/bin/activate && \
	pip3 install -Ur requirements-base.txt && \
	pip3 freeze > requirements.txt

test:
	pytest

run: test

clean:
	find . -type f -name '*~' -exec rm -f {} \;
	find . -type d -name '__pycache__' -prune -exec rm -rf {} \;

.PHONY: all env upgrade test run clean
