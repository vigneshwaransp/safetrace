import base64
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any, Optional, Dict
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, InvalidHashError
from cryptography.fernet import Fernet
from app.core.config import settings

# Initialize Argon2 Password Hasher
pwd_hasher = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16
)


def get_password_hash(password: str) -> str:
    """Hash password using Argon2id."""
    return pwd_hasher.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against Argon2 hash."""
    try:
        return pwd_hasher.verify(hashed_password, plain_password)
    except (VerifyMismatchError, InvalidHashError):
        return False


def create_access_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    """Generate signed JWT access token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,
        "type": "access",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(subject: str | Any, expires_delta: Optional[timedelta] = None) -> str:
    """Generate signed JWT refresh token."""
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        
    to_encode: Dict[str, Any] = {
        "sub": str(subject),
        "exp": expire,
        "iat": now,
        "type": "refresh",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.PyJWTError as e:
        raise ValueError(f"Invalid or expired token: {str(e)}")


def _get_fernet_cipher() -> Fernet:
    """Derive a valid 32-byte url-safe base64 key for Fernet AES encryption."""
    raw_key = settings.ENCRYPTION_KEY.encode()
    # Ensure key is exact 32 bytes base64 url-safe
    derived_32 = hashlib.sha256(raw_key).digest()
    b64_key = base64.urlsafe_b64encode(derived_32)
    return Fernet(b64_key)


def encrypt_bytes(data: bytes) -> bytes:
    """Encrypt raw bytes using authenticated AES-256 (Fernet)."""
    cipher = _get_fernet_cipher()
    return cipher.encrypt(data)


def decrypt_bytes(encrypted_data: bytes) -> bytes:
    """Decrypt authenticated AES-256 (Fernet) ciphertext."""
    cipher = _get_fernet_cipher()
    return cipher.decrypt(encrypted_data)
