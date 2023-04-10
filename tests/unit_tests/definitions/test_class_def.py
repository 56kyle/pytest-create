from pytest_create.definitions.class_def import ClassDef


def test_class_def_init(class_def: ClassDef) -> None:
    assert class_def


def test_class_def_str(class_def: ClassDef) -> None:
    assert isinstance(str(class_def), str)
