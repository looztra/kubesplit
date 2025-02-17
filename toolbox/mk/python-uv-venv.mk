UV_VERSION      := $(shell $(UV_BINARY) --version | awk '{print $$2}' 2> /dev/null)
UV_MIN_VERSION  := 0.4.30
VENV_DIR        ?= .venv

.PHONY: check-uv-version
check-uv-version: check-uv ## Check if uv is installed and version is greater or equal than $(UV_MIN_VERSION) ✂️
	@echo "+ $@"
	@if ! printf '%s\n' "$(UV_MIN_VERSION)" "$(UV_VERSION)" | sort --check=quiet --version-sort; then \
		echo "uv version $(UV_VERSION) is less than $(UV_MIN_VERSION)"; \
		exit 1; \
	else \
		echo "Using uv version $(UV_VERSION) >= $(UV_MIN_VERSION)"; \
	fi

.PHONY: setup-venv
setup-venv: check-uv-version ## ▶ Setup a virtual env for running our python goodness 🎃
	@echo "+ $@"
	@uv sync --frozen --all-packages --keyring-provider subprocess

.PHONY: generate-lock-file
generate-lock-file: check-uv ## ▶ Refresh the lock file 🔒
	@echo "+ $@"
	@uv lock --keyring-provider subprocess

.PHONY: upgrade-dependencies
upgrade-dependencies: check-uv-version ## ▶ Upgrade dependencies (uv.lock and venv) ♨️
	@echo "+ $@"
	@uv sync --upgrade --all-packages --keyring-provider subprocess

.PHONY: update-requirements-file
update-requirements-file: upgrade-dependencies ## ▶ Deprecated, use upgrade-dependencies instead
	@echo "+ $@"
	@echo "This target is deprecated, please use 'upgrade-dependencies' instead"

.PHONY: install-requirements
install-requirements: setup-venv ## ▶ Install requirements in a single command
	@echo "+ $@"
	@echo "This target is not required in a uv context, you can just use 'make setup-venv' instead"

.PHONY: install-all-requirements
install-all-requirements: setup-venv ## ▶ Install all requirements in a single command 🏎️
	@echo "+ $@"
	@echo "This target is not required in a uv context, you can just use 'make setup-venv' instead"

.PHONY: activate-venv
activate-venv: activate-raw-venv ## Activate venv for the current shell ✨
	@echo "+ $@"

.PHONY: generate-requirements-file
generate-requirements-file: generate-lock-file ## Generate the lock file (alias for 'generate-lock-file')

.PHONY: generate-requirements-files
generate-requirements-files: generate-lock-file ## ▶ Generate the lock file (alias for 'generate-lock-file')
	@echo "+ $@"

.PHONY: refresh-workspace
refresh-workspace: ## ▶ Refresh the workspace (use this after adding new members to the uv workspace)
	@echo "+ $@"
	@uv sync --all-packages --keyring-provider subprocess
