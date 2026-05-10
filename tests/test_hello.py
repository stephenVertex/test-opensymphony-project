from src.hello import greet


def test_greet_default():
    assert greet("World") == "Hello, World!"


def test_greet_custom_name():
    assert greet("OpenSymphony") == "Hello, OpenSymphony!"


def test_greet_empty_string():
    assert greet("") == "Hello, !"