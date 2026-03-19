PYTHON_INTERPRETER=python3
VENV_PATH=.venv

FRONTEND_DIR=frontend
SANDBOX_DIR=sandbox
STATICFILES_DIR=$(SANDBOX_DIR)/static-sources

BOUSSOLE_BIN=$(VENV_PATH)/bin/boussole
FLAKE_BIN=$(VENV_PATH)/bin/flake8
PYTEST_BIN=$(VENV_PATH)/bin/pytest
PYTHON_BIN=$(VENV_PATH)/bin/python
PIP_BIN=$(VENV_PATH)/bin/pip
TOX_BIN=$(VENV_PATH)/bin/tox
TWINE_BIN=$(VENV_PATH)/bin/twine

DJANGO_MANAGE=manage.py
SPHINX_RELOAD=$(PYTHON_BIN) docs/sphinx_reload.py

PACKAGE_NAME=django-smart-media
PACKAGE_SLUG=django_smart_media
APPLICATION_NAME=smart_media

# Formatting variables, FORMATRESET is always to be used last to close formatting
FORMATBLUE:=$(shell tput setab 4)
FORMATGREEN:=$(shell tput setab 2)
FORMATRED:=$(shell tput setab 1)
FORMATBOLD:=$(shell tput bold)
FORMATRESET:=$(shell tput sgr0)

help:
	@echo "Please use 'make <target> [<target>...]' where <target> is one of"
	@echo
	@echo "  Installation"
	@echo "  ============"
	@echo
	@echo "  install             -- to install this project with virtualenv and Pip"
	@echo "  freeze-dependencies -- to write a frozen.txt file with installed dependencies versions"
	@echo
	@echo "  Cleaning"
	@echo "  ========"
	@echo
	@echo "  clean               -- to clean EVERYTHING (Warning)"
	@echo "  clean-var           -- to clean data (uploaded medias, database, etc..)"
	@echo "  clean-doc           -- to remove documentation builds"
	@echo "  clean-install       -- to clean Python side installation"
	@echo "  clean-pycache       -- to remove all __pycache__, this is recursive from current directory"
	@echo
	@echo "  Django commands"
	@echo "  ==============="
	@echo
	@echo "  run                 -- to run Django development server"
	@echo "  migrations          -- to create new migrations for application after changes"
	@echo "  migrate             -- to apply demo database migrations"
	@echo "  superuser           -- to create a superuser for Django admin"
	@echo
	@echo "  Frontend commands"
	@echo "  ================="
	@echo
	@echo "  css                 -- to build uncompressed CSS from Sass sources"
	@echo "  watch-css           -- to watch for Sass changes to rebuild CSS"
	@echo "  css-prod            -- to build compressed and minified CSS from Sass sources"
	@echo "  js                  -- to build uncompressed Javascript from sources"
	@echo "  watch-js            -- to watch for Javascript sources changes to rebuild assets"
	@echo "  js-prod             -- to build minified JS assets"
	@echo "  frontend            -- to build uncompressed frontend assets (CSS, JS, etc..)"
	@echo "  frontend-prod       -- to build minified frontend assets (CSS, JS, etc..)"
	@echo
	@echo "  Documentation"
	@echo "  ============="
	@echo
	@echo "  docs                -- to build documentation"
	@echo "  livedocs            -- to run livereload server to rebuild documentation on source changes"
	@echo
	@echo "  Quality"
	@echo "  ======="
	@echo
	@echo "  check-django        -- to run Django System check framework"
	@echo "  check-migrations    -- to check for pending application migrations (do not write anything)"
	@echo "  check-release       -- to check package release before uploading it to PyPi"
	@echo "  flake               -- to launch Flake8 checking"
	@echo "  test                -- to launch base test suite using Pytest"
	@echo "  test-initial        -- to launch tests with pytest and re-initialized database (for after new application or model changes)"
	@echo "  quality             -- to launch Flake8 checking and every tests suites"
	@echo "  tox                 -- to launch tests for every Tox environments"
	@echo
	@echo "  Release"
	@echo "  ======="
	@echo
	@echo "  release             -- to release package for latest version on PyPi (once release has been pushed to repository)"
	@echo

clean-pycache:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear Python cache <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf .pytest_cache
	find . -type d -name "__pycache__"|xargs rm -Rf
	find . -name "*\.pyc"|xargs rm -f
.PHONY: clean-pycache

clean-backend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear installation <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf dist
	rm -Rf $(VENV_PATH)
	rm -Rf $(PACKAGE_SLUG).egg-info
.PHONY: clean-install

clean-var:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear 'var/' directory <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf var
.PHONY: clean-var

clean-doc:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Clear documentation <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf docs/_build
.PHONY: clean-doc

clean-frontend-build:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend built files <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(STATICFILES_DIR)/webpack-stats.json
	rm -Rf $(STATICFILES_DIR)/css
	rm -Rf $(STATICFILES_DIR)/js
.PHONY: clean-frontend-build

clean-frontend-install:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Cleaning frontend install <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(FRONTEND_DIR)/node_modules
.PHONY: clean-frontend-install

