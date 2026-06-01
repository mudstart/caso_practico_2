# ============================================================
# repositories.py — Repositories: List<Entity> con lógica de acceso a datos
# Fase II | ORM nativo en POO
# ============================================================

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fase2.db_context import DbContext
from fase2.entities   import CountryEntity, CityEntity, FilmEntity, CustomerEntity


class BaseRepository:
    """
    Modelo base genérico.
    Mantiene una lista de entidades en memoria (List<Entity>)
    y se sincroniza con la BD a través de DbContext.
    """
    def __init__(self):
        self.db      = DbContext()
        self._items: list = []   # Lista interna de entidades

    @property
    def items(self) -> list:
        return self._items

    def count(self) -> int:
        return len(self._items)

    def find(self, predicate) -> list:
        """Filtra la lista en memoria."""
        return [i for i in self._items if predicate(i)]


# ── Model: CountryModel ───────────────────────────────────────
class CountryRepository(BaseRepository):

    def load_all(self) -> list:
        rows = self.db.execute_query(
            "SELECT country_id, country, last_update FROM country ORDER BY country"
        )
        self._items = [CountryEntity.from_dict(r) for r in rows]
        return self._items

    def get_by_id(self, country_id: int) -> CountryEntity:
        rows = self.db.execute_query(
            "SELECT country_id, country, last_update FROM country WHERE country_id = %s",
            (country_id,)
        )
        return CountryEntity.from_dict(rows[0]) if rows else None

    def insert(self, entity: CountryEntity) -> int:
        new_id = self.db.execute_non_query(
            "INSERT INTO country (country, last_update) VALUES (%s, NOW())",
            (entity.country,)
        )
        entity.country_id = new_id
        self._items.append(entity)
        return new_id

    def update(self, entity: CountryEntity) -> bool:
        affected = self.db.execute_non_query(
            "UPDATE country SET country = %s, last_update = NOW() WHERE country_id = %s",
            (entity.country, entity.country_id)
        )
        return affected > 0

    def delete(self, country_id: int) -> bool:
        affected = self.db.execute_non_query(
            "DELETE FROM country WHERE country_id = %s",
            (country_id,)
        )
        self._items = [c for c in self._items if c.country_id != country_id]
        return affected > 0


# ── Model: CityModel ─────────────────────────────────────────
class CityRepository(BaseRepository):

    def load_all(self) -> list:
        rows = self.db.execute_query("""
            SELECT ci.city_id, ci.city, ci.country_id,
                   co.country, ci.last_update
            FROM city ci
            JOIN country co ON ci.country_id = co.country_id
            ORDER BY ci.city
        """)
        self._items = [CityEntity.from_dict(r) for r in rows]
        return self._items

    def get_by_id(self, city_id: int) -> CityEntity:
        rows = self.db.execute_query(
            "SELECT city_id, city, country_id, last_update FROM city WHERE city_id = %s",
            (city_id,)
        )
        return CityEntity.from_dict(rows[0]) if rows else None

    def get_by_country(self, country_id: int) -> list:
        rows = self.db.execute_query(
            "SELECT city_id, city, country_id, last_update FROM city WHERE country_id = %s ORDER BY city",
            (country_id,)
        )
        return [CityEntity.from_dict(r) for r in rows]

    def insert(self, entity: CityEntity) -> int:
        new_id = self.db.execute_non_query(
            "INSERT INTO city (city, country_id, last_update) VALUES (%s, %s, NOW())",
            (entity.city, entity.country_id)
        )
        entity.city_id = new_id
        self._items.append(entity)
        return new_id

    def update(self, entity: CityEntity) -> bool:
        affected = self.db.execute_non_query(
            "UPDATE city SET city = %s, country_id = %s, last_update = NOW() WHERE city_id = %s",
            (entity.city, entity.country_id, entity.city_id)
        )
        return affected > 0

    def delete(self, city_id: int) -> bool:
        affected = self.db.execute_non_query(
            "DELETE FROM city WHERE city_id = %s",
            (city_id,)
        )
        self._items = [c for c in self._items if c.city_id != city_id]
        return affected > 0


