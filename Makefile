SRC = $(wildcard ./*.ipynb)

all: cheviz docs

cheviz: $(SRC)
	nbdev_build_lib
	touch cheviz

docs_serve: docs
	cd docs && bundle exec jekyll serve

docs: $(SRC)
	nbdev_build_docs
	touch docs

test:
	nbdev_test_nbs

release: pypi
	nbdev_bump_version

pypi: dist
	twine upload --repository pypi dist/*

dist: clean
	python setup.py sdist bdist_wheel

dist-upgrade:
	conda env update --file environment.yml  --prune --quiet
	conda env export --no-builds | grep -v 'prefix:' > environment.yml
	pip list --format=freeze > requirements.txt

clean:
	rm -rf dist
