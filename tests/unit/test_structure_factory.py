import pytest

from ..factories.structure_factory import Structure, StructureDictFactory, StructureFactory


def test_structure_factory():
    value = StructureFactory()
    assert isinstance(value, Structure)
    assert isinstance(value.nested.inner, float)


def test_structure_dict():
    value = StructureDictFactory()
    assert isinstance(value, dict)
    assert isinstance(value["nested"]["inner"], float)
