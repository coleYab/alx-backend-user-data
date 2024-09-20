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
