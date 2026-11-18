HK_GUARD := $(shell command -v hk 2> /dev/null)

.PHONY: check-hk
check-hk: ## Check if hk is installed 🙉
	@echo "+ $@"
ifndef HK_GUARD
	$(error "hk is not available please install it (https://hk.jdx.dev/getting_started.html)")
endif
	@echo "Found hk 👌"

.PHONY: hk-install
hk-install: check-hk ## ▶ Install the hk git hooks
	@echo "+ $@"
	hk install

.PHONY: hk-check
hk-check: check-hk ## ▶ Run the hk hooks on all files (check mode)
	@echo "+ $@"
	hk check --all

.PHONY: hk-fix
hk-fix: check-hk ## ▶ Run the hk hooks on all files (fix mode)
	@echo "+ $@"
	hk fix --all
