# Test factories

This repository's purpose is to show examples on how to define and use test factories
using the library `factory-boy`.

Factory is a generic object-oriented software pattern that uses a class or a function to build
objects of a certain kind, but not using the constructor.

In particular, this repository uses the more specific pattern Object Mother, but for consistency
with the library and havit, it uses Factory as the concept in most examples.

For more info on Object Mother pattern, you can start with Martin's Fowler article:

https://martinfowler.com/bliki/ObjectMother.html

To show the use of `factoryboy` we will use pytest and sqlalchemy, to exemplify advanced usages
closest to the real world. This example can be easily translated to other framework and tools,
namely Django and its ORM, Mongo.

For more modern libraries, while factoryboy is still a good option, newer libraries have popped out
like [polyfactory](https://polyfactory.litestar.dev/latest/). The examples shown in this repository
should be applicable with some effort into `polyfactory` or any other library in Python or in
any other languages

## Other interesting things about this repo

This repo uses pre-commit and several tools to keep the repo style consistent and in shape.
You can take a look and reuse them.

- doit: [dodo.py](dodo.py)
- make: [Makefile](Makefile)
- pre-commit: [.pre-commit-config.yaml](.pre-commit-config.yaml)
  - uses black, isort, pylint, interrogate

Configuration is either in [setup.cfg](setup.cfg) or [pyproject.toml]

## How to install

```shell
sudo apt install libpq-dev python3-dev
pipenv install --dev
````

For other dependency systems use [requirements.txt](requirements.txt)



## How to launch tests

```shell
pipenv shell
docker compose up -dev
pytest
```

## Acknowledgments

I want to thank my colleagues and former colleagues at CitNOW which have contributed to set up
and evolve our testing and tooling skills, these examples are partially based on our work.
