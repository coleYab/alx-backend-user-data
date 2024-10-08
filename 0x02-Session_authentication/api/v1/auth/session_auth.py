#!/usr/bin/env python3
"""
Session auth method
"""
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar


class SessionAuth(Auth):
    """
    SessionAuth: class to implement session authorization
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create_session: we are creating session id from user
        """
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        from uuid import uuid4
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrives user id from session_id
        """
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user: retriving current user from the given request
        args:
            - request: the request object
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """
        destroy_session: destroys a given session from a request
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
