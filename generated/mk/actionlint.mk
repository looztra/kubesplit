ACTIONLINT_GUARD  := $(shell command -v actionlint 2> /dev/null)

.PHONY: check-actionlint
check-actionlint: ## Check if actionlint is installed
	@echo "+ $@"
ifndef ACTIONLINT_GUARD
	$(error "actionlint is not available please install it, see https://github.com/rhysd/actionlint/")
endif
	@echo "Found actionlint 👌"

.PHONY: actionlint
actionlint: check-actionlint ## ▶ Run actionlint on current directory and sub-directories
	@echo "+ $@"
	@echo "Running actionlint on current directory and sub-directories"
	@actionlint
