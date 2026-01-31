"""
Password hashing using bcrypt directly (no passlib) so we avoid the 72-byte
limit issue in passlib's internal backend detection. We pre-hash with SHA-256
so arbitrarily long strong passwords are supported.
"""
import hashlib
from typing import Union

import bcrypt

# bcrypt only accepts up to 72 bytes. Pre-hash with SHA-256 so we support
# arbitrarily long passwords: we store bcrypt(sha256(password)).
# SHA-256 hex digest is 64 bytes, so always under bcrypt's limit.
_PREHASH_ENCODING = "utf-8"
_BCRYPT_MAX_BYTES = 72


def _prehash_for_bcrypt(password: str) -> bytes:
    """Return SHA-256 digest as bytes (64 bytes) so bcrypt never sees > 72 bytes."""
    digest = hashlib.sha256(password.encode(_PREHASH_ENCODING)).hexdigest()
    return digest.encode("ascii")


def hash_password(password: str) -> str:
    digest = _prehash_for_bcrypt(password)
    hashed = bcrypt.hashpw(digest, bcrypt.gensalt())
    return hashed.decode("ascii")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    if not hashed_password:
        return False
    digest = _prehash_for_bcrypt(plain_password)
    hashed_bytes = hashed_password.encode("ascii")
    if bcrypt.checkpw(digest, hashed_bytes):
        return True
    # Backwards compatibility: hashes created before SHA-256 pre-hash (plain bcrypt)
    try:
        plain_bytes = plain_password.encode(_PREHASH_ENCODING)
        if len(plain_bytes) <= _BCRYPT_MAX_BYTES:
            return bcrypt.checkpw(plain_bytes, hashed_bytes)
    except (ValueError, TypeError):
        pass
    return False
