from typing import List
from uuid import UUID
from fastapi import UploadFile
from passlib.context import CryptContext
from rsa import PrivateKey, PublicKey
from rsa import decrypt as dec
from rsa import encrypt as enc

from .environment import config

pwd_context = CryptContext(schemes=["sha256_crypt"])

PUBLIC_KEY_AUX = config.get(
    "database.encryption.public",
    "",
).split(",")
PRIVATE_KEY_AUX = config.get(
    "database.encryption.private",
    "",
).split(",")


public_key = PublicKey(int(PUBLIC_KEY_AUX[0]), int(PUBLIC_KEY_AUX[1]))
private_key = PrivateKey(
    int(PRIVATE_KEY_AUX[0]),
    int(PRIVATE_KEY_AUX[1]),
    int(
        PRIVATE_KEY_AUX[2],
    ),
    int(PRIVATE_KEY_AUX[3]),
    int(PRIVATE_KEY_AUX[4]),
)


def encrypt(message: str) -> str:
    return enc(message.encode("utf8"), public_key)


def decrypt(cripto: str) -> str:
    return dec(cripto, private_key).decode("utf8")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def validate_uuid4(uuid_string):
    try:
        val = UUID(str(uuid_string), version=4)
        return True
    except ValueError:
        return False
