#!/usr/bin/env python3
"""
Session auth method
"""
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """
    SessionAuth: class to implement session authorization
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        from uuid import uuid4
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id
