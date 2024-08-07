#!/usr/bin/env python3
""" Authorization and Authentication of API
"""
from typing import List, TypeVar
import re

class Auth:
    """Class for handling authentication."""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check the path and excluded_paths
        Returns:
            - False if path and excluded_path is same
        """

        if not path or not excluded_paths:
            return True
        
        if path[-1] != '/':
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False
            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the authorization header, or None if not found."""
        if not request:
            return None
        auth_header = request.headers.get('Authorization', None)
        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """TODO: implement"""
        return None   
