apps = rcp

fixtures:
	@cp ../toochka-new/src/api/core/tests/pylib_fixtures.json rcp/tests/fixtures.json

tests:
	pytest -v $(apps)

tdd: clean fixtures
	@ptw -p -v

style:
	isort $(apps)
	yapf -ir $(apps)
	pylint $(apps)

