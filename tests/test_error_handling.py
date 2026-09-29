import pytest

from core.exceptions import ElementInteractionError


def test_missing_element_generates_framework_error(settings_page):
    invalid_locator = (
        "id",
        "com.android.settings:id/does_not_exist",
    )

    with pytest.raises(ElementInteractionError):
        settings_page.find_element(invalid_locator)