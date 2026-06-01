# ============================================================
# controllers.py — Capa Controller (patrón MVC)
# Recibe peticiones, orquesta Repositories y retorna respuestas
# Fase II | ORM nativo en POO
# ============================================================

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fase2.repositories import CountryRepository, CityRepository, FilmRepository, CustomerRepository
from fase2.entities import CountryEntity, CityEntity, FilmEntity, CustomerEntity


class BaseController:
    """Respuesta estándar para todos los controllers."""

    @staticmethod
    def ok(data=None, message: str = "OK") -> dict:
        return {"status": "success", "message": message, "data": data}

    @staticmethod
    def error(message: str, data=None) -> dict:
        return {"status": "error", "message": message, "data": data}


# ── CountryController ─────────────────────────────────────────
class CountryController(BaseController):

    def __init__(self):
        self.repository = CountryRepository()

    def get_all(self) -> dict:
        countries = self.repository.load_all()
        return self.ok(
            data=[c.to_dict() for c in countries],
            message=f"{len(countries)} países encontrados."
        )

    def get_by_id(self, country_id: int) -> dict:
        entity = self.repository.get_by_id(country_id)
        if entity:
            return self.ok(data=entity.to_dict())
        return self.error(f"País ID={country_id} no encontrado.")

    def create(self, country_name: str) -> dict:
        if not country_name or not country_name.strip():
            return self.error("El nombre del país no puede estar vacío.")
        entity = CountryEntity(country=country_name.strip())
        new_id = self.repository.insert(entity)
        return self.ok(data={"country_id": new_id}, message=f"País '{country_name}' creado.")

    def update(self, country_id: int, country_name: str) -> dict:
        entity = self.repository.get_by_id(country_id)
        if not entity:
            return self.error(f"País ID={country_id} no encontrado.")
        entity.country = country_name
        success = self.repository.update(entity)
        if success:
            return self.ok(message=f"País ID={country_id} actualizado a '{country_name}'.")
        return self.error("No se pudo actualizar.")

    def delete(self, country_id: int) -> dict:
        success = self.repository.delete(country_id)
        if success:
            return self.ok(message=f"País ID={country_id} eliminado.")
        return self.error(f"País ID={country_id} no encontrado.")


# ── CityController ────────────────────────────────────────────
class CityController(BaseController):

    def __init__(self):
        self.repository = CityRepository()

    def get_all(self) -> dict:
        cities = self.repository.load_all()
        return self.ok(
            data=[c.to_dict() for c in cities],
            message=f"{len(cities)} ciudades encontradas."
        )

    def get_by_id(self, city_id: int) -> dict:
        entity = self.repository.get_by_id(city_id)
        if entity:
            return self.ok(data=entity.to_dict())
        return self.error(f"Ciudad ID={city_id} no encontrada.")

    def get_by_country(self, country_id: int) -> dict:
        cities = self.repository.get_by_country(country_id)
        return self.ok(
            data=[c.to_dict() for c in cities],
            message=f"{len(cities)} ciudades en país ID={country_id}."
        )

    def create(self, city_name: str, country_id: int) -> dict:
        if not city_name or not city_name.strip():
            return self.error("El nombre de la ciudad no puede estar vacío.")
        entity = CityEntity(city=city_name.strip(), country_id=country_id)
        new_id = self.repository.insert(entity)
        return self.ok(data={"city_id": new_id}, message=f"Ciudad '{city_name}' creada.")

    def update(self, city_id: int, city_name: str = None, country_id: int = None) -> dict:
        entity = self.repository.get_by_id(city_id)
        if not entity:
            return self.error(f"Ciudad ID={city_id} no encontrada.")
        if city_name:    entity.city       = city_name
        if country_id:   entity.country_id = country_id
        success = self.repository.update(entity)
        return self.ok(message=f"Ciudad ID={city_id} actualizada.") if success else self.error("No se pudo actualizar.")

    def delete(self, city_id: int) -> dict:
        success = self.repository.delete(city_id)
        return self.ok(message=f"Ciudad ID={city_id} eliminada.") if success else self.error(f"Ciudad ID={city_id} no encontrada.")


