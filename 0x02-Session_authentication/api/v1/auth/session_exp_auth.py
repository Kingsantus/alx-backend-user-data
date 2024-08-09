#!/usr/bin/env python3
"""Handles the expiration date of Session ID"""
from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """class handles seting and expiration of session time"""

    def __init__(self):
        """Initialize the session"""
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create session id using super() fro SessionAuth"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        session_dictionary = {
            'user_id': user_id,
            'created_at': datetime.now()
        }

        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Get session ID of user and when it was created"""

        if not session_id:
            return None

        session_key = self.user_id_by_session_id[session_id]
        if not session_key:
            return None

        if self.session_duration <= 0:
            return session_key.get('user_id')

        created_at = session_key.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)

        if datetime.now() > expiration_time:
            return None

        return session_key.get("user_id")
