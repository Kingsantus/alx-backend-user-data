#!/usr/bin/env python3
""" Authorization and Authentication of API
"""
from flask import request
from typing import List, TypeVar
import base64

class Auth:

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check the path and excluded_paths
        Returns:
            - False if path and excluded_path is same
        """
        if not path:
            return True
        
        if not excluded_paths or len(excluded_paths) == 0:
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
        """ None Request
        Returns:
            -   Object containing auth_headers or None
        """
        if request is None:
            return None
        
        auth_header = request.headers.get('Authorization', None)
        
        return auth_header
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ TODO: implement
        """
        return None