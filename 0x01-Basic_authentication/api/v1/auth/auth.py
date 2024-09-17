#!/usr/bin/env python3
""" Simple Auth class to imulate authorization
"""

from typing import *
from flask import request

class Auth:
    """ Auth clas that ecapsulates authing
    """
    def __init__(self):
        """ constructor type shit
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ requireing authing
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ authorizating the main header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ getting current user
        """
        return None

