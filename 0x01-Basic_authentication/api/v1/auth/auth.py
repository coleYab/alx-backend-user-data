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
        if path is not None:
            if excluded_paths is not None and len(excluded_paths) >= 0:
                new_path = path + '/'
                res = path in excluded_paths or new_path in excluded_paths
                return not res

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header: retrives auth header from request.
        args:
            - request: the main falsk.request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user: retrives the current user.
        args:
            - request: the main request object
        """
        return None
