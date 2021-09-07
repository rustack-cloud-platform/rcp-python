apps = esu

fixtures:
	@cp ../toochka-new/src/api/core/tests/pylib_fixtures.json esu/tests/fixtures.json

tdd: clean fixtures
	@ptw -p -v

style:
	isort $(apps)
	yapf -ir $(apps)
	pylint $(apps)

clean:
	@rm -f .coverage
	@rm -rf build rustack_esu.egg-info dist
	@rm -rf docs/static
	@find . | grep -E "\(__pycache__|\.pyc|\.pyo$\)" | xargs rm -rf

sphinx:
	@sphinx-build -b html -E docs docs/static/docs
	@open docs/static/docs/index.html

upload:
	@pip install setuptools wheel twine
	@python setup.py sdist bdist_wheel
	@twine upload dist/*
