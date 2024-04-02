all:
	poetry run isort domain_account/ tests/
	poetry run black domain_account/ tests/
	poetry run flake8 domain_account/ tests/
	poetry run mypy domain_account/ tests/ --install-types --non-interactive --show-error-codes
	poetry run pylint domain_account/ tests/
	poetry run wily build domain_account/
	poetry run wily diff -a --no-detail domain_account/

style:
	isort domain_account/
	black --line-length 120 domain_account/

run:
	uvicorn domain_account.main:app --host 0.0.0.0 --reload
