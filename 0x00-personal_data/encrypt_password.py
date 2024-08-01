#!/usr/bin/env python3
"""Encryption of password"""
import bcrypt

def hash_password(password: str) -> bytes:
    """hashing password
    
    Keyword arguments:
    password -- password provided by user
    Return: a salted, hashed password, which is a byte string
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password

def is_valid(hashed_password: bytes, password: str) -> bool:
    """is_valid
    
    Keyword arguments:
    hashed_password -- bytes hashed_password retured from hash_password function
    password -- string provided by user
    Return: returns a boolean if validate that hashed_password and string is equal
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
