#!/usr/bin/env python3
"""Session authenticator for USER
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """Class handles all session authenticator
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""

        if not user_id:
            return None

        if type(user_id) is not str:
            return None

        session_id = str(uuid4())
        # storing the generated id as key
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Returns user ID based on Session ID"""

        if not session_id:
            return None

        if type(session_id) is not str:
            return None

        userID = self.user_id_by_session_id.get(session_id)

        return userID

    def current_user(self, request=None):
        """Returns a User instance based on a cookie value"""

        session_id = self.session_cookie(request)
        user_id = self.user_id_by_session_id(session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """Deletes the user session after logout"""

        if request is not None:
            return False

        session_id = self.session_cookie(request)

        if not session_id:
            return False

        user_id = self.session_cookie(request)
        if not user_id:
            return False

        del self.user_id_by_session_id[session_id]

        return True
