# APP_MODULE is APP_NAME unless set elsewhere
APP_MODULE          ?= $(shell echo $(APP_NAME)| tr - _ )
IT_TESTS_TARGET     ?= .

.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts
	@echo "+ $@"

.PHONY: clean-build
clean-build: check-find ## Remove build artifacts
	@echo "+ $@"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	$(FIND_CMD) . -name '*.egg-info' -not -path "**/.venv/*" -not -path "**/.tox/*" -exec rm -fr {} +
	$(FIND_CMD) . -name '*.egg' -not -path "**/.venv/*" -not -path "**/.tox/*" -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: check-find ## Remove Python file artifacts
	@echo "+ $@"
	$(FIND_CMD) . -name '*.pyc' -not -path "**/.venv/*" -not -path "**/.tox/*" -exec rm -f {} +
	$(FIND_CMD) . -name '*.pyo' -not -path "**/.venv/*" -not -path "**/.tox/*" -exec rm -f {} +
	$(FIND_CMD) . -name '*~' -not -path "**/.venv/*" -not -path "**/.tox/*" -exec rm -f {} +
	$(FIND_CMD) . -name '__pycache__' -not -path "**/.venv/*" -not -path "**/.tox/*" -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## Remove test and coverage artifacts
	@echo "+ $@"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: test
test: tests ## Wrapper, same as the 'tests' target

.PHONY: unit-tests
unit-tests: tests ## Wrapper, same as the 'tests' target

.PHONY: integration-tests
integration-tests: ## ▶ Run integration tests (if any)
	@echo "+ $@"
	cd $(IT_TESTS_TARGET); bats .

.PHONY: integration-test
integration-test: integration-tests ## Wrapper, same as the 'integration-tests' target

.PHONY: package
package: dist

.PHONY: build
build: lint tests ## ▶ lint and test all in one

.PHONY: echo-app-name
echo-app-name: ## Echo APP_NAME value (used in ci)
	@echo $(APP_NAME)

.PHONY: check-preflight
check-preflight:: ## Preflight/prerequisites checks
	@echo "+ $@"

.PHONY: check-all
check-all: clean lint test integration-test ## Reset cache and test everything
	@echo "+ $@"

.PHONY: show-deps
show-deps: list-installed-dependencies ## ▶ Show dependencies
	@echo "+ $@"

.PHONY: style
style: ## ▶ Run all formatters calling target $(STYLE_TARGETS)
	@echo "+ $@"
	@$(MAKE) --no-print-directory $(STYLE_TARGETS)

.PHONY: lint
lint: ## ▶ Run all linters calling target $(LINT_TARGETS)
	@echo "+ $@"
	@$(MAKE) --no-print-directory $(LINT_TARGETS)

.PHONY: tests
tests: ## ▶ Run tests calling target $(TESTS_TARGETS)
	@echo "+ $@"
	@$(MAKE) --no-print-directory $(TESTS_TARGETS)

.PHONY: dist
dist: ## ▶ Generate packages calling target $(DIST_TARGETS)
	@echo "+ $@"
	@$(MAKE) --no-print-directory $(DIST_TARGETS)

.PHONY: dist-upload
dist-upload: ## ▶ Upload packages calling target $(DIST_UPLOAD_TARGETS)
	@echo "+ $@"
	@$(MAKE) --no-print-directory $(DIST_UPLOAD_TARGETS)