clean: clean-var clean-doc clean-backend-install clean-frontend-install clean-frontend-build clean-pycache
.PHONY: clean

create-var-dirs:
	@mkdir -p var/db
	@mkdir -p var/media
	@mkdir -p var/static
	@mkdir -p $(SANDBOX_DIR)/media
	@mkdir -p $(STATICFILES_DIR)/fonts
.PHONY: create-var-dirs

venv:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install virtual environment <---$(FORMATRESET)\n"
	@echo ""
	virtualenv -p $(PYTHON_INTERPRETER) $(VENV_PATH)
.PHONY: venv

install-backend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Install everything for development <---$(FORMATRESET)\n"
	@echo ""
	$(PIP_BIN) install -e .[dev,quality,doc,doc-live,release]
.PHONY: install-backend

install-icon-font:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Copying bootstrap-icons to staticfiles directory <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf $(STATICFILES_DIR)/fonts/icons
	mkdir -p $(STATICFILES_DIR)/fonts
	cp -r $(FRONTEND_DIR)/node_modules/bootstrap-icons/font/fonts $(STATICFILES_DIR)/fonts/icons
.PHONY: install-icon-font

install-frontend:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Installing frontend requirements <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm install
	${MAKE} install-icon-font
.PHONY: install-frontend

install: venv create-var-dirs install-backend migrate install-frontend frontend
.PHONY: install

migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Making application migrations <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) $(DJANGO_MANAGE) makemigrations $(APPLICATION_NAME) sample
.PHONY: migrations

migrate:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Apply pending migrations <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) $(DJANGO_MANAGE) migrate
.PHONY: migrate

superuser:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Create new superuser <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) $(DJANGO_MANAGE) createsuperuser
.PHONY: superuser

run:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running development server <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) $(DJANGO_MANAGE) runserver 0.0.0.0:8001
.PHONY: run

css:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building CSS for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css
.PHONY: css

watch-sass:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching Sass sources for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script watch-css
.PHONY: watch-sass

css-prod:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building CSS for production environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run-script css-prod
.PHONY: css-prod

js:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building distributed Javascript for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run js
.PHONY: js

watch-js:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching Javascript sources for development environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run watch-js
.PHONY: watch-js

js-prod:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Building distributed Javascript for production environment <---$(FORMATRESET)\n"
	@echo ""
	cd $(FRONTEND_DIR) && npm run js-prod
.PHONY: js-prod

frontend: css js
.PHONY: frontend

frontend-prod: css-prod js-prod
.PHONY: frontend-prod

docs:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Build documentation <---$(FORMATRESET)\n"
	@echo ""
	cd docs && make html
.PHONY: docs

livedocs:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Watching documentation sources <---$(FORMATRESET)\n"
	@echo ""
	$(SPHINX_RELOAD)
.PHONY: livedocs

check-django:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Running Django System check <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) $(DJANGO_MANAGE) check
.PHONY: check-django

check-migrations:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Checking for pending backend model migrations <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) $(DJANGO_MANAGE) makemigrations --check --dry-run -v 3
.PHONY: check-migrations

flake:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Flake <---$(FORMATRESET)\n"
	@echo ""
	$(FLAKE_BIN) --show-source $(APPLICATION_NAME) tests
.PHONY: flake

test:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Tests <---$(FORMATRESET)\n"
	@echo ""
	$(PYTEST_BIN) -vv --reuse-db tests/
	rm -Rf var/media-tests/
.PHONY: test

test-initial:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Tests from zero <---$(FORMATRESET)\n"
	@echo ""
	$(PYTEST_BIN) -vv --reuse-db --create-db tests/
	rm -Rf var/media-tests/
.PHONY: test-initial

freeze-dependencies:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Freeze dependencies versions <---$(FORMATRESET)\n"
	@echo ""
	$(PYTHON_BIN) freezer.py ${PACKAGE_NAME} --destination=frozen.txt
.PHONY: freeze-dependencies

build-package:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Build package <---$(FORMATRESET)\n"
	@echo ""
	rm -Rf dist
	$(PYTHON_BIN) setup.py sdist
.PHONY: build-package

release: build-package
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Release package <---$(FORMATRESET)\n"
	@echo ""
	$(TWINE_BIN) upload dist/*
.PHONY: release

check-release: build-package
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Check package <---$(FORMATRESET)\n"
	@echo ""
	$(TWINE_BIN) check dist/*
.PHONY: check-release

tox:
	@echo ""
	@printf "$(FORMATBLUE)$(FORMATBOLD)---> Launch all Tox environments <---$(FORMATRESET)\n"
	@echo ""
	$(TOX_BIN)
.PHONY: tox

quality: check-django check-migrations test-initial flake docs check-release freeze-dependencies
	@echo ""
	@printf "$(FORMATGREEN)$(FORMATBOLD) ♥ ♥ Everything should be fine ♥ ♥ $(FORMATRESET)\n"
	@echo ""
	@echo ""
.PHONY: quality
