POETRY_GUARD            := $(shell command -v poetry 2> /dev/null)
VENV_DIR                ?= $(shell poetry env info --path)
VENV_PYTHON3            := python3
PYTHON3_GUARD           := $(shell command -v ${VENV_PYTHON3} 2> /dev/null)
ifeq ($(VENV_DIR),)
	VENV_EXISTS             := $(shell ls -d $(VENV_DIR) 2> /dev/null)
endif
VENV_ACTIVATED          := $(shell echo $(VIRTUAL_ENV) 2> /dev/null)
VENV_ACTIVATE_FISH_CMD  := source $(VENV_DIR)/bin/activate.fish
VENV_ACTIVATE_OTHER_CMD := source $(VENV_DIR)/bin/activate
POETRY_INSTALL_SYNC_OPT := true

.PHONY: check-poetry
check-poetry: ## Check if poetry is installed 🐍
	@echo "+ $@"
ifndef POETRY_GUARD
	$(error "python3 is not available please install it")
endif
	@echo "Found poetry at '${POETRY_GUARD}' (and that's a good news)"

.PHONY: check-python3
check-python3: ## Check if python3 is installed 🐍
	@echo "+ $@"
ifndef PYTHON3_GUARD
	$(error "python3 is not available please install it")
endif
	@echo "Found ${VENV_PYTHON3} (and that's a good news)"

.PHONY: check-venv-exists
check-venv-exists: ## Check if venv is created 🙉
	@echo "+ $@"
ifdef VENV_EXISTS
	$(error "no venv dir found, please create it first with 'make setup-venv'")
else
	@echo "Found venv at path '$(VENV_DIR)' (and that's a good news)"
endif

.PHONY: setup-venv
setup-venv: check-python3 ## ▶ Setup a virtual env for running our python goodness 🎃
	@echo "+ $@"
ifdef VENV_EXISTS
	@poetry install --sync
else
	@echo "Doing nothing, venv already setup at path [$(VENV_DIR)]"
endif


.PHONY: delete-venv
delete-venv: ## ▶ Delete venv
	@echo "+ $@"
	@if [ -d $(VENV_DIR) ]; then \
		echo "Deleting directory [$(VENV_DIR)]"; \
		rm -rf $(VENV_DIR); \
	else \
		echo "Nothing to do, directory [$(VENV_DIR)] does not exist"; \
	fi

.PHONY: venv
venv: setup-venv

.PHONY: activate-venv
activate-venv: check-python3 check-venv-exists ## Activate venv for the current shell ✨
	@echo "+ $@"
	@echo "Activating venv for shell [$(CURRENT_SHELL)]"
	@echo "please exec the current command: "
	@echo "------------>"
	@if [[ "$(CURRENT_SHELL)" == "fish" ]]; then \
		echo $(VENV_ACTIVATE_FISH_CMD); \
	else \
		echo $(VENV_ACTIVATE_OTHER_CMD); \
	fi
	@echo "<------------"

.PHONY: echo-venv-activate-cmd
echo-venv-activate-cmd: SHELL := $(WHICH_BASH)
echo-venv-activate-cmd: ## ▶ Echo the command to use to activate the venv
	@if [[ "$(CURRENT_SHELL)" == "fish" ]]; then \
		echo $(VENV_ACTIVATE_FISH_CMD); \
	else \
		echo $(VENV_ACTIVATE_OTHER_CMD); \
	fi

.PHONY: check-venv-is-ready
check-venv-is-ready: ## Check if venv is ready
	echo "+ $@"

.PHONY: check-venv-is-activated
check-venv-is-activated: ## Check if venv is activated 👻
	@echo "+ $@"
ifndef VENV_ACTIVATED
	$(error "venv does not seem to be activated, please activate it with 'make activate-venv'")
endif
	@echo "venv activated (and that's a good news)"
	@echo "Running venv from [${VIRTUAL_ENV}]"

.PHONY: exit-venv
exit-venv: check-venv-is-activated ## Exit venv (deactivate) 👋
	@echo "+ $@"
	@echo "Please exec the command:"
	@echo "deactivate"

.PHONY: poetry-lock
poetry-lock: ## ▶ Update poetry lockfile
	@echo "+ $@"
	@poetry lock

.PHONY: update-requirements-file
update-requirements-file: SHELL := $(WHICH_BASH)
update-requirements-file: ## ▶ Generate requirements.txt from poetry
	@echo "+ $@"
	@if [ -f pyproject.toml ]; then \
		if [ ! -f poetry.lock ]; then \
			poetry lock; \
		fi; \
		poetry export --format=requirements.txt --with dev --without-hashes --output=requirements.txt; \
	else \
		echo "No pyproject.toml file, skipping."; \
	fi

#.PHONY: update-dev-requirements-file
#update-dev-requirements-file: SHELL := $(WHICH_BASH)
#update-dev-requirements-file: poetry-lock ## ▶ Generate dev requirements.txt from poetry
#	@echo "+ $@"
#	@if [ -f pyproject.toml ]; then \
#		poetry export --only=dev --format=requirements.txt --without-hashes --output=requirements_dev_only.txt;\
#	else \
#		echo "No requirements.in file, skipping."; \
#	fi

.PHONY: install-all-requirements
install-all-requirements: SHELL := $(WHICH_BASH)
install-all-requirements: ## ▶ Install all requirements in a single command (requires make install-requirements)
	@echo "+ $@"
ifeq ($(POETRY_INSTALL_SYNC_OPT),true)
	$(eval POETRY_INSTALL_SYNC_OPT_STRING = --sync)
else
	$(eval POETRY_INSTALL_SYNC_OPT_STRING = )
endif
	poetry install $(POETRY_INSTALL_SYNC_OPT_STRING)

# .PHONY: update-all-requirements-files
# update-all-requirements-files: update-requirements-file update-dev-requirements-file ## ▶ Update all requirements files
