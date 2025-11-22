# Copilot instructions

## Project

- This project is located in the following [GitHub Repository](https://github.com/looztra/kubesplit).
- This is a repository hosting a python project. The main branch is `main`.

## Pull requests and commits

- When creating a pull request, ensure the title is descriptive and follows the format `feat: <description>` for new features, `fix: <description>` for bug fixes, or `chore: <description>` for maintenance tasks.
- Please take a look at [Conventional Commit](https://www.conventionalcommits.org/en/v1.0.0/) specifications for more details about this.
- When committing code, use clear and concise commit messages that follow the same format as pull request titles.
- When creating pull requests, ensure that you follow the [Pull Request Template](https://github.com/looztra/kubesplit/blob/main/.github/PULL_REQUEST_TEMPLATE.md) to provide a clear description of the changes made, the reason for the changes, and any relevant context.
- If the pull request is related to an issue, include a link to the issue in the pull request description in the format `Fixes #<issue_number>` in the section `## Link to the initial request/ticket`. If the Pull Request is not related to an issue, you can remove this section.

## Coding style

### General

- Always conform to the coding styles defined in `.editorconfig` when you write code.
- Ensure there is no trailing whitespace at the end of lines.
- Ensure files end in a newline and only a newline.

### Markdown files

- Follow the instructions from <https://github.com/github/awesome-copilot/blob/main/instructions/markdown.instructions.md> when writing markdown files.
- Always conform to the coding styles defined in `.markdownlint.yaml` when you write markdown files.

### Python files

- We use `uv` to manage python dependencies and virtual environments.

### General Instructions

- Always prioritize readability and clarity.
- For algorithm-related code, include explanations of the approach used.
- Write code with good maintainability practices, including comments on why certain design decisions were made.
- Handle edge cases and write clear exception handling.
- Use consistent naming conventions and follow language-specific best practices.
- Write concise, efficient, and idiomatic code that is also easily understandable.

### Style guides

- We use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as the coding style for Python files.
- We use [PEP 257](https://www.python.org/dev/peps/pep-0257/) for docstrings in Python files.
- We use one-line docstrings for functions that do not raise exceptions, and multi-line docstrings for function that do raise exceptions.
- Python modules and packages contain a docstring at the top of the file, which describes the module's purpose and functionality
- Python packages contain an explicit `__init__.py` file.
- When writing code, ensure that it is well-structured and follows the principles of clean code.
- When writing code, ensure that it is well-documented comments where necessary.

- We use f-strings for string formatting except when writing log statements.

### Testing

- Tests are located in the `tests` directory and follow the naming convention `test_*.py`.
- If a function or class is located in a module named `foo.py`, the test file should be named `test_foo.py`.

- When writing tests, use the `pytest` framework and ensure that all tests are passing before submitting a pull request.
- When using `pytest.mark.parametrize`:
  - always use a tuple for the parameters, even if there is only one parameter.
  - the content of the `argvalues` parameter should be a list of `pytest.param(...)` objects, which allows you to specify additional metadata for each test case, such as `id`, `marks`, and `xfail`.

- When writing code or tests, respect as much as possible the pylint rule `Import outside toplevel (import-outside-toplevel)` and the ruff rule [PLC0415](https://docs.astral.sh/ruff/rules/import-outside-top-level/).

- When writing tests, ensure that you use fixtures to set up the test environment.
- Write custom fixtures in the `conftest.py` file located in the `tests` directory and use the `@pytest.fixture` decorator to define and declare the name of the fixture through the `name` parameter of `@pytest.fixture`

### Checking code

- Before submitting a pull request, ensure that you have run the following commands with success to check your code:

  ```bash
  ruff format --check
  ruff check
  ```

- When running these checks in vscode, use `uv run` to execute the commands, as it ensures that the correct virtual environment is used.
