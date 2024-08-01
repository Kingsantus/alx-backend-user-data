#!/usr/bin/env python3
"""
Filtered logger of main.py
"""
import re
import os
import logging
import mysql.connector
from typing import List

# defining the fields of essentiall pII in user_data.csv
PII_FIELDS = ("name", "email", "phone", "ssn", "password")

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """Filter datum function
    Keyword arguments:
    fields -- a list of strings representing all fields to obfuscate
    redaction -- a string representing by what the field will be obfuscated
    messages -- a string representing the log line
    seperator -- a string representing by which character is separating all fields in the log line (message)
    Return:  the log message obfuscated
    """
    return re.sub(rf'({"|".join(fields)})=.*?{separator}', lambda msg: f'{msg.group(1)}={redaction}{separator}', message)

class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> str:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        record.msg = filter_datum(self.fields, self.REDACTION, record.getMessage(), self.SEPARATOR)

        return super(RedactingFormatter, self).format(record)

def get_logger() -> logging.Logger:
    """
    returns a logging.Logger object
    """
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()    
    formatter = RedactingFormatter(PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """Return a MySQL database connection object."""
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.environ.get("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connection.MySQLConnection(user=username, password=password, host=host, database=db_name)

def main():
    """
    Function obtain a database connection using get_db and retrieve all rows in the users table
    Return: display each row under a filtered format 
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    field_names = [i[0] for i in cursor.description]

    logger = get_logger()
    for row in cursor:
        str_row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, field_names))
        logger.info(str_row.strip())

    cursor.close()
    db.close()
