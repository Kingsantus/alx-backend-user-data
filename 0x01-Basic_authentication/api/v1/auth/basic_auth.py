#!/usr/bin/env python3
""" Basic Auth for Base64
"""
from ..views.users import User
from .auth import Auth
import base64
from typing import TypeVar

class BasicAuth(Auth):
    """ BasicAuth inherites from Auth. Basic authentication handling.
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ authorization_header in base64
        Return:
            -   other str excepts "Basic " or None
        """
        if not authorization_header:
            return None
        
        if type(authorization_header) is not str:
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header.split('Basic ', maxsplit=1)[1]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ Base for autherization header
        Return:
            -   decode value
        """
        if not base64_authorization_header:
            return None
        
        if type(base64_authorization_header) is not str:
            return None
        
        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            
            str_decoded = decoded_bytes.decode('utf-8')

            return str_decoded
        except Exception:
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ decode authorization header
        Returns:
            - tuple str of email:password
        """
        if not decoded_base64_authorization_header:
            return (None, None)
        
        if type(decoded_base64_authorization_header) is not str:
            return (None, None)
        
        if ':' not in decoded_base64_authorization_header:
            return (None, None)
        
        email, password = decoded_base64_authorization_header.split(':', 1)

        return email, password
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ Validate user_email and user_password
        Return:
            -  User object or None user email don't match password
        """
        if user_email is None or type(user_email)is not str:
            return None
        
        if user_pwd is None or type(user_pwd) is not str:
            return None
        
        try:
            users = User.search({'email': user_email})
            if not users or users == []:
                return None
            
            for user in users:
                if not user.is_valid_password(user_pwd):
                    return user
            
            return None
        except Exception:
            return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Current_user
        Returns:
            -   User instance for a request
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return
        

        
        
