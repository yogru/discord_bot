from passlib.context import CryptContext


class BCrypt:
    def __init__(self):
        self.ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, plain_password: str) -> str:
        return self.ctx.hash(plain_password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return self.ctx.verify(plain_password, hashed_password)