# ============================================================
# crud_country.py — CRUD básico para la tabla COUNTRY
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
def create_country(country_name: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO country (country, last_update) VALUES (%s, NOW())",
        (country_name,)
    )
    conn.commit()
    new_id = cursor.lastrowid
    print(f"✅ País creado: ID={new_id}, country='{country_name}'")
    cursor.close()
    conn.close()
    return new_id


# ── READ (todos) ──────────────────────────────────────────────
def read_all_countries() -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT country_id, country, last_update FROM country ORDER BY country")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── READ (por ID) ─────────────────────────────────────────────
def read_country_by_id(country_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT country_id, country, last_update FROM country WHERE country_id = %s",
        (country_id,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


# ── UPDATE ────────────────────────────────────────────────────
def update_country(country_id: int, new_name: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE country SET country = %s, last_update = NOW() WHERE country_id = %s",
        (new_name, country_id)
    )
    conn.commit()
    print(f"✅ País ID={country_id} actualizado a '{new_name}'")
    cursor.close()
    conn.close()


# ── DELETE ────────────────────────────────────────────────────
def delete_country(country_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM country WHERE country_id = %s", (country_id,))
    conn.commit()
    affected = cursor.rowcount
    msg = f"✅ País ID={country_id} eliminado." if affected else f"⚠️  País ID={country_id} no encontrado."
    print(msg)
    cursor.close()
    conn.close()


# ── EXPORT CSV ───────────────────────────────────────────────
def export_countries_to_csv(filepath: str = "data/countries.csv"):
    rows = read_all_countries()
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["country_id", "country", "last_update"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ {len(rows)} países exportados a '{filepath}'")


# ── IMPORT CSV ───────────────────────────────────────────────
def import_countries_from_csv(filepath: str = "data/countries.csv"):
    conn = get_connection()
    cursor = conn.cursor()
    count = 0
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                "INSERT INTO country (country, last_update) VALUES (%s, NOW())",
                (row["country"],)
            )
            count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {count} países importados desde '{filepath}'")


# ── EXPORT JSON ──────────────────────────────────────────────
def export_countries_to_json(filepath: str = "data/countries.json"):
    rows = read_all_countries()
    for r in rows:
        if r.get("last_update"):
            r["last_update"] = str(r["last_update"])
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)
    print(f"✅ {len(rows)} países exportados a '{filepath}'")


# ── IMPORT JSON ──────────────────────────────────────────────
def import_countries_from_json(filepath: str = "data/countries.json"):
    conn = get_connection()
    cursor = conn.cursor()
    with open(filepath, encoding="utf-8") as f:
        rows = json.load(f)
    count = 0
    for row in rows:
        cursor.execute(
            "INSERT INTO country (country, last_update) VALUES (%s, NOW())",
            (row["country"],)
        )
        count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {count} países importados desde '{filepath}'")


# ── DEMO ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== CRUD COUNTRY — DEMO ===\n")
    countries = read_all_countries()
    print(f"Total países: {len(countries)}")
    for c in countries[:5]:
        print(f"  {c}")

    new_id = create_country("País de Prueba")
    print(f"\nCreado: {read_country_by_id(new_id)}")
    update_country(new_id, "País Actualizado")
    delete_country(new_id)

    export_countries_to_csv("../data/countries.csv")
    export_countries_to_json("../data/countries.json")
