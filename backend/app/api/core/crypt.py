from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str):
    return bcrypt_context.hash(password)


async def verify_password(password: str, hashed_password: str):
    return bcrypt_context.verify(password, hashed_password)
