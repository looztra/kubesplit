# APP_MODULE is APP_NAME unless set elsewhere
APP_MODULE          ?= $(shell echo $(APP_NAME)| tr - _ )
IT_TESTS_TARGET     ?= .
TOX_ARGS            ?=

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts
	@echo "+ $@"

.PHONY: clean-build
clean-build: check-find ## Remove build artifacts
	@echo "+ $@"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(FIND_CMD) . -name '*.egg-info' -exec rm -fr {} +
	$(FIND_CMD) . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: check-find ## Remove Python file artifacts
	@echo "+ $@"
	$(FIND_CMD) . -name '*.pyc' -exec rm -f {} +
	$(FIND_CMD) . -name '*.pyo' -exec rm -f {} +
	$(FIND_CMD) . -name '*~' -exec rm -f {} +
	$(FIND_CMD) . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts
	@echo "+ $@"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: style
style: SHELL := $(WHICH_BASH)
style: check-venv-is-ready ## ▶ force style with black and isort
	@echo "+ $@"
	@echo "Enforce code format with black"
	@black --line-length 119 .
	@echo "Ordering import with isort..."
	@isort --line-width 119 --dont-order-by-type --profile black .
	@echo "🦾 Done!"

.PHONY: lint
lint: SHELL := $(WHICH_BASH)
lint: check-venv-is-ready # ▶ Run tox -e linters
	@echo "+ $@"
	@declare -a tox_args=(); \
	if [ -n "$(TOX_ARGS)" ]; then \
		tox_args+=($(TOX_ARGS)); \
	fi; \
	tox $${tox_args[@]} -e linters

.PHONY: tests
tests: SHELL := $(WHICH_BASH)
tests: check-venv-is-ready ## ▶ Run tests quickly with the default Python
	@echo "+ $@"
	@declare -a tox_args=(); \
	if [ -n "$(TOX_ARGS)" ]; then \
		tox_args+=($(TOX_ARGS)); \
	fi; \
	tox $${tox_args[@]} -e py3

.PHONY: test
test: tests ## Wrapper, same as the 'tests' target
	@echo "+ $@"

.PHONY: unit-tests
unit-tests: tests ## Wrapper, same as the 'tests' target
	@echo "+ $@"

.PHONY: integration-tests
integration-tests: check-venv-is-ready ## ▶ Run integration tests (if any)
	@echo "+ $@"
	cd $(IT_TESTS_TARGET); bats .

.PHONY: integration-test
integration-test: integration-tests ## Wrapper, same as the 'integration-tests' target

.PHONY: dist
dist: SHELL := $(WHICH_BASH)
dist: check-venv-is-ready ## ▶ Build python3 package
	@echo "+ $@"
	@poetry build

.PHONY: package
package: dist

.PHONY: build
build: lint tests ## ▶ lint and test all in one

.PHONY: dist-upload
dist-upload: check-venv-is-ready ## Upload the python3 package to pypi
	poetry publish

.PHONY: echo-app-name
echo-app-name: ## Echo APP_NAME value (used in ci)
	@echo $(APP_NAME)

.PHONY: check-all
check-all: clean lint test integration-test ## Reset cache and test everything
	@echo "+ $@"
