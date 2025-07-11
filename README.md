# Inventory Microservice

## Descripción

El microservicio de Inventory es parte del sistema Linktic, diseñado para gestionar el inventario de productos utilizando **FastAPI** y **MongoDB** con motor asíncrono. Este servicio proporciona operaciones para consultar y actualizar productos en el inventario.

## Arquitectura

### Estructura del Proyecto

```
inventory/
├── src/
│   ├── controllers/     # Controladores de la aplicación
│   ├── entities/        # Entidades Pydantic
│   ├── repository/      # Capa de acceso a datos
│   ├── services/        # Servicios y rutas de la API
│   ├── utils/           # Utilidades e infraestructura
│   └── main.py         # Punto de entrada de la aplicación
├── test/               # Tests unitarios e integración
├── Dockerfile          # Configuración Docker
├── docker-compose.yml  # Orquestación Docker
├── pyproject.toml      # Dependencias Poetry
└── README.md          # Este archivo
```

### Tecnologías

- **FastAPI**: Framework web para APIs REST
- **Motor**: Driver asíncrono para MongoDB
- **Pydantic**: Validación de datos y serialización
- **Poetry**: Gestión de dependencias
- **Uvicorn**: Servidor ASGI
- **pytest**: Framework de testing

## Endpoints

### Health Check
```http
GET /api-inventory/health/
```
Verifica el estado del servicio de inventario.

**Response:**
```json
{
  "status": "success",
  "message": "Inventory service is running"
}
```

### Obtener Productos
```http
POST /api-inventory/products/
```
Obtiene información de productos del inventario.

**Body:**
```json
{
  "product": {
    "id": "12345"
  }
}
```

### Actualizar Producto
```http
POST /api-inventory/update-product/
```
Actualiza la información de un producto en el inventario.

**Body:**
```json
{
  "product": {
    "id": "12345"
  }
}
```

## Modelos de Datos

### Product
```python
class Product(BaseModel):
    product: Dict[str, Any] = Field(
        ..., 
        description="Product data containing id, name, and price"
    )
```

## Configuración

### Variables de Entorno
El servicio utiliza las siguientes configuraciones en `src/utils/settings.py`:

- **MongoDB Connection**: Conexión a la base de datos MongoDB
- **Database Name**: Nombre de la base de datos
- **Collection Name**: Nombre de la colección de productos

### Estructura de Configuración
```python
config = {
    "local": {
        "connection": "mongodb://localhost:27017/",
        "db": "inventory_db",
        "collection_owner": "products"
    }
}
```

## Desarrollo

### Instalación de Dependencias
```bash
poetry install
```

### Ejecutar en Desarrollo
```bash
poetry run python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8001
```

### Ejecutar Tests
```bash
# Tests unitarios
poetry run pytest

# Tests con cobertura
poetry run pytest --cov=src --cov-report=html
```

### Docker
```bash
# Construir imagen
docker build -t ms-inventory .

# Ejecutar contenedor
docker run -p 8001:8001 ms-inventory
```

### Docker Compose
Antes de levantar el container se debe crear la network para que se conecten
```bash
docker network create linktic-shared-network

# Ejecutar con docker-compose
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

## Patrones de Diseño

### Repository Pattern
El `ProductsRepository` encapsula el acceso a MongoDB usando Motor para operaciones asíncronas, en 
                        donde se obtiene asicronamente cuando se actualiza algo en la coleccion que se esta
                        comprando algun producto, esto se muestra a nivel de consola.

### Controller Pattern
Los controladores manejan la lógica de negocio:
- `GetProducts`: Para consultas de productos
- `UpdateProducts`: Para actualizaciones de productos

### Service Layer
Los servicios definen las rutas de la API y coordinan entre controladores y repositorios.

## Características Especiales

### Motor (MongoDB Asíncrono)
- Uso de `motor.motor_asyncio.AsyncIOMotorClient`
- Operaciones asíncronas para mejor rendimiento
- Conexión automática a MongoDB

### Event Handlers
- `EventHandler().startup_event`: Eventos de inicio de la aplicación
- Configuración automática al arrancar el servicio

### Error Handling
- Manejo centralizado de errores con `ErrorHandler`
- Logging estructurado con `Log`
- Respuestas consistentes en formato JSON

## Logging y Monitoreo

El servicio incluye:
- **Structured Logging**: Usando `structlog`
- **Error Handling**: Manejo centralizado de errores
- **Health Checks**: Monitoreo del estado del servicio
- **Event Handlers**: Configuración automática, que permite obtener eventos de la coleccion de la base
                      de datos MongoDB

## Docker

### Dockerfile
```dockerfile
FROM python:3.12-slim
WORKDIR /app
# ... configuración completa
CMD ["poetry", "run", "python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  ms-inventory:
    image: ms-inventory
    ports:
      - "8001:8001"
    networks:
      - linktic-network
```

## Testing

### Estructura de Tests
```
test/
├── test_controllers/    # Tests de controladores
├── test_entities/       # Tests de entidades
├── test_services/       # Tests de servicios
└── conftest.py         # Configuración de pytest
```

### Ejecutar Tests
```bash
# Todos los tests
poetry run pytest

# Tests específicos
poetry run pytest test/test_controllers/

# Tests con cobertura
poetry run pytest --cov=src --cov-report=html
```

