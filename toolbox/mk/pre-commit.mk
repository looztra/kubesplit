PRECOMMIT_GUARD := $(shell command -v pre-commit 2> /dev/null)

.PHONY: check-precommit
check-precommit: ## Check if pre-commit is installed 🙉
	@echo "+ $@"
ifndef PRECOMMIT_GUARD
	$(error "pre-commit is not available please install it (https://pre-commit.com/#install)")
endif
	@echo "Found pre-commit 👌"

.PHONY: precommit-install
precommit-install: check-precommit ## ▶ Install pre-commit hooks
	@echo "+ $@"
	pre-commit install

.PHONY: precommit-run
precommit-run: check-precommit ## ▶ Run pre-commit hooks
	@echo "+ $@"
	pre-commit run --show-diff-on-failure --color=always --all-files

.PHONY: pre-commit-run
pre-commit-run: precommit-run ## Alias for 'precommit-run'

.PHONY: pre-commit-install
pre-commit-install: precommit-install ## Alias for 'precommit-install'
