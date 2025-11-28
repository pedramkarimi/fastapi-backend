# src/core/security.py  (اگر نداری، بعداً حرفه‌ای‌ترش می‌کنیم)
from passlib.context import CryptContext

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Security:

    def hash_password(password: str) -> str:
        return _pwd_context.hash(password)


    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return _pwd_context.verify(plain_password, hashed_password)
