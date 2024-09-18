#!/usr/bin/env python3
""" Simple Auth class to imulate authorization
"""
from flask import request
from typing import (
    List,
    TypeVar
)


class Auth:
    """
    Auth:
        - a simple class for authorization
    Methods:
        - require_auth: checks if a path requires auth
        - authorization_header: returns auth header from request
        - current_user: retrives the current authorized user
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth: methods to return path requires auth
        args:
            - path: the path to check
            - excluded_paths: the path that don't need auth
        returns:
            True, False
        """
        if None in [path, excluded_paths] or len(excluded_paths) == 0:
            return False
        for excl_path in excluded_paths:
            if excl_path[-1] == '*' and path.startswith(excl_path[:-1]):
                return False
            if path.startswith(excl_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header: retrives auth header from request.
        args:
            - request: the main falsk.request object
        """
        if request is not None:
            header = request.headers
            if 'Authorization' in header.keys():
                return header['Authorization']

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user: retrives the current user.
        args:
            - request: the main request object
        """
        return None
