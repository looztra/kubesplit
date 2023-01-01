.DEFAULT_GOAL := help
#
IS_GIT_CONTEXT := $(shell git rev-parse --short HEAD > /dev/null 2>&1 || echo "not-git")

ifneq ($(IS_GIT_CONTEXT),not-git)
ifdef GITHUB_SHA_SHORT
	GIT_SHA1 := $(GITHUB_SHA_SHORT)
else
	GIT_SHA1 := $(shell git rev-parse --short HEAD || echo "not.git")
endif
ifdef GITHUB_REF
	GIT_REF := $(GITHUB_REF)
else
	GIT_REF := $(shell git describe --tags --exact-match 2>/dev/null || git symbolic-ref -q --short HEAD || echo "not.git")
endif
ifdef GITHUB_HEAD_REF_SLUG
	GIT_REF_SAFE_NAME    = $(GITHUB_HEAD_REF_SLUG)
else
ifdef GITHUB_EVENT_REF_SLUG
	GIT_REF_SAFE_NAME    = $(GITHUB_EVENT_REF_SLUG)
else
	GIT_REF_SAFE_NAME    = $(shell echo $(GIT_REF) | tr "/" "-")
endif
endif
GIT_STATUS_LINES_COUNT := $(shell git status --porcelain --untracked-files | wc -l || echo "not.git")
else
	GIT_SHA1 := not.git
	GIT_REF := not.git
	GIT_REF_SAFE_NAME := not.git
	GIT_STATUS_LINES_COUNT := 0
endif
ifeq ($(GIT_STATUS_LINES_COUNT),0)
	GIT_IS_DIRTY :=
else
	GIT_IS_DIRTY := dirty
endif
ifdef GIT_IS_DIRTY
	GIT_SHA1_DIRTY_MAYBE     := $(GIT_SHA1)-$(GIT_IS_DIRTY)
	GIT_SHA1_DIRTY_MAYBE_DOT := $(GIT_SHA1).$(GIT_IS_DIRTY)
else
	GIT_SHA1_DIRTY_MAYBE     := $(GIT_SHA1)
	GIT_SHA1_DIRTY_MAYBE_DOT := $(GIT_SHA1)
endif
ifeq ($(OS),Windows_NT)
	detected_OS := Windows
else
	detected_OS := $(shell sh -c 'uname 2>/dev/null || echo Unknown')
endif
# Check Find Command
# See https://stackoverflow.com/a/14777895/295716
ifeq ($(detected_OS),Darwin)        # Mac OS X
	FIND_CMD := gfind
else
	FIND_CMD := find
endif
#
PWD           := $(shell pwd)
FZF_GUARD     := $(shell command -v fzf 2> /dev/null)
WHICH_BASH    ?= $(shell which bash)
CURRENT_SHELL ?= $(shell echo $$SHELL | rev | cut -d "/" -f 1 | rev)
FIND_GUARD    := $(shell command -v ${FIND_CMD} 2> /dev/null)

.PHONY: git-status-extended
git-status-extended:
	@echo "+ $@"
	@git status --porcelain --untracked-files

.PHONY: is-git-dirty
is-git-dirty: ## Echo dirty if git repo is dirty 🚽
	@echo ${GIT_IS_DIRTY}

.PHONY: check-fzf
check-fzf: ## Check if fzf is installed
	@echo "+ $@"
ifndef FZF_GUARD
	$(error "fzf is not available please install it")
endif
	@echo "Found fzf 👌"

.PHONY: check-find
check-find: ## Check if find is installed
	@echo "+ $@"
ifndef FIND_GUARD
	$(error "$(FIND_CMD) is not available please install it (brew install findutils on macOS).")
endif
	@echo "Found $(FIND_CMD) 👌"

print-%: ## Print the current value of a variable
	@echo '$($*)'

.PHONY: help
help: ## ▶ Print MAIN targets 🆘
	@echo "+ $@"
	@grep -E '^[%a-zA-Z0-9_-]+:.*?## ▶ .*$$' $(MAKEFILE_LIST) \
			| cut -d ":" -f2- \
			| sort \
			| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-36s\033[0m %s\n", $$1, $$2}'

.PHONY: help-all
help-all: ## ▶ Print ALL targets 🧻
	@echo "+ $@"
	@printf "\033[1m\033[5m\033[38;5;208mTop level targets flagged with \033[93m▶\033[25m\033[0m\n"
	@grep -E '^[%a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
			| cut -d ":" -f2- \
			| sort \
			| awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-36s\033[0m %s\n", $$1, $$2}'

menu: SHELL := $(WHICH_BASH)
.PHONY: menu
menu: check-fzf ## ▶ Display the interactive menu with top-level targets 🌶️
	@top_level_targets=$$( grep -E '^[%a-zA-Z0-9_-]+:.*?## ▶ .*$$' $(MAKEFILE_LIST) | grep -v menu | cut -d ":" -f2 | tr '\n' ' ') ; \
	selected_item=$$( echo $$top_level_targets | tr ' ' '\n' | sort | fzf) ; \
	$(MAKE) $$selected_item

menu-all: SHELL := $(WHICH_BASH)
.PHONY: menu-all
menu-all: check-fzf ## ▶ Display the interactive menu with all targets 🍍
	@top_level_targets=$$( grep -E '^[%a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | grep -v menu | cut -d ":" -f2 | tr '\n' ' ') ; \
	selected_item=$$( echo $$top_level_targets | tr ' ' '\n' | sort | fzf) ; \
	$(MAKE) $$selected_item
