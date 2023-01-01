WHICH_BASH_     ?= $(shell which bash)
SHA256SUM_GUARD := $(shell command -v sha256sum 2> /dev/null)
LOCAL_MK_CACHE  ?= generated/mk
REMOTE_MK_REPO  ?= looztra/toolbox
REMOTE_MK_DIR   ?= toolbox/mk

# $1: mk file without .mk extension
# $2: mk file sha256 signature
# $3: git ref
define get_remote_mk
	@echo "+ retreiving $@"
	@mkdir -p $(LOCAL_MK_CACHE)
	@GITHUB_API_TOKEN=$${GITHUB_API_TOKEN:-$$GITHUB_TOKEN}; \
	if [ -z "$${GITHUB_API_TOKEN}" ]; then \
		echo -e "\e[0;31m**ERROR** please set either GITHUB_API_TOKEN or GITHUB_TOKEN\e[m"; \
		echo -e "\e[0;33mThis is the next error message (Makefile:xx: $(LOCAL_MK_CACHE)/$(1).mk: No such file or directory) root cause!\e[m"; \
		exit 1; \
	fi; \
	curl \
		-o $(LOCAL_MK_CACHE)/$(1).fetched.mk \
		-L "https://whatever:$(GITHUB_API_TOKEN)@raw.githubusercontent.com/$(REMOTE_MK_REPO)/$(3)/$(REMOTE_MK_DIR)/$(1).mk"
	@echo "$(2) *$(LOCAL_MK_CACHE)/$(1).fetched.mk" \
		| sha256sum --check - && \
		mv $(LOCAL_MK_CACHE)/$(1).fetched.mk $(LOCAL_MK_CACHE)/$(1).mk
endef

.PHONY: check-sha256sum
check-sha256sum: ## Check if sha256sum is installed 🙉
	@echo "+ $@"
ifndef SHA256SUM_GUARD
	$(error "sha256sum is not available please install it")
endif


.PHONY: init-mk
init-mk: check-sha256sum ## ▶ no-op target to make sure all remote targets are downloaded
	@echo "+ $@"

.PHONY: clear-mk-cache
clear-mk-cache: ## ▶ Clear make target cache
	@echo "+ $@"
	@mkdir -p $(LOCAL_MK_CACHE)
	@rm -rf $(LOCAL_MK_CACHE)/*.mk

$(LOCAL_MK_CACHE)/%.mk: SHELL := $(WHICH_BASH_)
$(LOCAL_MK_CACHE)/%.mk: Makefile
	$(eval MK_NAME = $(shell echo $@ | cut -d "/" -f3 | cut -d "." -f1))
	@echo "Working on remote mk [$(MK_NAME)]"
	$(eval MK_NAME_UPPER = $(shell echo $(MK_NAME) | tr '[:lower:]' '[:upper:]' | tr '-' '_'))
	$(eval MK_SHA256_VAR_NAME= MK_$(MK_NAME_UPPER)_SHA256)
	$(eval MK_SHA256_VALUE = $($(MK_SHA256_VAR_NAME)))
	@if [ -z "$(MK_SHA256_VALUE)" ]; then \
		echo -e "\e[31m**ERROR** Cannot find the SHA256 signature for remote mk [$(MK_NAME)], please define variable [$(MK_SHA256_VAR_NAME)]\e[0m"; \
		echo; \
		exit 1; \
	fi
	$(call get_remote_mk,$(MK_NAME),$(MK_SHA256_VALUE),$(MK_GIT_REF))
