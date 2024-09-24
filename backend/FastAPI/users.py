from fastapi import FastAPI, HTTPException
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


@app.post("/user/", response_model=User, status_code=201)
async def create_user(user: User):
    """
    Crea un nuevo usuario y lo agrega a la lista si no existe previamente.

    Args:
        user (User): Objeto con la información del usuario a agregar.

    Returns:
        User: El objeto usuario agregado si la operación es exitosa.

    Raises:
        HTTPException: Si el usuario ya existe en la lista (status code 409)
    """

    # busca si el usuario ya existe en la lista por su ID
    if search_user(user.id) is not None:
        # Si el usuario existe, lanza una excepción con status 409 (conflict)
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    else:
        # Si no existe, lo agrega a la lista de usuarios
        users_list.append(user)
        # Devuelve el objeto agregado
        return user


# Operacion capaz de actualizar valores
@app.put("/user/", response_model=User, status_code=200)
async def update_user(user: User):
    """
    Actualiza la información de un usuario existente en la lista.

    Args:
        user (User): El objeto usuario con la información actualizada.

    Returns:
        User: El objeto usuario actualizado si la operación es exitosa.

    Raises:
        HTTPException: Si no se encuentra el usuario a actualizar (status code 422).
    """
    found = False  # Indicador para saber si encontro el usuario

    # Itera sobre la lista de usuarios para encontrar el usuario a actuallizar
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            # Si encuentra el usuario, lo actualiza en la lista
            users_list[index] = user
            found = True
            break  # Termina el loop si ya encontro y actualizo al usuario

    if not found:
        # Si no se encuentra el usuario, lanza una excepcion HTTP 422 (Unprocessable Entity)
        raise HTTPException(
            status_code=422,
            detail="No se puede procesar: usuario no encontrado para actualizar ",
        )

    # Si el usuario se actualiza correctamente, lo devuelve
    return user


# Operacion capaz dde borrar valores
@app.delete("/user/{id}", status_code=204)
async def delete_user(id: int):
    """
    Elimina un usuario de la lista según su ID.

    Args:
        id (int): El ID del usuario que se desea eliminar.

    Returns:
        dict: Un mensaje de éxito si el usuario es eliminado, o una respuesta sin contenido si el usuario no existía.

    Raises:
        HTTPException: Si el usuario no se encuentra en la lista (status code 404).
    """
    found = False  # Indicador para saber si se encontró el usuario

    # Itera sobre la lista de usuarios para encontrar el usuario a eliminar
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            # Si encuentra el usuario, lo elimina de la lista
            del users_list[index]
            found = True
            break  # Termina el loop si ya encontró y eliminó al usuario

    if not found:
        # Si no se encuentra el usuario, lanza una excepxcion HTTP 404(not found)
        raise HTTPException(
            status_code=404, detail="Usuario no encontrado para eliminar"
        )

    # Si el usuario se elimina correctamente, retorna un mensaje de éxito
    return {"exito": "usuario borrado exitosamente"}


def search_user(id: int):
    """
    Busca un usuario por su ID dentro de la lista de usuarios.

    Args:
        id(int): ID del usuario que se desea buscar.

    Returns:
        User: El objeto usuario si se encuentra en la lista.
        None: Si no se encuentra el usuario con el ID especificado

    """

    # Filtra la lista de usuarios para encontrar aquel con el ID coincidente
    users = [user for user in users_list if user.id == id]
    try:
        # Devuelve el primer usuario encontrado
        return users[0]
    except IndexError:
        # Si no hay coincidencias, devuelve None
        return None
