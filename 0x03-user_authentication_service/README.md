# User authentication service

## In the industry, you should not implement your own authentication system and use a module or framework that doing it for you (like in Python-Flask: Flask-User). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

## Task

## Project Overview

The project is broken down into 5 major different files.
- auth.py
intermediate between db.py and routes in app.py
- main.py
a test file for the routes specified in app.py
- app.py
it handles the routes of the API for creating user, logout, gettting session id and resetting password
- db.py
contains fuction that interacts with the database.
- user.py
contains the sql code to create a simple user
