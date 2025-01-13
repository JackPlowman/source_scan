# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    poetry install -E dev

# Install application python dependencies only
install-root-only:
    poetry install --only-root

# Run the scanner
run:
    poetry run python -m scanner

# Run the scanner with defaults
run-with-defaults:
    DEBUG=true GITHUB_REPOSITORY_OWNER=JackPlowman just run

# Runs unit tests
unit-test:
    poetry run pytest scanner --cov=. --cov-report=xml

# Runs unit tests with debug
unit-test-debug:
    poetry run pytest scanner --cov=. --cov-report=xml -vv

# ------------------------------------------------------------------------------
# Cleaning Commands
# ------------------------------------------------------------------------------

# Remove all generated files
clean:
    find . \( \
      -name '__pycache__' -o \
      -name '.coverage' -o \
      -name '.mypy_cache' -o \
      -name '.pytest_cache' -o \
      -name '.ruff_cache' -o \
      -name '*.pyc' -o \
      -name '*.pyd' -o \
      -name '*.pyo' -o \
      -name 'coverage.xml' -o \
      -name 'db.sqlite3' \
    \) -print | xargs rm -rfv

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formating
# Set up ruff red-knot when it's ready
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just ruff-format-fix
    just ruff-lint-fix

# Check for Ruff issues
ruff-lint:
    poetry run ruff check .

# Fix Ruff lint issues
ruff-lint-fix:
    poetry run ruff check . --fix

# Check for Ruff format issues
ruff-format:
    poetry run ruff format --check .

# Fix Ruff format issues
ruff-format-fix:
    poetry run ruff format .

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

# Check for unused code
vulture:
    poetry run vulture .

# ------------------------------------------------------------------------------
# Prettier - File Formatting
# ------------------------------------------------------------------------------

# Check for prettier issues
prettier-check:
    prettier . --check

# Fix prettier issues
prettier-format:
    prettier . --check --write

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

# Format the Just code
just-format:
    just --fmt --unstable

# Check for Just format issues
just-format-check:
    just --fmt --check --unstable

# ------------------------------------------------------------------------------
# Git Hooks
# ------------------------------------------------------------------------------

# Install pre commit hook to run on all commits
install-git-hooks:
    cp -f githooks/pre-commit .git/hooks/pre-commit
    cp -f githooks/post-commit .git/hooks/post-commit
    chmod ug+x .git/hooks/*
