# Tooling

This repository secondary goal is to show tooling for Python repositories in action
Tooling is runnable within several auxiliary tools: make, doit, shell, pre-commit.

Some of the tools can be used in your IDE to run against a given file of module.

In general, is recommended to run this tools often, for the code to be clean and readable as
you develop, and run then in the terminal, specially the slow ones.


## Style and linting

### black

Shape code into a common and consistent style

```shell
black -l 100
make black
pre-commit black --all
````

### isort

Order and group the import in classic style


## flake8

**Recommendation**: use flake in the IDE terminal, it will allow you to jump directly to the
flagged code.

### pylint

Caveat: very slow even in small codebase, specially checking for duplicate code
Alternatives: ruff

### vulture

Looks for dead code


## Docstrings

My personal preference is Google's docstring style, usually skipping parameters because
naming and typing do most of the work for them.

### interrogate

### docstr-coverage


## TODO

- mcabe
- loc
- pandas
- ruff
- liccheck
- bandit
- other sec tools (Docker and non-docker)
