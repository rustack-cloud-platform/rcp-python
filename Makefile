apps = esu

fixtures:
	@cp ../toochka-new/src/api/core/tests/pylib_fixtures.json esu/tests/fixtures.json

tests:
	pytest -v $(apps)

tdd: clean fixtures
	@ptw -p -v

style:
	isort $(apps)
	yapf -ir $(apps)
	pylint $(apps)

