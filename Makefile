.PHONY: virtualenv setup

virtualenv:
	[ ! -d env ] && python3 -m venv env || true

setup:  virtualenv requirements.txt
	env/bin/pip install -r requirements.txt
	env/bin/pip install -e .
