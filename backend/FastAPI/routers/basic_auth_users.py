from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Instancia de la aplicación FastAPI
app = FastAPI()

# Definición del esquema de autenticación OAuth2 que espera un token Bearer
oauth2 = OAuth2PasswordBearer(tokenUrl="login")


# Modelo que define los atributos de un usuario básico
class User(BaseModel):
    username: str  # Nombre de usuario
    full_name: str  # Nombre completo del usuario
    email: str  # Correo electrónico del usuario
    disable: bool  # Estado de deshabilitación del usuario


# Modelo de usuario para la base de datos, que incluye la contraseña
class UserDB(User):
    password: str  # Contraseña del usuario


# Base de datos simulada que contiene información de usuarios ficticios
users_db = {
    "Nigguelf": {
        "username": "Nigguelf",
        "full_name": "Nigguel Fernandez",
        "email": "nigguel@python.com",
        "disable": False,
        "password": "123456",  # Contraseña del usuario
    },
    "Nixonf": {
        "username": "Nixonf",
        "full_name": "Nixon Fernandez",
        "email": "nixon@python.com",
        "disable": True,  # Usuario deshabilitado
        "password": "654321",
    },
}


# Función que busca un usuario en la base de datos y retorna una instancia del modelo UserDB
def search_user_db(username: str):
    """
    Busca en la base de datos el usuario proporcionado.

    Args:
        username (str): Nombre de usuario a buscar.

    Returns:
        UserDB: Instancia del modelo UserDB si se encuentra el usuario.
    """
    if username in users_db:
        # Se convierte el diccionario de usuario en una instancia del modelo UserDB
        return UserDB(users_db[username])


# Función que busca un usuario en la base de datos y retorna una instancia del modelo User
def search_user(username: str):
    """
    Busca en la base de datos el usuario proporcionado pero sin la contraseña.

    Args:
        username (str): Nombre de usuario a buscar.

    Returns:
        User: Instancia del modelo User si se encuentra el usuario.
    """
    if username in users_db:
        # Se convierte el diccionario de usuario en una instancia del modelo User (sin contraseña)
        return User(**users_db[username])


# Función asincrónica para obtener el usuario actual a partir del token de OAuth2
async def current_user(token: str = Depends(oauth2)):
    """
    Verifica y retorna el usuario actual autenticado según el token de OAuth2.

    Args:
        token (str): Token de autenticación obtenido a través de OAuth2.

    Returns:
        User: Instancia del modelo User si el usuario está autenticado correctamente.

    Raises:
        HTTPException: Si el usuario no es encontrado o si está deshabilitado.
    """
    # Se usa el token (nombre de usuario) para buscar el usuario en la base de datos
    user = search_user(token)
    if not user:
        # Si no se encuentra el usuario, se lanza una excepción HTTP de no autorizado
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales de autenticación inválidas",
            headers={"www-Authenticate": "Bearer"},
        )

    if user.disable:
        # Si el usuario está deshabilitado, se lanza una excepción HTTP de solicitud incorrecta
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )
    # Retorna el usuario actual si todo es correcto
    return user


# Ruta para el inicio de sesión de los usuarios
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Verifica las credenciales del usuario y retorna un token de acceso si es válido.

    Args:
        form (OAuth2PasswordRequestForm): Datos del formulario de login que incluyen username y password.

    Returns:
        dict: Diccionario que contiene el token de acceso y el tipo de token.

    Raises:
        HTTPException: Si el usuario no es encontrado o si la contraseña es incorrecta.
    """
    # Busca el usuario en la base de datos por su nombre de usuario
    user_db = users_db.get(form.username)
    if not user_db:
        # Si no se encuentra el usuario, se lanza una excepción de solicitud incorrecta
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario no es correcto",
        )

    # Se busca el usuario completo incluyendo la contraseña
    user = search_user_db(form.username)
    if form.password == user.password:
        # Si la contraseña no es correcta, se lanza una excepción de solicitud incorrecta
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta",
        )

    # Si el usuario y la contraseña son correctos, se genera un token de acceso
    return {"access_token": user.username, "token_type": "bearer"}


# Ruta para obtener los detalles del usuario actual autenticado
@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    """
    Retorna la información del usuario autenticado.

    Args:
        user (User): Usuario autenticado obtenido a través de la dependencia `current_user`.

    Returns:
        User: La instancia del usuario autenticado.
    """
    # Retorna los detalles del usuario autenticado
    return user
