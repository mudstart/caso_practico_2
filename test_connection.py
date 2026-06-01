# ============================================================
# test_connection.py — Verifica la conexión a MySQL Sakila
# Ejecutar: python test_connection.py
# ============================================================

import mysql.connector
from config import DB_CONFIG

def test_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()

        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"✅ Conexión exitosa a MySQL")
        print(f"   Versión: {version[0]}")

        cursor.execute("SELECT DATABASE()")
        db = cursor.fetchone()
        print(f"   Base de datos activa: {db[0]}")

        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        print(f"\n📋 Tablas en Sakila ({len(tables)} total):")
        for t in tables:
            print(f"   - {t[0]}")

        cursor.close()
        conn.close()

    except mysql.connector.Error as e:
        print(f"❌ Error de conexión: {e}")

if __name__ == "__main__":
    test_connection()
