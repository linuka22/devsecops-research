import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app.auth import hash_password, generate_token, verify_token

def test_password_hashing():
    hashed = hash_password("testpassword")
    assert hashed is not None
    assert len(hashed) == 32

def test_token_generation_and_verification():
    token = generate_token(1, "testuser", "customer")
    assert token is not None
    payload = verify_token(token)
    assert payload["username"] == "testuser"
    assert payload["role"] == "customer"

def test_token_invalid():
    result = verify_token("invalid.token.here")
    assert result is None