from pytest_create.definitions.class_def import ClassDef


def test_class_def_init():
    class_def = ClassDef(name="TestClass", docstring="A simple test class.")
    assert class_def.name == "TestClass"
    assert class_def.docstring.value == "A simple test class."
    assert class_def.bases == []
    assert class_def.decorators == []
    assert class_def.definitions == []


def test_class_def_init_with_bases():
    class_def = ClassDef(name="TestClass", bases=["BaseClass1", "BaseClass2"])
    assert class_def.name == "TestClass"
    assert class_def.bases == ["BaseClass1", "BaseClass2"]


def test_class_def_init_with_decorators():
    class_def = ClassDef(name="TestClass", decorators=["@decorator1", "@decorator2"])
    assert class_def.name == "TestClass"
    assert class_def.decorators == ["@decorator1", "@decorator2"]


def test_class_def_str():
    class_def = ClassDef(name="TestClass", docstring="A simple test class.")
    assert isinstance(str(class_def), str)
