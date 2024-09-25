from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Crear una instancia de APIRouter para definir las rutas de este módulo
router = APIRouter(
    prefix="/products", tags=["Products"], responses={404: {"message": "No encontrado"}}
)


# Definición del modelo de datos para 'Products' utilizando Pydantic.
# Este modelo será utilizado para validar y estructurar los datos de los productos.
class Products(BaseModel):
    id: int
    name: str
    value: float


# Lista simulada de productos como base de datos en memoria
products_list = [
    Products(id=1, name="Camisa", value=32.5),
    Products(id=2, name="Pantalón", value=45.98),
    Products(id=3, name="Gorra", value=15.19),
    Products(id=4, name="Chaqueta", value=50),
    Products(id=5, name="Zapatos", value=80.95),
]


# Endpoint para obtener todos los productos.
# Este endpoint devolverá la lista completa de prodcutos.
@router.get("/")
async def products():
    """
    Retorna la lista completa de Productos.

    Returns:
        List[Products]: Lista de objetos de Productos.
    """
    return products_list


# Endpoint para obtener un producto por su ID utilizando path parameters.
# Devuelve un único producto si se encuentra, o lanza una excepción 422 si no existe.
@router.get("/{id}", response_model=Products, status_code=200)
async def get_product(id: int):
    """
    Busca y retorna un producto basado en su ID.

    Args:
        id (int): El ID del producto a buscar.

    Returns:
        User: El objeto producto correspondiente al ID solicitado.

    Raises:
        HTTPException: Si el producto no es encontrado (status 422).
    """
    if search_product(id) is not None:
        return search_product(id)
    else:
        raise HTTPException(status_code=422, detail="Producto no encontrado")


def search_product(id: int):
    """
    Busca un producto por su ID dentro de la lista de productos.

    Args:
        id(int): ID del producto que se desea buscar.

    Returns:
        User: El objeto producto si se encuentra en la lista.
        None: Si no se encuentra el producto con el ID especificado

    """
    # next() busca el primer producto con ID coincidente, o devuelve None si no lo encuentra
    return next((product for product in products_list if product.id == id), None)
