from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Entidad user
class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(name="Nigguel", surname="Fernández", url="https://nigguel.com", age=26),
    User(name="Genesis", surname="Castañeda", url="https://genesis.com", age=20),
    User(name="Jasmin", surname="Salcedo", url="https://jasmin.com", age=49),
]


# Ejemplo, no es habitual
@app.get("/usersjson")
async def usersjason():
    return [
        {
            "name": "Nigguel",
            "surname": "Fernández",
            "url": "https://nigguel.com",
            "age": 26,
        },
        {
            "name": "Nixon",
            "surname": "Fernández",
            "url": "https://nixon.com",
            "age": 22,
        },
        {
            "name": "Jasmin",
            "surname": "Salcedo",
            "url": "https://Jasmin.com",
            "age": 49,
        },
    ]


@app.get("/users")
async def users():
    return users_list
