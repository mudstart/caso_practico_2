# ============================================================
# entities.py — Clases Entity (espejo de tablas en la BD)
# Fase II | ORM nativo en POO
# ============================================================

from datetime import datetime


class BaseEntity:
    """Clase base con utilidades comunes para todas las entidades."""

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({attrs})"


# ── Entity: Country ───────────────────────────────────────────
class CountryEntity(BaseEntity):
    """
    Espejo de la tabla `country`.
    Campos: country_id, country, last_update
    """
    def __init__(self, country_id: int = None, country: str = "",
                 last_update: datetime = None):
        self.country_id   = country_id
        self.country      = country
        self.last_update  = last_update or datetime.now()

    @classmethod
    def from_dict(cls, d: dict) -> "CountryEntity":
        return cls(
            country_id  = d.get("country_id"),
            country     = d.get("country", ""),
            last_update = d.get("last_update")
        )


# ── Entity: City ──────────────────────────────────────────────
class CityEntity(BaseEntity):
    """
    Espejo de la tabla `city`.
    Campos: city_id, city, country_id, last_update
    """
    def __init__(self, city_id: int = None, city: str = "",
                 country_id: int = None, last_update: datetime = None):
        self.city_id     = city_id
        self.city        = city
        self.country_id  = country_id
        self.last_update = last_update or datetime.now()

    @classmethod
    def from_dict(cls, d: dict) -> "CityEntity":
        return cls(
            city_id    = d.get("city_id"),
            city       = d.get("city", ""),
            country_id = d.get("country_id"),
            last_update= d.get("last_update")
        )


# ── Entity: Film ──────────────────────────────────────────────
class FilmEntity(BaseEntity):
    """
    Espejo de la tabla `film`.
    Campos principales de la tabla film de Sakila.
    """
    VALID_RATINGS = {"G", "PG", "PG-13", "R", "NC-17"}

    def __init__(self, film_id: int = None, title: str = "",
                 description: str = "", release_year: int = 2006,
                 language_id: int = 1, rental_duration: int = 3,
                 rental_rate: float = 4.99, length: int = 90,
                 replacement_cost: float = 19.99, rating: str = "G",
                 last_update: datetime = None):
        self.film_id          = film_id
        self.title            = title
        self.description      = description
        self.release_year     = release_year
        self.language_id      = language_id
        self.rental_duration  = rental_duration
        self.rental_rate      = rental_rate
        self.length           = length
        self.replacement_cost = replacement_cost
        self.rating           = rating if rating in self.VALID_RATINGS else "G"
        self.last_update      = last_update or datetime.now()

    @classmethod
    def from_dict(cls, d: dict) -> "FilmEntity":
        return cls(
            film_id          = d.get("film_id"),
            title            = d.get("title", ""),
            description      = d.get("description", ""),
            release_year     = d.get("release_year", 2006),
            language_id      = d.get("language_id", 1),
            rental_duration  = d.get("rental_duration", 3),
            rental_rate      = float(d.get("rental_rate", 4.99)),
            length           = d.get("length", 90),
            replacement_cost = float(d.get("replacement_cost", 19.99)),
            rating           = d.get("rating", "G"),
            last_update      = d.get("last_update")
        )


# ── Entity: Customer (extra) ──────────────────────────────────
class CustomerEntity(BaseEntity):
    """Espejo de la tabla `customer`."""
    def __init__(self, customer_id: int = None, store_id: int = None,
                 first_name: str = "", last_name: str = "",
                 email: str = "", active: int = 1,
                 create_date: datetime = None):
        self.customer_id = customer_id
        self.store_id    = store_id
        self.first_name  = first_name
        self.last_name   = last_name
        self.email       = email
        self.active      = active
        self.create_date = create_date or datetime.now()

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def from_dict(cls, d: dict) -> "CustomerEntity":
        return cls(
            customer_id = d.get("customer_id"),
            store_id    = d.get("store_id"),
            first_name  = d.get("first_name", ""),
            last_name   = d.get("last_name", ""),
            email       = d.get("email", ""),
            active      = d.get("active", 1),
            create_date = d.get("create_date")
        )