# ── FilmController ────────────────────────────────────────────
class FilmController(BaseController):

    def __init__(self):
        self.repository = FilmRepository()

    def get_all(self, limit: int = 50) -> dict:
        films = self.repository.load_all(limit=limit)
        return self.ok(
            data=[f.to_dict() for f in films],
            message=f"{len(films)} películas cargadas."
        )

    def get_by_id(self, film_id: int) -> dict:
        entity = self.repository.get_by_id(film_id)
        if entity:
            return self.ok(data=entity.to_dict())
        return self.error(f"Película ID={film_id} no encontrada.")

    def search(self, keyword: str) -> dict:
        films = self.repository.search_by_title(keyword)
        return self.ok(
            data=[f.to_dict() for f in films],
            message=f"{len(films)} resultado(s) para '{keyword}'."
        )

    def create(self, title: str, description: str = "", release_year: int = 2024,
               language_id: int = 1, rental_rate: float = 4.99,
               length: int = 90, rating: str = "G") -> dict:
        if not title or not title.strip():
            return self.error("El título no puede estar vacío.")
        entity = FilmEntity(
            title=title.strip(), description=description,
            release_year=release_year, language_id=language_id,
            rental_rate=rental_rate, length=length, rating=rating
        )
        new_id = self.repository.insert(entity)
        return self.ok(data={"film_id": new_id}, message=f"Película '{title}' creada.")

    def update(self, film_id: int, title: str = None, rental_rate: float = None,
               description: str = None, rating: str = None) -> dict:
        entity = self.repository.get_by_id(film_id)
        if not entity:
            return self.error(f"Película ID={film_id} no encontrada.")
        if title:       entity.title       = title
        if rental_rate: entity.rental_rate = rental_rate
        if description: entity.description = description
        if rating:      entity.rating      = rating
        success = self.repository.update(entity)
        return self.ok(message=f"Película ID={film_id} actualizada.") if success else self.error("No se pudo actualizar.")

    def delete(self, film_id: int) -> dict:
        success = self.repository.delete(film_id)
        return self.ok(message=f"Película ID={film_id} eliminada.") if success else self.error(f"Película ID={film_id} no encontrada.")


# ── CustomerController ────────────────────────────────────────
class CustomerController(BaseController):

    def __init__(self):
        self.repository = CustomerRepository()

    def get_all(self) -> dict:
        customers = self.repository.load_all()
        return self.ok(
            data=[c.to_dict() for c in customers],
            message=f"{len(customers)} clientes encontrados."
        )

    def get_by_id(self, customer_id: int) -> dict:
        entity = self.repository.get_by_id(customer_id)
        if entity:
            return self.ok(data=entity.to_dict())
        return self.error(f"Cliente ID={customer_id} no encontrado.")

    def create(self, first_name: str, last_name: str, email: str,
               store_id: int = 1) -> dict:
        entity = CustomerEntity(
            first_name=first_name, last_name=last_name,
            email=email, store_id=store_id
        )
        new_id = self.repository.insert(entity)
        # Releer desde BD para obtener todos los campos generados (create_date, etc.)
        created = self.repository.get_by_id(new_id)
        return self.ok(
            data=created.to_dict() if created else {"customer_id": new_id},
            message=f"Cliente '{first_name} {last_name}' creado."
        )

    def update(self, customer_id: int, **kwargs) -> dict:
        entity = self.repository.get_by_id(customer_id)
        if not entity:
            return self.error(f"Cliente ID={customer_id} no encontrado.")
        for key, val in kwargs.items():
            if hasattr(entity, key):
                setattr(entity, key, val)
        success = self.repository.update(entity)
        return self.ok(message=f"Cliente ID={customer_id} actualizado.") if success else self.error("No se pudo actualizar.")

    def delete(self, customer_id: int) -> dict:
        success = self.repository.delete(customer_id)
        return self.ok(message=f"Cliente ID={customer_id} eliminado.") if success else self.error(f"Cliente ID={customer_id} no encontrado.")
