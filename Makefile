VENV_DIR := .venv
PIP_BIN := $(VENV_DIR)/bin/pip
PYTHON_BIN := $(VENV_DIR)/bin/python
TWINE_BIN := $(VENV_DIR)/bin/twine

# https://endoflife.date/python 2025/10
SYSTEM_PYTHON ?= python3.9

.PHONY: build
build: $(TWINE_BIN)
	$(PYTHON_BIN) -m build
	$(TWINE_BIN) check dist/*

.PHONY: clean
clean:
	git clean -dxf dist build

$(PIP_BIN):
	$(SYSTEM_PYTHON) -m venv $(VENV_DIR)

${TWINE_BIN}: $(PIP_BIN)
	$(PIP_BIN) install wheel twine build

.PHONY: pip
pip: $(PIP_BIN)
	$(PIP_BIN) install --upgrade pip wheel twine

.PHONY: changelog
changelog:
	git log --first-parent --pretty='%s'

###############################################################################
### Format Tasks
###############################################################################

RUFF_BIN := $(VENV_DIR)/bin/ruff

$(RUFF_BIN): $(PIP_BIN)
	$(PIP_BIN) install ruff

.PHONY: format
format: $(RUFF_BIN) $(BLACK_BIN)
	$(RUFF_BIN) check $(PKG_NAME) --fix
	$(RUFF_BIN) format $(PKG_NAME)
