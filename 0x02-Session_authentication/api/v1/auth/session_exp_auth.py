#!/usr/bin/env python3
"""
Expiration based session authorization
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime


class SessionExpAuth(SessionAuth):
    """
    Expiration based session authorization
    """
    def __init__(self):
        super().__init__()
        try:
            val = int(getenv("SESSION_DURATION"))
            self.session_duration = val
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create_session: creating a session with duration
        args:
            - user_id: user id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dic = {'user_id': user_id, 'created_at': datetime.now()}
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user_id_for_session_id: retrives the user id for given session id
        """
        if session_id is None:
            return None
        session_dic = SessionExpAuth.user_id_by_session_id[session_id]
        if session_dic is None or 'user_id' not in session_dic:
            return None
        created_at = session_dic['created_at']
        if created_at + timedelta(seconds=self.session_duration) < datetime.now():
            return None
        return session_dic['user_id']
