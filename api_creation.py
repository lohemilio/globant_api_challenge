from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine, text
import sqlite3

app = Flask(__name__)
DATABASE_URI = 'sqlite:///test.db'
engine = create_engine(DATABASE_URI)

# Crear las tablas en la base de datos
def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER,
            name TEXT
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER,
            position_name TEXT
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER,
            full_name TEXT,
            hire_date TEXT,
            number1 INTEGER,
            number2 INTEGER
        )
        """))

create_tables()

# Endpoint para subir archivos CSV
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    files = request.files
    table_columns = {
        'departments': ['id', 'name'],
        'jobs': ['id', 'position_name'],
        'employees': ['id', 'full_name', 'hire_date', 'number1', 'number2']
    }

    # Conectar a la base de datos SQLite
    conn = sqlite3.connect('test.db')
    for table_name in files:
        file = files[table_name]
        # Leer el archivo CSV (no tiene column headers)
        df = pd.read_csv(file, header=None, names=table_columns[table_name])
        # Insertar datos en la tabla correspondiente
        df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
    
    return jsonify({"message": "Files uploaded successfully"}), 200

# Endpoint para insertar datos en batch
@app.route('/batch_insert', methods=['POST'])
def batch_insert():
    data = request.json
    table_name = data.get('table')
    rows = data.get('rows')
    if not table_name or not rows:
        return jsonify({"message": "Invalid request"}), 400

    table_columns = {
        'departments': ['id', 'name'],
        'jobs': ['id', 'position_name'],
        'employees': ['id', 'full_name', 'hire_date', 'number1', 'number2']
    }

    if table_name not in table_columns:
        return jsonify({"message": "Invalid table name"}), 400

     # Crear un DataFrame con los datos proporcionados
    df = pd.DataFrame(rows, columns=table_columns[table_name])
    
    conn = sqlite3.connect('test.db')

    # Insertar los datos en la tabla correspondiente
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()
    
    return jsonify({"message": "Batch insert successful"}), 200

if __name__ == '__main__':
    app.run(debug=True)