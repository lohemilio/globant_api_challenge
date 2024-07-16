from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text

app = Flask(__name__)
DATABASE_URI = 'sqlite:///test.db'
engine = create_engine(DATABASE_URI)

# Crear las tablas en la base de datos
def create_tables():
    with engine.connect() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY,
            position_name TEXT
        )
        """))
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            full_name TEXT,
            hire_date TEXT,
            number1 INTEGER,
            number2 INTEGER
        )
        """))

create_tables()