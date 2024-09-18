#!/usr/bin/env python3
"""
a basic authing system
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import (
    TypeVar, List
)


class BasicAuth(Auth):
    """
    BasicAuth: basic auth system for class
    """
    def extract_base64_authorization_header(
            self, authorization_header: str
            ) -> str:
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

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
            ) -> str:
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
        except Exception as e:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
            ) -> (str, str):
        """
        extract_user_credentials: this is the main extraction of user data
        """
        if decoded_base64_authorization_header is not None:
            if not isinstance(decoded_base64_authorization_header, str):
                return None, None
            dt = decoded_base64_authorization_header.find(':')
            cred = decoded_base64_authorization_header
            if dt != -1:
                return cred[:dt], cred[dt+1:]
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str
            ) -> TypeVar('User'):
        """
        creating user from user credentials
        """
        for cred in [user_email, user_pwd]:
            if cred is None or not isinstance(cred, str):
                return None
        users = User.search({'email': user_email})
        if users is None or len(users) == 0:
            return None
        for user in users:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current user retrieving from it
        """
        auth_header = self.authorization_header(request)
        auth_data = self.extract_base64_authorization_header(auth_header)
        auth_data = self.decode_base64_authorization_header(auth_data)
        user_email, user_pwd = self.extract_user_credentials(auth_data)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
