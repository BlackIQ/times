# Password Lib
from pwdlib import PasswordHash

# Hash instance
password_hash = PasswordHash.recommended()


# Hash password
def hash_password(password: str) -> str:
    return password_hash.hash(password)


# Verify password
def verify_password(password: str, hashed: str) -> bool:
    return password_hash.verify(password, hashed)
