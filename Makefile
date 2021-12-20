.DEFAULT_GOAL := help

PROG_NAME ?= kubesplit
NAME := looztra/$(PROG_NAME)
CI_PLATFORM := github_actions
GIT_SHA1 := $(shell git rev-parse --short HEAD)
GIT_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
GIT_DIRTY := $(shell git diff --quiet || echo '-dirty')
GIT_SHA1_DIRTY_MAYBE := ${GIT_SHA1}${GIT_DIRTY}
KUBESPLIT_VERSION := $(shell cat setup.cfg | grep current_version | head -n 1 | cut -d " " -f 3)
TAG := ${KUBESPLIT_VERSION}-${GIT_SHA1_DIRTY_MAYBE}
TAG_LATEST := "latest"
IMG := ${NAME}:${TAG}
IMG_LATEST := ${NAME}:${TAG_LATEST}

ifdef GITHUB_RUN_NUMBER
	CI_BUILD_NUMBER := "${GITHUB_RUN_NUMBER}"
else
	CI_BUILD_NUMBER := "N/A"
endif


.PHONY: clean
clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts
	@echo "+ $@"

.PHONY: clean-build
clean-build: ## remove build artifacts
	@echo "+ $@"
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

.PHONY: clean-pyc
clean-pyc: ## remove Python file artifacts
	@echo "+ $@"
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

.PHONY: clean-test
clean-test: ## remove test and coverage artifacts
	@echo "+ $@"
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

.PHONY: style
style: ## force style with black
	@echo "+ $@"
	black --line-length 79 tests $(PROG_NAME)

.PHONY: lint
lint: ## check style with flake8
	@echo "+ $@"
	tox -e linters

.PHONY: all
all: clean lint test integration-test ## Reset cache and test everything
	@echo "+ $@"

.PHONY: tests
tests: ## run tests quickly with the default Python
	@echo "+ $@"
	tox -e py3

.PHONY: test
test: tests ## wrapper
	@echo "+ $@"

.PHONY: unit-tests
unit-tests: tests ## wrapper
	@echo "+ $@"

.PHONY: integration-tests
integration-tests: ## Run integration tests
	@echo "+ $@"
	bats tests.bats

.PHONY: integration-test
integration-test: integration-tests ## Run integration tests

.PHONY: dist-upload
release: dist ## package and upload a release
	@echo "+ $@"
	twine upload dist/*

.PHONY: dist
dist: clean ## builds source and wheel package
	@echo "+ $@"
	python setup.py sdist
	python setup.py bdist_wheel

.PHONY: dist-check
dist-check: ## Check the python3 package
	@echo "+ $@"
	twine check dist/$(PROG_NAME)-${KUBESPLIT_VERSION}-py2.py3-none-any.whl
	twine check dist/$(PROG_NAME)-${KUBESPLIT_VERSION}.tar.gz

.PHONY: install
install: clean ## install the package to the active Python's site-packages
	@echo "+ $@"
	python setup.py install

.PHONY: docker-build
docker-build: ## build docker image from pip package
	@echo "+ $@"
	docker image build \
		--build-arg CI_PLATFORM=${CI_PLATFORM} \
		--build-arg KUBESPLIT_VERSION=${KUBESPLIT_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_BRANCH=${GIT_BRANCH} \
		--build-arg CI_BUILD_NUMBER=${CI_BUILD_NUMBER} \
		-t ${IMG} -f Dockerfile .
ifndef GIT_DIRTY
	docker image tag ${IMG} ${IMG_LATEST}
endif

.PHONY: docker-push
docker-push: ## build docker image from pip package
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
	exit 1
else
	@echo "Let's push ${IMG} (please check that you are logged in)"
	@docker image push ${IMG}
	@docker image push ${IMG_LATEST}
endif

.PHONY: docker-build-local
docker-build-local: clean ## build docker image from local sources
	@echo "+ $@"
	docker image build \
		--build-arg CI_PLATFORM=${CI_PLATFORM} \
		--build-arg KUBESPLIT_VERSION=${KUBESPLIT_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_BRANCH=${GIT_BRANCH} \
		--build-arg CI_BUILD_NUMBER=${CI_BUILD_NUMBER} \
		-t ${IMG} -f local.Dockerfile .
ifndef GIT_DIRTY
	docker image tag ${IMG} ${IMG_LATEST}
endif

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
