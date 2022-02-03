PIP_BIN := .venv/bin/pip
PYTHON_BIN := .venv/bin/python
TWINE_BIN := .venv/bin/twine

.PHONY: build
build: $(PIP_BIN)
	$(PYTHON_BIN) setup.py sdist
	$(TWINE_BIN) check dist/*

.PHONY: clean
clean:
	git clean -dxf dist build

$(PIP_BIN):
	python3.7 -m .venv

.PHONY: pip
pip: $(PIP_BIN)
	$(PIP_BIN) install --upgrade pip wheel twine
