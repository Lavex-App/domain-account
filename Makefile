style:
	isort domain_account/
	black --line-length 120 domain_account/

run:
	uvicorn domain_account.main:app --host 0.0.0.0 --reload
