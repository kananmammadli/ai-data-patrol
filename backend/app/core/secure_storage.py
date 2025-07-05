import os
from cryptography.fernet import Fernet, InvalidToken

# The encryption key should be set as an environment variable
FERNET_KEY = os.environ.get("DATA_PATROL_FERNET_KEY")
if not FERNET_KEY:
    raise RuntimeError("DATA_PATROL_FERNET_KEY environment variable not set!")
fernet = Fernet(FERNET_KEY)

def encrypt_secret(secret: str) -> str:
    return fernet.encrypt(secret.encode()).decode()

def decrypt_secret(token: str) -> str:
    try:
        return fernet.decrypt(token.encode()).decode()
    except InvalidToken:
        raise ValueError("Invalid encryption token or key.")
