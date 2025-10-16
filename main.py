from fastapi import FastAPI
from strawberry.asgi import GraphQL

from schema import schema

app = FastAPI()


@app.get("/")
def index():
    return {"message": "Welcome to the Task API"}


app.add_route("/graphql", GraphQL(schema))
