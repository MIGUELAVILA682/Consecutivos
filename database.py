import sqlite3
from datetime import datetime
import os

DB_NAME = "consecutivos.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consecutivos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                numero TEXT,
                fecha TEXT,
                asunto TEXT,
                elaborado_por TEXT
            )
        """)
        conn.commit()

def crear_consecutivo(asunto, elaborado_por):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT numero FROM consecutivos ORDER BY id DESC LIMIT 1")
        ultimo = cursor.fetchone()
        if ultimo:
            ultimo_num = int(ultimo[0][1:]) + 1
        else:
            ultimo_num = 1
        nuevo = f"C{ultimo_num:06d}"
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        cursor.execute("""
            INSERT INTO consecutivos (numero, fecha, asunto, elaborado_por)
            VALUES (?, ?, ?, ?)
        """, (nuevo, fecha_actual, asunto, elaborado_por))
        conn.commit()
        return nuevo

def obtener_hojas():
    return ["Formulario"]