from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Crear una instancia de APIRouter para definir las rutas de este módulo
router = APIRouter(prefix="/user", tags=["Users"])


# Definición del modelo de datos para 'User' utilizando Pydantic.
# Este modelo será utilizado para validar y estructurar los datos de los usuarios.
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


# Lista simulada de usuarios como base de datos en memoria
users_list = [
    User(id=1, name="Nigguel", surname="Fernández", url="https://nigguel.com", age=26),
    User(id=2, name="Genesis", surname="Castañeda", url="https://genesis.com", age=20),
    User(id=3, name="Jasmin", surname="Salcedo", url="https://jasmin.com", age=49),
]


# Endpoint para obtener todos los usuarios.
# Este endpoint devolverá la lista completa de usuarios.
@router.get("/users/")
async def users():
    """
    Retorna la lista completa de usuarios.

    Returns:
        List[User]: Lista de objetos de usuarios.
    """
    return users_list


# Endpoint para obtener un usuario por su ID utilizando path parameters.
# Devuelve un único usuario si se encuentra, o lanza una excepción 422 si no existe.
@router.get("/{id}", response_model=User, status_code=200)
async def get_user(id: int):
    """
    Busca y retorna un usuario basado en su ID.

    Args:
        id (int): El ID del usuario a buscar.

    Returns:
        User: El objeto usuario correspondiente al ID solicitado.

    Raises:
        HTTPException: Si el usuario no es encontrado (status 422).
    """
    if search_user(id) is not None:
        return search_user(id)
    else:
        raise HTTPException(status_code=422, detail="Usuario no encontrado")


# Endpoint para crear un nuevo usuario.
# Valida si el usuario ya existe; si no existe, lo agrega a la lista.
@router.post("/", response_model=User, status_code=201)
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

    if search_user(user.id):
        raise HTTPException(status_code=409, detail="El usuario ya existe")
    users_list.append(user)  # Agregar el nuevo usuario a la lista
    return user


# Endpoint para actualizar un usuario existente.
# Busca al usuario por su ID y actualiza sus datos.
@router.put("/", response_model=User, status_code=200)
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
    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user  # Actualiza el usuario en la lista
            return user
    raise HTTPException(status_code=422, detail="Usuario no encontrado para actualizar")


# Endpoint para eliminar un usuario existente por su ID.
# Devuelve un código 204 si la operación es exitosa.
@router.delete("/{id}", status_code=204)
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
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]  # Eliminar el usuario de la lista
            return {"exito": "usuario borrado exitosamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado para eliminar")


def search_user(id: int):
    """
    Busca un usuario por su ID dentro de la lista de usuarios.

    Args:
        id(int): ID del usuario que se desea buscar.

    Returns:
        User: El objeto usuario si se encuentra en la lista.
        None: Si no se encuentra el usuario con el ID especificado

    """
    # next() busca el primer usuario con ID coincidente, o devuelve None si no lo encuentra
    return next((user for user in users_list if user.id == id), None)
