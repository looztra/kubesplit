UV_TESTS_WITH_COVERAGE_SCRIPT_NAME ?= pytest:cov
UV_LINT_ALL_SCRIPT_NAME            ?= lint:all
UV_STYLE_SCRIPT_NAME               ?= style
STYLE_TARGETS                      ?= style-uv-default
LINT_TARGETS                       ?= lint-uv-default
TESTS_TARGETS                      ?= tests-uv-default
DIST_TARGETS                       ?= dist-uv-default
DIST_UPLOAD_TARGETS                ?= dist-upload-uv-default
TWINE_UPLOAD_TARGET                ?= dist/*.whl
UV_PACKAGE_LIST                    ?= all
UV_TASK_RUNNER                     ?= poe
UV_RUN_OPTIONS                     ?= --frozen

.PHONY: style-uv-default
style-uv-default: check-uv ## Enforce style with task '$(UV_STYLE_SCRIPT_NAME)'
	@echo "+ $@"
	@uv run $(UV_RUN_OPTIONS) $(UV_TASK_RUNNER) $(UV_STYLE_SCRIPT_NAME)
	@echo "🦾 Done!"

.PHONY: fast-lint
fast-lint: check-uv ## ▶ Run ruff check
	@echo "+ $@"
	@uv run $(UV_RUN_OPTIONS) ruff check
	@echo "🦾 Done!"

.PHONY: lint-uv-default
lint-uv-default: check-uv ## Run all linters with task '$(UV_LINT_ALL_SCRIPT_NAME)'
	@echo "+ $@"
	@uv run $(UV_RUN_OPTIONS) $(UV_TASK_RUNNER) $(UV_LINT_ALL_SCRIPT_NAME)

.PHONY: tests-no-coverage
tests-no-coverage: check-uv check-prerequisites-pytest ## ▶ Run tests quickly (no coverage) 🚀
	@echo "+ $@"
	@uv run $(UV_RUN_OPTIONS) pytest

.PHONY: tests-with-coverage
tests-with-coverage: check-uv check-prerequisites-pytest ## ▶ Run tests with coverage
	@echo "+ $@"
	@uv run $(UV_RUN_OPTIONS) $(UV_TASK_RUNNER) $(UV_TESTS_WITH_COVERAGE_SCRIPT_NAME)

.PHONY: tests-uv-default
tests-uv-default: tests-with-coverage ## Run tests (defaults to tests-with-coverage)
	@echo "+ $@"

.PHONY: dist-uv-default
dist-uv-default: SHELL := $(WHICH_BASH)
dist-uv-default: check-uv ## Build python package(s) default target (called by "make dist") if not overriden
	@echo "+ $@"
	@if [[ "$(UV_PACKAGE_LIST)" == "all" ]] ; then \
		uv build --wheel --all; \
	else \
		for package in $(UV_PACKAGE_LIST) ; \
		do \
			uv build --wheel --package $$package ; \
		done \
	fi

.PHONY: dist-upload-uv-default
dist-upload-uv-default: ## Upload the python3 package
	@echo "+ $@"
# @uv publish FIXME

.PHONY: list-installed-dependencies
list-installed-dependencies: check-uv ## ▶ List installed dependencies
	@echo "+ $@"
	@uv tree --frozen

.PHONY: check-prerequisites-pytest
check-prerequisites-pytest: SHELL := $(WHICH_BASH)
check-prerequisites-pytest: ## Check if pytest is in the .venv
	@echo "+ $@"
	@if uv run $(UV_RUN_OPTIONS) pytest --version > /dev/null 2>&1; then \
		echo "'pytest' found in venv, everything seems ok"; \
	else \
		echo "No 'pytest' found in the venv, did you run 'make setup-venv'?"; \
		exit 1; \
	fi
