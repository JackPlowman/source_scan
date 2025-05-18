# ------------------------------------------------------------------------------
# Common Commands
# ------------------------------------------------------------------------------

# Install python dependencies
install:
    uv sync

# Install python dependencies with dev dependencies
install-all:
    uv sync --all-extras

# Run the scanner
run:
    uv run python -m scanner

# Run the scanner with defaults
run-with-defaults:
    DEBUG=true GITHUB_REPOSITORY_OWNER=JackPlowman just run

# Check UV lock
uv-lock-check:
    uv lock --check

# ------------------------------------------------------------------------------
# Test Commands
# ------------------------------------------------------------------------------

# Runs unit tests
unit-test:
    uv run pytest scanner --cov=. --cov-report=xml

# Runs unit tests with debug
unit-test-debug:
    uv run pytest scanner --cov=. --cov-report=xml -vv

# Run markdown tests
markdown-test:
    uv run pytest tests/markdown

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
# Create Diagrams
# ------------------------------------------------------------------------------

# Create the C4 diagram
create-c4-diagram:
    uv run python diagrams/c4.py

# ------------------------------------------------------------------------------
# Ruff - Python Linting and Formatting
# Set up ty when it's ready
# ------------------------------------------------------------------------------

# Fix all Ruff issues
ruff-fix:
    just ruff-format-fix
    just ruff-lint-fix

# Run all ruff checks
ruff-checks:
    just ruff-lint ruff-format

# Check for Ruff issues
ruff-lint:
    uv run ruff check .

# Fix Ruff lint issues
ruff-lint-fix:
    uv run ruff check . --fix

# Check for Ruff format issues
ruff-format:
    uv run ruff format --check .

# Fix Ruff format issues
ruff-format-fix:
    uv run ruff format .

# ------------------------------------------------------------------------------
# Other Python Tools
# ------------------------------------------------------------------------------

# Check for unused code
vulture:
    uv run vulture scanner

# ------------------------------------------------------------------------------
# Prettier
# ------------------------------------------------------------------------------

# Check all files with prettier
prettier-check:
    prettier . --check

# Format all files with prettier
prettier-format:
    prettier . --check --write

# ------------------------------------------------------------------------------
# Justfile
# ------------------------------------------------------------------------------

# Format Justfile
format:
    just --fmt --unstable

# Check Justfile formatting
format-check:
    just --fmt --check --unstable

# ------------------------------------------------------------------------------
# Gitleaks
# ------------------------------------------------------------------------------

# Run gitleaks detection
gitleaks-detect:
    gitleaks detect --source .

# ------------------------------------------------------------------------------
# Lefthook
# ------------------------------------------------------------------------------

# Validate lefthook config
lefthook-validate:
    lefthook validate

# ------------------------------------------------------------------------------
# Zizmor
# ------------------------------------------------------------------------------

# Run zizmor checking
zizmor-check:
    uvx zizmor . --persona=pedantic

# Run zizmor checking with sarif output
zizmor-check-sarif:
    uvx zizmor . --persona=pedantic --format sarif > results.sarif

# ------------------------------------------------------------------------------
# Pinact
# ------------------------------------------------------------------------------

# Run pinact
pinact-run:
    pinact run

# Run pinact checking
pinact-check:
    pinact run --verify --check

# Run pinact update
pinact-update:
    pinact run --update

# ------------------------------------------------------------------------------
# Git Hooks
# ------------------------------------------------------------------------------

# Install pre commit hook to run on all commits
install-git-hooks:
    lefthook install -f
