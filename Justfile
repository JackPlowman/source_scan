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

# Mutation tests
mutmut-run:
    uv run mutmut run

# Run markdown tests
markdown-test:
    uv run pytest tests/markdown

export DEFAULT_PROJECT_URL := "https://jackplowman.github.io/source_scan"

# Run UI tests
ui-tests $PROJECT_URL=DEFAULT_PROJECT_URL $browser="chromium":
    uv run pytest tests/ui -vv --reruns 2 --browser ${browser}

# Run UI Tests in a specific browser
ui-tests-ci $browser:
    just ui-tests $DEFAULT_PROJECT_URL ${browser}

# Install playwright dependencies
playwright-install:
    uv run playwright install --with-deps

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
