from pages.base_page import BasePage


class SettingsPage(BasePage):
    SETTINGS_TITLE = (
        "id",
        "com.android.settings:id/homepage_title"
    )

    NETWORK_OPTION = (
        "xpath",
        '//android.widget.TextView[@text="Network & internet"]'
    )

    INTERNET_TITLE = (
        "xpath",
        '//android.widget.TextView[@text="Internet"]'
    )

    def is_settings_displayed(self) -> bool:
        return self.is_displayed(self.SETTINGS_TITLE)

    def open_network(self) -> None:
        self.tap(self.NETWORK_OPTION)

    def is_internet_screen_displayed(self) -> bool:
        return self.is_displayed(self.INTERNET_TITLE)