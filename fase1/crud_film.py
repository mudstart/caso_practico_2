# ============================================================
# crud_film.py — CRUD básico para la tabla FILM
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
def create_film(title: str, description: str, release_year: int,
                language_id: int = 1, rental_duration: int = 3,
                rental_rate: float = 4.99, length: int = 90,
                replacement_cost: float = 19.99, rating: str = "G") -> int:
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO film
            (title, description, release_year, language_id,
             rental_duration, rental_rate, length,
             replacement_cost, rating, last_update)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """
    cursor.execute(sql, (title, description, release_year, language_id,
                         rental_duration, rental_rate, length,
                         replacement_cost, rating))
    conn.commit()
    new_id = cursor.lastrowid
    print(f"✅ Película creada: ID={new_id}, title='{title}'")
    cursor.close()
    conn.close()
    return new_id


# ── READ (todos) ──────────────────────────────────────────────
def read_all_films(limit: int = 100) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT f.film_id, f.title, f.release_year, f.rating,
               f.rental_rate, f.length, l.name AS language
        FROM film f
        JOIN language l ON f.language_id = l.language_id
        ORDER BY f.title
        LIMIT %s
    """
    cursor.execute(sql, (limit,))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── READ (por ID) ─────────────────────────────────────────────
def read_film_by_id(film_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = """
        SELECT f.*, l.name AS language
        FROM film f
        JOIN language l ON f.language_id = l.language_id
        WHERE f.film_id = %s
    """
    cursor.execute(sql, (film_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row


# ── READ (búsqueda por título) ────────────────────────────────
def search_films_by_title(keyword: str) -> list:
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT film_id, title, rating, rental_rate, length FROM film WHERE title LIKE %s ORDER BY title",
        (f"%{keyword}%",)
    )
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows


# ── UPDATE ────────────────────────────────────────────────────
def update_film(film_id: int, title: str = None, rental_rate: float = None,
                description: str = None, rating: str = None):
    conn = get_connection()
    cursor = conn.cursor()
    fields, params = [], []
    if title:        fields.append("title = %s");        params.append(title)
    if rental_rate:  fields.append("rental_rate = %s");  params.append(rental_rate)
    if description:  fields.append("description = %s");  params.append(description)
    if rating:       fields.append("rating = %s");       params.append(rating)
    if not fields:
        print("⚠️  No se proporcionaron campos a actualizar.")
        return
    fields.append("last_update = NOW()")
    params.append(film_id)
    sql = f"UPDATE film SET {', '.join(fields)} WHERE film_id = %s"
    cursor.execute(sql, params)
    conn.commit()
    print(f"✅ Película ID={film_id} actualizada.")
    cursor.close()
    conn.close()


# ── DELETE ────────────────────────────────────────────────────
def delete_film(film_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM film WHERE film_id = %s", (film_id,))
    conn.commit()
    affected = cursor.rowcount
    msg = f"✅ Película ID={film_id} eliminada." if affected else f"⚠️  Película ID={film_id} no encontrada."
    print(msg)
    cursor.close()
    conn.close()


# ── EXPORT CSV ───────────────────────────────────────────────
def export_films_to_csv(filepath: str = "data/films.csv"):
    rows = read_all_films(limit=10000)
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ {len(rows)} películas exportadas a '{filepath}'")


# ── IMPORT CSV ───────────────────────────────────────────────
def import_films_from_csv(filepath: str = "data/films.csv"):
    conn = get_connection()
    cursor = conn.cursor()
    count = 0
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute(
                """INSERT INTO film (title, description, release_year, language_id,
                   rental_duration, rental_rate, length, replacement_cost, rating, last_update)
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
                (row["title"], row.get("description",""), row.get("release_year", 2006),
                 row.get("language_id", 1), row.get("rental_duration", 3),
                 row.get("rental_rate", 4.99), row.get("length", 90),
                 row.get("replacement_cost", 19.99), row.get("rating","G"))
            )
            count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {count} películas importadas desde '{filepath}'")


# ── EXPORT JSON ──────────────────────────────────────────────
def export_films_to_json(filepath: str = "data/films.json"):
    rows = read_all_films(limit=10000)
    for r in rows:
        for k, v in r.items():
            if hasattr(v, 'isoformat'):
                r[k] = str(v)
    os.makedirs(os.path.dirname(filepath), exist_ok=True) if os.path.dirname(filepath) else None
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=4, ensure_ascii=False)
    print(f"✅ {len(rows)} películas exportadas a '{filepath}'")


# ── IMPORT JSON ──────────────────────────────────────────────
def import_films_from_json(filepath: str = "data/films.json"):
    conn = get_connection()
    cursor = conn.cursor()
    with open(filepath, encoding="utf-8") as f:
        rows = json.load(f)
    count = 0
    for row in rows:
        cursor.execute(
            """INSERT INTO film (title, description, release_year, language_id,
               rental_duration, rental_rate, length, replacement_cost, rating, last_update)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
            (row["title"], row.get("description",""), row.get("release_year", 2006),
             row.get("language_id", 1), row.get("rental_duration", 3),
             row.get("rental_rate", 4.99), row.get("length", 90),
             row.get("replacement_cost", 19.99), row.get("rating","G"))
        )
        count += 1
    conn.commit()
    cursor.close()
    conn.close()
    print(f"✅ {count} películas importadas desde '{filepath}'")


# ── DEMO ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n=== CRUD FILM — DEMO ===\n")
    films = read_all_films(limit=5)
    print("Primeras 5 películas:")
    for f in films:
        print(f"  {f}")

    results = search_films_by_title("ACADEMY")
    print(f"\nBúsqueda 'ACADEMY': {len(results)} resultados")

    new_id = create_film(
        title="TEST MOVIE",
        description="Película de prueba",
        release_year=2024,
        language_id=1
    )
    update_film(new_id, rental_rate=2.99, rating="PG")
    delete_film(new_id)

    export_films_to_csv("../data/films.csv")
    export_films_to_json("../data/films.json")
