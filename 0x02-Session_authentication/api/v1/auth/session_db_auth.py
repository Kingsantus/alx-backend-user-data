#!/usr/bin/env python3
"""Session DataBase Auth Module"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Class Session DB Auth"""

    def create_session(self, user_id=None):
        """Create and stores new instance of usersessions"""
        session_id = super().create_session(user_id)

        if not session_id:
            return None

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user Id from usersession"""

        if session_id is None:
            return None

        user_session = UserSession.search({"session_id": session_id})

        if not user_session:
            return None

        if self.session_duration <= 0:
            return user_session.user_id

        created_at = user_session.created_at
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        """Destroys the user sessions"""

        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_session = UserSession.search({"session_id": session_id})
        if not user_session:
            return False

        user_session.remove()

        return True