# ── Model: FilmModel ──────────────────────────────────────────
class FilmRepository(BaseRepository):

    def load_all(self, limit: int = 200) -> list:
        rows = self.db.execute_query(
            """SELECT film_id, title, description, release_year, language_id,
                      rental_duration, rental_rate, length,
                      replacement_cost, rating, last_update
               FROM film ORDER BY title LIMIT %s""",
            (limit,)
        )
        self._items = [FilmEntity.from_dict(r) for r in rows]
        return self._items

    def get_by_id(self, film_id: int) -> FilmEntity:
        rows = self.db.execute_query(
            "SELECT * FROM film WHERE film_id = %s", (film_id,)
        )
        return FilmEntity.from_dict(rows[0]) if rows else None

    def search_by_title(self, keyword: str) -> list:
        rows = self.db.execute_query(
            "SELECT * FROM film WHERE title LIKE %s ORDER BY title",
            (f"%{keyword}%",)
        )
        return [FilmEntity.from_dict(r) for r in rows]

    def insert(self, entity: FilmEntity) -> int:
        new_id = self.db.execute_non_query(
            """INSERT INTO film (title, description, release_year, language_id,
               rental_duration, rental_rate, length, replacement_cost, rating, last_update)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())""",
            (entity.title, entity.description, entity.release_year,
             entity.language_id, entity.rental_duration, entity.rental_rate,
             entity.length, entity.replacement_cost, entity.rating)
        )
        entity.film_id = new_id
        self._items.append(entity)
        return new_id

    def update(self, entity: FilmEntity) -> bool:
        affected = self.db.execute_non_query(
            """UPDATE film SET title=%s, description=%s, rental_rate=%s,
               rating=%s, last_update=NOW() WHERE film_id=%s""",
            (entity.title, entity.description, entity.rental_rate,
             entity.rating, entity.film_id)
        )
        return affected > 0

    def delete(self, film_id: int) -> bool:
        affected = self.db.execute_non_query(
            "DELETE FROM film WHERE film_id = %s", (film_id,)
        )
        self._items = [f for f in self._items if f.film_id != film_id]
        return affected > 0


# ── Model: CustomerModel ──────────────────────────────────────
class CustomerRepository(BaseRepository):

    def load_all(self) -> list:
        rows = self.db.execute_query(
            """SELECT customer_id, store_id, first_name, last_name,
                      email, active, create_date
               FROM customer ORDER BY last_name, first_name"""
        )
        self._items = [CustomerEntity.from_dict(r) for r in rows]
        return self._items

    def get_by_id(self, customer_id: int) -> CustomerEntity:
        rows = self.db.execute_query(
            "SELECT * FROM customer WHERE customer_id = %s", (customer_id,)
        )
        return CustomerEntity.from_dict(rows[0]) if rows else None

    def insert(self, entity: CustomerEntity) -> int:
        new_id = self.db.execute_non_query(
            """INSERT INTO customer (store_id, first_name, last_name, email,
               address_id, active, create_date, last_update)
               VALUES (%s, %s, %s, %s, 1, %s, NOW(), NOW())""",
            (entity.store_id, entity.first_name, entity.last_name,
             entity.email, entity.active)
        )
        entity.customer_id = new_id
        self._items.append(entity)
        return new_id

    def update(self, entity: CustomerEntity) -> bool:
        affected = self.db.execute_non_query(
            """UPDATE customer SET first_name=%s, last_name=%s, email=%s,
               active=%s, last_update=NOW() WHERE customer_id=%s""",
            (entity.first_name, entity.last_name, entity.email,
             entity.active, entity.customer_id)
        )
        return affected > 0

    def delete(self, customer_id: int) -> bool:
        affected = self.db.execute_non_query(
            "DELETE FROM customer WHERE customer_id = %s", (customer_id,)
        )
        self._items = [c for c in self._items if c.customer_id != customer_id]
        return affected > 0
