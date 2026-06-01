# ============================================================
# metrics.py — Métricas descriptivas fundamentales sobre Sakila
# Media, Rango, Desviación, Varianza, Covarianza
# Fase I | Caso Práctico 2
# ============================================================

import mysql.connector
import math
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DB_CONFIG


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


# ── Funciones estadísticas manuales (sin librerías externas) ─

def mean(data: list) -> float:
    return sum(data) / len(data) if data else 0.0

def data_range(data: list) -> float:
    return max(data) - min(data) if data else 0.0

def variance(data: list) -> float:
    if len(data) < 2:
        return 0.0
    mu = mean(data)
    return sum((x - mu) ** 2 for x in data) / (len(data) - 1)  # varianza muestral

def std_deviation(data: list) -> float:
    return math.sqrt(variance(data))

def covariance(x: list, y: list) -> float:
    if len(x) != len(y) or len(x) < 2:
        return 0.0
    mx, my = mean(x), mean(y)
    return sum((xi - mx) * (yi - my) for xi, yi in zip(x, y)) / (len(x) - 1)

def print_stats(label: str, data: list):
    print(f"\n📊 Métricas: {label}")
    print(f"   n          = {len(data)}")
    print(f"   Media      = {mean(data):.4f}")
    print(f"   Mín        = {min(data):.4f}  |  Máx = {max(data):.4f}")
    print(f"   Rango      = {data_range(data):.4f}")
    print(f"   Varianza   = {variance(data):.4f}")
    print(f"   Desv. Est. = {std_deviation(data):.4f}")


# ── Métricas sobre películas ──────────────────────────────────

def film_metrics():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT rental_rate, length, replacement_cost FROM film")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    rental_rates       = [float(r[0]) for r in rows]
    lengths            = [int(r[1])   for r in rows]
    replacement_costs  = [float(r[2]) for r in rows]

    print_stats("Tarifa de renta (rental_rate)", rental_rates)
    print_stats("Duración de película en min (length)", lengths)
    print_stats("Costo de reposición (replacement_cost)", replacement_costs)

    cov = covariance(rental_rates, replacement_costs)
    print(f"\n🔗 Covarianza (rental_rate vs replacement_cost) = {cov:.4f}")

    cov2 = covariance(lengths, rental_rates)
    print(f"🔗 Covarianza (length vs rental_rate)           = {cov2:.4f}")


# ── Métricas sobre pagos ─────────────────────────────────────

def payment_metrics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT amount FROM payment")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    amounts = [float(r[0]) for r in rows]
    print_stats("Monto de pagos (amount)", amounts)


# ── Métricas sobre inventario ────────────────────────────────

def inventory_metrics():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT film_id, COUNT(*) AS copies
        FROM inventory
        GROUP BY film_id
    """)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    copies = [int(r[1]) for r in rows]
    print_stats("Copias por película en inventario", copies)


# ── MAIN ─────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  MÉTRICAS DESCRIPTIVAS — BASE DE DATOS SAKILA")
    print("=" * 55)

    film_metrics()
    payment_metrics()
    inventory_metrics()

    print("\n✅ Análisis completado.\n")
