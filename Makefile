#!/usr/bin/make -f
PKGS="examples"


#### Slides

help:  ## Prompts help for every command, try `make`
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = "[:,##]"}; {printf "\033[36m%-30s\033[0m %s\n", $$2, $$2}'

one: ## Generate slide for one only TODO sponge addendum
	@cp masters/fixtures_factories.md temp/slides.md
	@cat masters/0_main_template.md  temp/slides.md | sponge temp/slides.md
	@mdslides temp/slides.md
	@mkdir -p slides/assets/title
	@rm -f slides/assets/title/*
	@rm -f slides/assets/*.*
	@cp -r assets/* slides/assets/.
	@chromium slides/index.html &

#### Testing

tests:  ## Run tests, dashed options will be included ( make test -s)
	pytest $(MFLAGS)

current-tests:  ## Run tests decorated with @pytest.mark.current, with prompt output and verbosity, dashed options will be included
	pytest -s -m current -v $(MFLAGS)

clean-python:  ## Remove python compiled and temporal files
	@find . -name '*.pyc' -exec rm -f {} +
	@find . -name '*.pyo' -exec rm -f {} +
	@find . -name '*~' -exec rm -f {} +
	@find . -name '__pycache__' -exec rm -fr {} +
	@find . -name '.pytest_cache' -exec rm -fr {} +
	@find . -name '*.egg-info' -exec rm -fr {} +
	@rm -rf build/

##### Style, docstrings and linting

isort:  ## Run import sorting
	@isort "${PKGS}" --settings-file=setup.cfg

black:  ## Run black style
	@black -l 100 -C "${PKGS}"

flake: ## Runs flake8 style check
	@flake8 "${PKGS}" \
	&& echo "${GREEN}Passed Flake8 style review for: ${PKGS}.${REGULAR}" \
	|| (echo "${RED}Flake8 style review failed for ${PKGS}.${REGULAR}" ; exit 1)

lint:  ## Run pylint
	@pylint --rcfile setup.cfg ${PKGS} | tee .coverage-reports/pylint.txt

linting-full:  ## Run pylint without any configuration
	@pylint -v ${PKGS} tests

format: isort black flake linting

interrogate:  # Run interrogate docstrings with extra parsing
	@interrogate --config=setup.cfg | sed -e "s/^| //" -e "s#[^\s]*\.py#&:1#"

docstrings:  ## Review docstrings, use doit interrogate better
	@pydocstyle "${PKGS}" && echo "${GREEN}pydocstyle OK ${REGULAR}" || echo "";
	@docstr-coverage "${PKGS}" -v 1; echo ""

check-pipfile:  ## List available python package updates, may request creating a password wallet
	@pipenv update --dev --outdated


requirements:  ## Generate dev requirements from Pipfile
	@pipfile2req --dev Pipfile.lock |  sed 's/;.*//' > requirements.txt


.PHONY: tests current-tests clean-python black format lint lint-full isort requirements
