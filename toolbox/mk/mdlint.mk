MDLINT_CLI_DOCKER_IMAGE ?= davidanson/markdownlint-cli2:v0.6.0

.PHONY: mdlint
mdlint: check-docker ## ▶ Run markdownlint-cli2 on current directory and sub-directories
	@echo "+ $@"
	@echo "Running markdownlint-cli2 in a docker container"
	@if ! test -f .markdownlint-cli2.yaml; then \
		echo "No '.markdownlint-cli2.yaml' file found, so default globs will be used, see <https://github.com/DavidAnson/markdownlint-cli2/tree/main#markdownlint-cli2jsonc>"; \
	fi
	@docker container run -ti \
		--rm \
		-w /app/code \
		-v $(PWD):/app/code \
		$(MDLINT_CLI_DOCKER_IMAGE)

.PHONY: mdlint-fix
mdlint-fix: check-docker ## ▶ Run markdownlint-cli2 fix on current directory and sub-directories
	@echo "+ $@"
	@echo "Running markdownlint-cli2 fix in a docker container"
	@if ! test -f .markdownlint-cli2.yaml; then \
		echo "No '.markdownlint-cli2.yaml' file found, so default globs will be used, see <https://github.com/DavidAnson/markdownlint-cli2/tree/main#markdownlint-cli2jsonc>"; \
	fi
	@docker container run -ti \
		--rm \
		-w /app/code \
		-v $(PWD):/app/code \
		--entrypoint="markdownlint-cli2-fix" \
		$(MDLINT_CLI_DOCKER_IMAGE)
