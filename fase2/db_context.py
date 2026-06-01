# ============================================================
# db_context.py — DbContext: gestión de conexión a MySQL
# Fase II | ORM nativo en POO
# ============================================================

import mysql.connector
from mysql.connector import Error
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DB_CONFIG


class DbContext:
    """
    Capa de abstracción de conexión a la base de datos.
    Equivalente al DbContext de Entity Framework (C#).
    Gestiona la conexión y provee métodos genéricos de consulta.
    """

    _instance = None  # Singleton

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    # ── Conexión ──────────────────────────────────────────────
    def connect(self):
        try:
            if self._connection is None or not self._connection.is_connected():
                self._connection = mysql.connector.connect(**DB_CONFIG)
                print("[DbContext] Conexión establecida.")
        except Error as e:
            print(f"[DbContext] Error al conectar: {e}")
            raise

    def disconnect(self):
        if self._connection and self._connection.is_connected():
            self._connection.close()
            print("🔌 [DbContext] Conexión cerrada.")

    def get_connection(self):
        self.connect()
        return self._connection

    # ── Operaciones genéricas ─────────────────────────────────
    def execute_query(self, sql: str, params: tuple = ()) -> list:
        """Ejecuta un SELECT y retorna lista de dicts."""
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql, params)
        results = cursor.fetchall()
        cursor.close()
        return results

    def execute_non_query(self, sql: str, params: tuple = ()) -> int:
        """Ejecuta INSERT/UPDATE/DELETE. Retorna lastrowid o rowcount."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params)
        conn.commit()
        result = cursor.lastrowid if cursor.lastrowid else cursor.rowcount
        cursor.close()
        return result

    def execute_many(self, sql: str, data: list) -> int:
        """Ejecuta INSERT/UPDATE en lote. Retorna filas afectadas."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.executemany(sql, data)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        return affected

    # ── Context Manager ───────────────────────────────────────
    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
