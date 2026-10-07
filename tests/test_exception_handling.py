import pytest

from core.exceptions import ElementInteractionError
from pages.base_page import BasePage


def test_element_interaction_error():
    error = ElementInteractionError(
        "Unable to tap element: ('id', 'invalid')"
    )

    with pytest.raises(ElementInteractionError):
        raise error