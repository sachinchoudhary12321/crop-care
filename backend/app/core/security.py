"""Security helpers.

Authentication / authorization (JWT, API keys, roles) is a later task. These
functions are the always-useful foundation: generate secrets and store only
their hash, compared in constant time.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets


def generate_secret(nbytes: int = 32) -> str:
    """Generate a URL-safe random secret (e.g. for API keys)."""
    return secrets.token_urlsafe(nbytes)


def hash_secret(secret: str) -> str:
    """Return the hex SHA-256 hash of a secret. Store this, never the raw value."""
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()


def verify_secret(secret: str, expected_hash: str) -> bool:
    """Constant-time comparison of a raw secret against its stored hash."""
    return hmac.compare_digest(hash_secret(secret), expected_hash)