from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(id=1, name="Nigguel", surname="Fernández", url="https://nigguel.com", age=26),
    User(id=2, name="Genesis", surname="Castañeda", url="https://genesis.com", age=20),
    User(id=3, name="Jasmin", surname="Salcedo", url="https://jasmin.com", age=49),
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


@app.get("/users/")
async def users():
    return users_list


# path
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)


# Query
@app.get("/user/")
async def user(id: int):
    return search_user(id)


# operacion capaz de Insertar valores
@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)
        return user


# Operacion capaz de actualizar valores
@app.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return {"error": "No se ha encontrado el usuario"}
    else:
        return user


# Operacion capaz dde borrar valores
@app.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True

    if not found:
        return {"error": "No se ha borrado el usuario"}
    else:
        return {"exito": "usuario borrado exitosamente"}


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
