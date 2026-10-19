import pytest

@pytest.mark.mobile
def test_driver_session(driver):
    assert driver is not None