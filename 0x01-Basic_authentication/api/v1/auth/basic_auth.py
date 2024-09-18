#!/usr/bin/env python3
"""
a basic authing system
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth: basic auth system for class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        extract_base64_authorization_header: extracts the header
        """
        if authorization_header is None:
            return None
        elif not isinstance(authorization_header, str):
            return None
        elif not authorization_header.startswith('Basic '):
            return None

        return authorization_header.lstrip('Basic ')

    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """
        decode_base64_authorization_header: decoding the header
        """
        if base64_authorization_header is None:
            return None
        elif not isinstance(base64_authorization_header, str):
            return None

        try:
            import base64
            by = base64.b64decode(base64_authorization_header, validate=True)
            return by.decode('utf-8')
        except:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """
        extract_user_credentials: this is the main extraction of user data
        """
        if decoded_base64_authorization_header is not None:
            if not isinstance(decoded_base64_authorization_header, str):
                return None, None
            dt = decoded_base64_authorization_header.split(':')
            if len(dt) != 2:
                return None, None
            return tuple(dt)
        return None, None
