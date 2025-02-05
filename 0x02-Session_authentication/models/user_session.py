#!/usr/bin/env python3
""" User Sessions module
"""
from models.base import Base


class UserSession(Base):
    """User Session class"""

    def __init__(self, *args: list, **kwargs: dict):
        """Initializing a session class"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
