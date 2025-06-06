PYTHON_INTERPRETER=python3
VENV_PATH=.venv

SANDBOX_DIR=sandbox
STATICFILES_DIR=$(SANDBOX_DIR)/static-sources

PYTHON_BIN=$(VENV_PATH)/bin/python
PIP=$(VENV_PATH)/bin/pip
BOUSSOLE=$(VENV_PATH)/bin/boussole
TOX=$(VENV_PATH)/bin/tox
TWINE=$(VENV_PATH)/bin/twine
DJANGO_MANAGE=$(PYTHON_BIN) $(SANDBOX_DIR)/manage.py
FLAKE=$(VENV_PATH)/bin/flake8
PYTEST=$(VENV_PATH)/bin/pytest
SPHINX_RELOAD=$(PYTHON_BIN) sphinx_reload.py

DEMO_DJANGO_SECRET_KEY=samplesecretfordev
PACKAGE_NAME=django-smart-media
PACKAGE_SLUG=`echo $(PACKAGE_NAME) | tr '-' '_'`
APPLICATION_NAME=smart_media

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo "  freeze-dependencies -- to write a frozen.txt file with installed dependencies versions"
	@echo
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-var           -- to clean data (uploaded medias, database, etc..)"
	@echo "  clean-doc           -- to remove documentation builds"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  run                 -- to run Django development server"
	@echo "  migrations                    -- to create new migrations for application after changes"
	@echo "  migrate             -- to apply demo database migrations"
	@echo "  superuser           -- to create a superuser for Django admin"
	@echo ""
	@echo "  css                 -- to build stylesheets with Boussole from Sass sources"
	@echo "  watch-sass          -- to launch Boussole watch mode to rebuild stylesheets from Sass sources"
	@echo
	@echo "  docs                -- to build documentation"
	@echo "  livedocs            -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  check-django        -- to run Django System check framework"
	@echo "  check-migrations    -- to check for pending application migrations (do not write anything)"
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  test                -- to launch base test suite using Pytest"
	@echo "  test-initial        -- to launch tests with pytest and re-initialized database (for after new application or model changes)"
	@echo "  quality             -- to launch Flake8 checking and every tests suites"
	@echo
	@echo "  check-release       -- to check package release before uploading it to PyPi"
	@echo "  release             -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@echo "==== Clear Python cache ===="
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-install:
	@echo ""
	@echo "==== Clear installation ===="
	@echo ""
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_SLUG).egg-info
.PHONY: clean-install

clean-var:
	@echo ""
	@echo "==== Clear var/ directory ===="
	@echo ""
	rm -Rf var
.PHONY: clean-var

clean-doc:
	@echo ""
	@echo "==== Clear documentation ===="
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean: clean-var clean-doc clean-install clean-pycache
.PHONY: clean

venv:
	@echo ""
	@echo "==== Install virtual environment ===="
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
.PHONY: venv

create-var-dirs:
	@mkdir -p var/db
	@mkdir -p var/media
	@mkdir -p var/static
	@mkdir -p $(SANDBOX_DIR)/media
	@mkdir -p $(STATICFILES_DIR)/fonts
.PHONY: create-var-dirs

install: venv create-var-dirs
	@echo ""
	@echo "==== Install everything for development ===="
	@echo ""
	$(PIP) install -e .[dev,frontend,quality,doc,doc-live,release]
	${MAKE} migrate
.PHONY: install

migrations:
	@echo ""
	@echo "==== Making application migrations for application ===="
	@echo ""
	$(DJANGO_MANAGE) makemigrations $(APPLICATION_NAME) sample
.PHONY: migrations

migrate:
	@echo ""
	@echo "==== Apply pending migrations ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) migrate
.PHONY: migrate

superuser:
	@echo ""
	@echo "==== Create new superuser ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) createsuperuser
.PHONY: superuser

run:
	@echo ""
	@echo "==== Running development server ===="
	@echo ""
	@DJANGO_SECRET_KEY=$(DEMO_DJANGO_SECRET_KEY) \
	$(DJANGO_MANAGE) runserver 0.0.0.0:8001
.PHONY: run

css:
	@echo ""
	@echo "==== Building CSS from Sass sources ===="
	@echo ""
	$(BOUSSOLE) compile --config sass/boussole.json
.PHONY: css

watch-sass:
	@echo ""
	@echo "==== Watching Sass sources for CSS rebuild ===="
	@echo ""
	$(BOUSSOLE) watch --config sass/boussole.json
.PHONY: watch-sass

docs:
	@echo ""
	@echo "==== Build documentation ===="
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@echo "==== Watching documentation sources ===="
	@echo ""
	$(SPHINX_RELOAD)
.PHONY: livedocs

check-django:
	@echo ""
	@echo "==== Running Django System check framework ===="
	@echo ""
	$(DJANGO_MANAGE) check
.PHONY: check-django

check-migrations:
	@echo ""
	@echo "==== Checking for pending project applications models migrations ===="
	@echo ""
	$(DJANGO_MANAGE) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

flake:
	@echo ""
	@echo "==== Flake ===="
	@echo ""
	$(FLAKE) --show-source $(APPLICATION_NAME) tests
.PHONY: flake

test:
	@echo ""
	@echo "==== Tests ===="
	@echo ""
	$(PYTEST) -vv --reuse-db tests/
	rm -Rf var/media-tests/
.PHONY: test

test-initial:
	@echo ""
	@echo "==== Tests from zero ===="
	@echo ""
	$(PYTEST) -vv --reuse-db --create-db tests/
	rm -Rf var/media-tests/
.PHONY: test-initial

freeze-dependencies:
	@echo ""
	@echo "==== Freeze dependencies versions ===="
	@echo ""
	$(PYTHON_BIN) freezer.py ${PACKAGE_NAME} --destination=frozen.txt
.PHONY: freeze-dependencies

build-package:
	@echo ""
	@echo "==== Build package ===="
	@echo ""
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@echo "==== Release ===="
	@echo ""
	$(TWINE) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@echo "==== Check package ===="
	@echo ""
	$(TWINE) check dist/*
.PHONY: check-release

tox:
	@echo ""
	@echo "==== Launch tests with Tox environments ===="
	@echo ""
	$(TOX)
.PHONY: tox

quality: test-initial flake docs check-release freeze-dependencies
	@echo ""
	@echo "♥ ♥ Everything should be fine ♥ ♥"
	@echo ""
.PHONY: quality
