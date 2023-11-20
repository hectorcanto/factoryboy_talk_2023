from pprint import pprint

from ..data_factory import DataFactory


def test_data_factory():
    sample = DataFactory()
    pprint(sample, indent=2)


def test_registered(dummy_factory):
    """Factory is usable, but not instantiated as dummy, like ORM fixtures"""
    assert dummy_factory()["example"] == 1
