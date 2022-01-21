PIP_BIN := .venv/bin/pip
PYTHON_BIN := .venv/bin/python

.PHONY:	test build check clean
.DEFAULT: test

$(PIP_BIN):
	python3 -m venv .venv

build: ${PIP_BIN}
	${PYTHON_BIN} setup.py sdist

clean:
	rm -rf .venv dist
