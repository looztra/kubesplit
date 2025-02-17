UV_BINARY           := uv
UV_GUARD            := $(shell command -v $(UV_BINARY) 2> /dev/null)

.PHONY: check-uv
check-uv: ## Check if uv is installed 🐍
	@echo "+ $@"
ifndef UV_GUARD
	error "$(UV_BINARY) is not available please install it"
endif
	@echo "Using $(UV_BINARY) at '${UV_GUARD}'"
