# API para Migración de Base de Datos

Esta es una API construida con Flask para manejar la migración de datos a una base de datos SQL (SQLite en este caso). La API permite subir datos históricos desde archivos CSV y realizar inserciones por lotes en las tablas `departments`, `jobs` y `employees`.

## Requisitos

- Python 3.6 o superior
- Flask
- pandas
- SQLAlchemy
- sqlite3

## Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio

2. Crea un entorno virtual y activa el entorno:
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

3. Instala las dependencias:
    ```bash
    pip install flask pandas sqlalchemy sqlite3

## Uso

### Ejecuta el servidor Flask:

    ```bash
python api_creation.py

La API estará disponible en [http://localhost:5000](http://localhost:5000).

### Endpoints

#### 1. Subir archivos CSV
- **URL:** `/upload_csv`
- **Método:** `POST`
- **Descripción:** Este endpoint recibe archivos CSV sin encabezados y los inserta en las tablas correspondientes.

**Ejemplo usando Postman:**

1. Selecciona `POST` como método.
2. URL: `http://localhost:5000/upload_csv`
3. En la pestaña `Body`, selecciona `form-data`.
4. Agrega los archivos con los nombres de las tablas (`departments`, `jobs`, `employees`) como claves.

#### 2. Insertar datos por lotes
- **URL:** `/batch_insert`
- **Método:** `POST`
- **Descripción:** Este endpoint recibe un JSON con datos para insertar en las tablas correspondientes en lotes.

Ejemplo: 

{
    "table": "nombre_de_la_tabla",
    "rows": [
        { "columna1": "valor1", "columna2": "valor2", ... },
        ...
    ]
}




