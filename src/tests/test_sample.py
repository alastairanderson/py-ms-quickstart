# https://docs.pytest.org/en/latest/
# https://docs.pytest.org/en/latest/example/index.html
# https://www.backendguy.com/testing-flask-applications-using-pytest/


def inc(x):
    return x + 1

def test_answer():
    assert inc(3) == 5

# To execute this:
#     $ pytest
