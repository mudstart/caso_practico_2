# ============================================================
# main.py — Demo completo del ORM nativo (Fase II)
# Ejecutar: python fase2/main.py
# ============================================================

import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from fase2.controllers import CountryController, CityController, FilmController, CustomerController


def print_response(label: str, response: dict):
    status_icon = "✅" if response["status"] == "success" else "❌"
    print(f"\n{status_icon} [{label}] {response['message']}")
    if response.get("data") and not isinstance(response["data"], list):
        print(f"   Data: {response['data']}")
    elif response.get("data") and isinstance(response["data"], list):
        print(f"   Registros: {len(response['data'])}")
        for item in response["data"][:3]:
            print(f"     {item}")
        if len(response["data"]) > 3:
            print(f"     ... y {len(response['data']) - 3} más")


def demo_country():
    print("\n" + "=" * 55)
    print("  COUNTRY CONTROLLER — CRUD Demo")
    print("=" * 55)
    ctrl = CountryController()

    r = ctrl.get_all()
    print_response("GET ALL", r)

    r = ctrl.get_by_id(1)
    print_response("GET BY ID=1", r)

    r = ctrl.create("Invernalia")
    print_response("CREATE", r)
    new_id = r["data"]["country_id"] if r["status"] == "success" else None

    if new_id:
        r = ctrl.update(new_id, "País Invernalia Actualizado")
        print_response("UPDATE", r)

        r = ctrl.delete(new_id)
        print_response("DELETE", r)


def demo_city():
    print("\n" + "=" * 55)
    print("  CITY CONTROLLER — CRUD Demo")
    print("=" * 55)
    ctrl = CityController()

    r = ctrl.get_all()
    print_response("GET ALL", r)

    r = ctrl.get_by_country(1)
    print_response("GET BY COUNTRY=1", r)

    r = ctrl.create("Ciudad ORM Demo", country_id=1)
    print_response("CREATE", r)
    new_id = r["data"]["city_id"] if r["status"] == "success" else None

    if new_id:
        r = ctrl.update(new_id, city_name="Ciudad ORM Actualizada")
        print_response("UPDATE", r)
        r = ctrl.delete(new_id)
        print_response("DELETE", r)


def demo_film():
    print("\n" + "=" * 55)
    print("  FILM CONTROLLER — CRUD Demo")
    print("=" * 55)
    ctrl = FilmController()

    r = ctrl.get_all(limit=10)
    print_response("GET ALL (limit=10)", r)

    r = ctrl.search("ACADEMY")
    print_response("SEARCH 'ACADEMY'", r)

    r = ctrl.create(
        title="ORM TEST FILM",
        description="Película creada por el ORM nativo",
        release_year=2024,
        rental_rate=3.50,
        rating="PG"
    )
    print_response("CREATE", r)
    new_id = r["data"]["film_id"] if r["status"] == "success" else None

    if new_id:
        r = ctrl.update(new_id, rental_rate=1.99, rating="G")
        print_response("UPDATE", r)
        r = ctrl.delete(new_id)
        print_response("DELETE", r)


def demo_customer():
    print("\n" + "=" * 55)
    print("  CUSTOMER CONTROLLER — CRUD Demo")
    print("=" * 55)
    ctrl = CustomerController()

    # READ — listar todos
    r = ctrl.get_all()
    print_response("GET ALL", r)

    # READ — por ID
    r = ctrl.get_by_id(1)
    print_response("GET BY ID=1", r)

    # CREATE
    r = ctrl.create(
        first_name="Jose",
        last_name="Berroa",
        email="jose.berroa@test.com",
        store_id=1
    )
    print_response("CREATE", r)
    new_id = r["data"]["customer_id"] if r["status"] == "success" else None

    if new_id:
        # UPDATE
        r = ctrl.update(new_id, first_name="Jose Miguel", email="josemiguel@test.com")
        print_response("UPDATE", r)

        # READ — verificar cambio
        r = ctrl.get_by_id(new_id)
        print_response("GET BY ID (post-update)", r)

        # DELETE
        r = ctrl.delete(new_id)
        print_response("DELETE", r)


if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  SAKILA ORM — Fase II Demo")
    print("  Arquitectura: MVC | DbContext + Entity + repository + Controller")
    print("=" * 55)

  #  demo_country()
    demo_city()
  #  demo_film()
  #  demo_customer()

    print("\n\n Demo completado exitosamente.\n")
