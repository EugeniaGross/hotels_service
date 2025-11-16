from src.services.auth import AuthService


def test_create_and_decode_access_token():
    data = {"user_id": 1}
    token = AuthService().create_access_token(data)
    assert token
    assert isinstance(token, str)
    decode_data = AuthService().decode_token(token)
    assert decode_data
    assert decode_data.get("user_id") == data["user_id"]
    assert "exp" in decode_data
    