.PHONY: install-dev lint format format-check test check build upload clean

VENV = .venv
VENV_READY = $(VENV)/.installed

# --system-site-packages: phpy no se instala con pip, debe existir a nivel
# de sistema (ver la opción PHPY_ENABLED de docker-python3.14-caddy-server)
# — los tests solo corren dentro de ese entorno.
#
# Un prerequisito basado en archivo (no solo un target phony): todos los
# demás targets dependen de $(VENV_READY), así que cada uno arranca el venv
# por su cuenta si falta, y Make se salta la reinstalación cuando nada
# relevante cambió.
$(VENV_READY): pyproject.toml
	python3 -m venv --system-site-packages $(VENV)
	$(VENV)/bin/pip install --upgrade pip
	$(VENV)/bin/pip install -e '.[dev]'
	touch $(VENV_READY)

install-dev: $(VENV_READY)

lint: $(VENV_READY)
	$(VENV)/bin/ruff check .

format: $(VENV_READY)
	$(VENV)/bin/ruff format .

format-check: $(VENV_READY)
	$(VENV)/bin/ruff format --check .

test: $(VENV_READY)
	$(VENV)/bin/pytest -v

check: lint format-check test

build: $(VENV_READY)
	$(VENV)/bin/python -m build

upload: build
	$(VENV)/bin/twine upload dist/*

clean:
	rm -rf dist build *.egg-info .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
