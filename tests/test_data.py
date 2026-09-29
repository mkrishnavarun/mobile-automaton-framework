def test_login_data(login_data):
    assert login_data["valid_user"]["username"] == "test_user"
    assert login_data["invalid_user"]["username"] == "invalid_user"