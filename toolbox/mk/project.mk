.PHONY: build-docs
build-docs: ## ▶ Build the documentation
	@echo "Building the documentation"
	@uv run mkdocs build --site-dir generated/mkdocs/HEAD

.PHONY: serve-docs
serve-docs: ## ▶ Serve the documentation
	@echo "Serving the documentation"
	@uv run mkdocs serve
