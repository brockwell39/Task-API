# LUSH Backend Developer Task
Small API project to demonstrate Strawberry queries and mutations\
Built using FastAPI, Python, Strawberry GraphQL, SQLAlchemy on a SQLite database

Built by Alex Catlow


### Requirements

Python 3.10+

Pip

### Instructions for  Windows


To set up the project you will need to create a virtual environment

Open a command temrinal

First make a directory (task-api) and navigate into it using this command

>mkdir task-api && cd task-api

Create a virtual environment using this command

>python -m venv env

Activate the virtual environment using this command

>env\Scripts\activate

Run this command to install the dependencies

>pip install fastapi sqlalchemy strawberry-graphql uvicorn[standard]

Download these files into the directory task-api\
main.py\
database.py\
models.py\
schema.py

run this command to start the API

>uvicorn main:app --reload

The API will be available here 

Local host http://localhost:8000/graphql


### Bonus points
Created a mutation to make a task urgent by adding text to the beginning, but only once\
Created a query 'To do list' to get all the non completed tasks ordered by created_at
