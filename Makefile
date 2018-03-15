lint:
	flake8 place tests

test:
	py.test tests --cov=place --cov-report term-missing --cov-fail-under=100 --cov-branch
