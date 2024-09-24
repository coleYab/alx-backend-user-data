#!/usr/bin/env python3
"""
a simple implementation of auth
"""
from bcrypt import hashpw, gensalt


def _hash_password(password: str) -> str:
    """
    _hash_password: hashes password with bcrypt
    """
    passwd = password.encode('utf-8')
    return hashpw(passwd, gensalt())
