# ============================================================
# crud_city.py — CRUD básico para la tabla CITY
# Fase I | Caso Práctico 2
# ============================================================

import mysql.connector
import csv
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ── CREATE ────────────────────────────────────────────────────
def create_city(city_name: str, country_id: int) -> int:
    """Inserta una nueva ciudad. Retorna el ID generado."""
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO city (city, country_id, last_update) VALUES (%s, %s, NOW())"
    cursor.execute(sql, (city_name, country_id))
    conn.commit()
    new_id = cursor.lastrowid
    print(f"✅ Ciudad creada: ID={new_id}, city='{city_name}', country_id={country_id}")
    cursor.close()
    conn.close()
    return new_id


# ── READ (todos) ──────────────────────────────────────────────
def read_all_cities() -> list:
    """Retorna todas las ciudades con su país."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT ci.city_id, ci.city, co.country, ci.last_update
        FROM city ci
        JOIN country co ON ci.country_id = co.country_id
        ORDER BY ci.city
    """
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── READ (por ID) ─────────────────────────────────────────────
def read_city_by_id(city_id: int) -> dict:
    """Retorna una ciudad por su ID."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT ci.city_id, ci.city, co.country_id, co.country, ci.last_update
        FROM city ci
        JOIN country co ON ci.country_id = co.country_id
        WHERE ci.city_id = %s
    """
    cursor.execute(sql, (city_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


# ── UPDATE ────────────────────────────────────────────────────
def update_city(city_id: int, new_name: str = None, new_country_id: int = None):
    """Actualiza el nombre o el país de una ciudad."""
    conn = get_connection()
    cursor = conn.cursor()
    fields, params = [], []
    if new_name:
        fields.append("city = %s")
        params.append(new_name)
    if new_country_id:
        fields.append("country_id = %s")
        params.append(new_country_id)
    if not fields:
        print("⚠️  No se proporcionaron campos a actualizar.")
        return
    fields.append("last_update = NOW()")
    params.append(city_id)
    sql = f"UPDATE city SET {', '.join(fields)} WHERE city_id = %s"
    cursor.execute(sql, params)
    conn.commit()
    print(f"✅ Ciudad ID={city_id} actualizada.")
    cursor.close()
    conn.close()


# ── DELETE ────────────────────────────────────────────────────
def delete_city(city_id: int):
    """Elimina una ciudad por su ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM city WHERE city_id = %s", (city_id,))
    conn.commit()
    affected = cursor.rowcount
    if affected:
        print(f"✅ Ciudad ID={city_id} eliminada.")
    else:
        print(f"⚠️  Ciudad ID={city_id} no encontrada.")
    cursor.close()
    conn.close()


# ── EXPORT CSV ───────────────────────────────────────────────
def export_cities_to_csv(filepath: str = "data/cities.csv"):
    """Exporta todas las ciudades a un archivo CSV."""
    rows = read_all_cities()
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["city_id", "city", "country", "last_update"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ {len(rows)} ciudades exportadas a '{filepath}'")


# ── IMPORT CSV ───────────────────────────────────────────────
def import_cities_from_csv(filepath: str = "data/cities.csv"):
    """Importa ciudades desde un CSV (requiere columnas: city, country_id)."""
    conn = get_connection()
    cursor = conn.cursor()
    count = 0
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                "INSERT INTO city (city, country_id, last_update) VALUES (%s, %s, NOW())",
                (row["city"], int(row["country_id"]))
            )
            count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {count} ciudades importadas desde '{filepath}'")


# ── EXPORT JSON ──────────────────────────────────────────────
def export_cities_to_json(filepath: str = "data/cities.json"):
    """Exporta todas las ciudades a JSON."""
    rows = read_all_cities()
    # convertir datetime a string
    for r in rows:
        if r.get("last_update"):
            r["last_update"] = str(r["last_update"])
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)
    print(f"✅ {len(rows)} ciudades exportadas a '{filepath}'")


# ── IMPORT JSON ──────────────────────────────────────────────
def import_cities_from_json(filepath: str = "data/cities.json"):
    """Importa ciudades desde un JSON (requiere campos: city, country_id)."""
    conn = get_connection()
    cursor = conn.cursor()
    with open(filepath, encoding="utf-8") as f:
        rows = json.load(f)
    count = 0
    for row in rows:
        cursor.execute(
            "INSERT INTO city (city, country_id, last_update) VALUES (%s, %s, NOW())",
            (row["city"], int(row["country_id"]))
        )
        count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {count} ciudades importadas desde '{filepath}'")


# ── DEMO ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== CRUD CITY — DEMO ===\n")

    # READ
    cities = read_all_cities()
    print(f"Total ciudades en BD: {len(cities)}")
    print("Primeras 5:")
    for c in cities[:5]:
        print(f"  {c}")

    # CREATE
    new_id = create_city("Ciudad de Prueba", 1)

    # READ by ID
    city = read_city_by_id(new_id)
    print(f"\nCiudad recién creada: {city}")

    # UPDATE
    update_city(new_id, new_name="Ciudad Actualizada")

    # DELETE
    delete_city(new_id)

    # EXPORT
    export_cities_to_csv("../data/cities.csv")
    export_cities_to_json("../data/cities.json")
