# Variables
PYTHON = python3
VENV = venv
BIN = $(VENV)/bin
PIP = $(BIN)/pip
PY = $(BIN)/python
FLAKE8 = $(BIN)/flake8
MYPY = $(BIN)/mypy
REQUIREMENTS = requirements.txt
MAIN = a-maze-ing.py
CONFIG = config.txt
OUTPUT = output.txt
DIST_DIR = dist
BUILD_DIR = build
EGG_INFO = *.egg-info
PYCACHE = __pycache__
MYPY_CACHE = .mypy_cache

# Targets
.PHONY: all install run lint clean fclean re venv

all: install run

$(VENV):
	$(PYTHON) -m venv $(VENV)

install: $(VENV)
	$(PIP) install -r $(REQUIREMENTS)

run: install
	$(PY) $(MAIN) $(CONFIG)

lint: install
	@echo "Running flake8..."
	$(FLAKE8) . --count --show-source --statistics --max-line-length=79 --exclude=venv,env,.venv,.env,__pycache__
	@echo "Running mypy..."
	$(MYPY) . --ignore-missing-imports --exclude venv

clean:
	rm -rf $(PYCACHE)
	rm -rf $(MYPY_CACHE)
	rm -rf $(DIST_DIR)
	rm -rf $(BUILD_DIR)
	rm -rf $(EGG_INFO)
	rm -rf */$(PYCACHE)
	rm -f $(OUTPUT)

fclean: clean
	rm -rf $(VENV)
	find . -maxdepth 1 -type f -name "*.txt" ! -name "$(REQUIREMENTS)" -delete

re: fclean all
