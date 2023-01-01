DOCKER_BINARY ?= docker
DOCKER_GUARD  := $(shell command -v ${DOCKER_BINARY} 2> /dev/null)
DOCKER_REPO   ?= looztra
TAG           := ${APP_VERSION}-${GIT_SHA1_DIRTY_MAYBE}
TAG_LATEST    := latest
IMG           := $(DOCKER_REPO)/${APP_NAME}:${TAG}
IMG_LATEST    := $(DOCKER_REPO)/${APP_NAME}:${TAG_LATEST}

.PHONY: check-docker
check-docker: ## Check if docker is installed 🐳
	@echo "+ $@"
ifndef DOCKER_GUARD
	$(error "docker (binary=${DOCKER_BINARY}) is not available please install it")
endif
	@echo "Found docker (binary=${DOCKER_BINARY}) (and that's a good news) 🐳"

.PHONY: check-version
check-version: ## Check that version is set
	@echo "+ $@"
ifndef APP_VERSION
	$(error "Please specify APP_VERSION")
endif

.PHONY: docker-build
docker-build: check-docker check-version ## ▶ Build the docker image 🐳
	@echo "+ $@"
	docker image build \
		--build-arg APP_VERSION=${APP_VERSION} \
		--build-arg GIT_SHA1=${GIT_SHA1_DIRTY_MAYBE} \
		--build-arg GIT_REF=${GIT_REF_SAFE_NAME} \
		-t ${IMG} -f Dockerfile .
ifndef GIT_DIRTY
	docker image tag ${IMG} ${IMG_LATEST}
endif

.PHONY: docker-push
docker-push: check-docker check-version ## Push the docker image with the sha1 tag
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG} (please check that you are logged in)"
	@docker image push ${IMG}
endif

.PHONY: docker-push-latest
docker-push-latest: check-docker check-version ## Push the docker image with tag latest
	@echo "+ $@"
	@echo "Tag ${TAG}"
ifdef GIT_DIRTY
	@echo "Cannot push a dirty image"
else
	@echo "Let's push ${IMG_LATEST} (please check that you are logged in)"
	@docker image push ${IMG_LATEST}
endif
