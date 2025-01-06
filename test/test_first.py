import pytest


@pytest.mark.usefixtures("browser")
class TestA:

    def test_title(self):
        print(self.driver.title)
