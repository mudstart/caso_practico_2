-- ============================================================
-- queries.sql — 10 Consultas sobre la base de datos Sakila
-- Caso Práctico 2 | Fase I
-- ============================================================

-- ----------------------------------------------------------------
-- Q1: Total de películas por categoría (ordenado de mayor a menor)
-- ----------------------------------------------------------------
SELECT
    c.name AS categoria,
    COUNT(fc.film_id) AS total_peliculas
FROM category c
JOIN film_category fc ON c.category_id = fc.category_id
GROUP BY c.name
ORDER BY total_peliculas DESC;

-- ----------------------------------------------------------------
-- Q2: Top 10 películas más rentadas
-- ----------------------------------------------------------------
SELECT
    f.title AS pelicula,
    COUNT(r.rental_id) AS total_rentas
FROM film f
JOIN inventory i   ON f.film_id    = i.film_id
JOIN rental r      ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY total_rentas DESC
LIMIT 10;

-- ----------------------------------------------------------------
-- Q3: Cantidad de ciudades por país (Top 15)
-- ----------------------------------------------------------------
SELECT
    co.country       AS pais,
    COUNT(ci.city_id) AS total_ciudades
FROM country co
JOIN city ci ON co.country_id = ci.country_id
GROUP BY co.country
ORDER BY total_ciudades DESC
LIMIT 15;

-- ----------------------------------------------------------------
-- Q4: Ingresos totales por tienda
-- ----------------------------------------------------------------
SELECT
    s.store_id,
    ci.city        AS ciudad,
    co.country     AS pais,
    SUM(p.amount)  AS ingresos_totales
FROM store s
JOIN address  a  ON s.address_id  = a.address_id
JOIN city     ci ON a.city_id     = ci.city_id
JOIN country  co ON ci.country_id = co.country_id
JOIN staff    st ON st.store_id   = s.store_id
JOIN payment  p  ON p.staff_id    = st.staff_id
GROUP BY s.store_id, ci.city, co.country
ORDER BY ingresos_totales DESC;

-- ----------------------------------------------------------------
-- Q5: Actores que aparecen en más películas (Top 10)
-- ----------------------------------------------------------------
SELECT
    CONCAT(a.first_name, ' ', a.last_name) AS actor,
    COUNT(fa.film_id) AS peliculas
FROM actor a
JOIN film_actor fa ON a.actor_id = fa.actor_id
GROUP BY a.actor_id, actor
ORDER BY peliculas DESC
LIMIT 10;

-- ----------------------------------------------------------------
-- Q6: Clientes con mayor gasto acumulado (Top 10)
-- ----------------------------------------------------------------
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS cliente,
    ci.city                                AS ciudad,
    SUM(p.amount)                          AS gasto_total
FROM customer c
JOIN payment p  ON c.customer_id = p.customer_id
JOIN address a  ON c.address_id  = a.address_id
JOIN city    ci ON a.city_id     = ci.city_id
GROUP BY c.customer_id, cliente, ci.city
ORDER BY gasto_total DESC
LIMIT 10;

-- ----------------------------------------------------------------
-- Q7: Películas disponibles en inventario por tienda y categoría
-- ----------------------------------------------------------------
SELECT
    s.store_id,
    cat.name       AS categoria,
    COUNT(i.inventory_id) AS copias_disponibles
FROM inventory i
JOIN store        s   ON i.store_id      = s.store_id
JOIN film_category fc  ON i.film_id       = fc.film_id
JOIN category     cat ON fc.category_id  = cat.category_id
GROUP BY s.store_id, cat.name
ORDER BY s.store_id, copias_disponibles DESC;

-- ----------------------------------------------------------------
-- Q8: Películas por clasificación (rating) con duración promedio
-- ----------------------------------------------------------------
SELECT
    rating,
    COUNT(*)                    AS total_peliculas,
    ROUND(AVG(length), 1)       AS duracion_promedio_min,
    MIN(length)                 AS duracion_minima,
    MAX(length)                 AS duracion_maxima
FROM film
GROUP BY rating
ORDER BY total_peliculas DESC;

-- ----------------------------------------------------------------
-- Q9: Rentas activas (sin fecha de devolución)
-- ----------------------------------------------------------------
SELECT
    CONCAT(c.first_name, ' ', c.last_name) AS cliente,
    f.title                                AS pelicula,
    r.rental_date                          AS fecha_renta,
    DATEDIFF(NOW(), r.rental_date)         AS dias_sin_devolver
FROM rental r
JOIN inventory i  ON r.inventory_id = i.inventory_id
JOIN film      f  ON i.film_id      = f.film_id
JOIN customer  c  ON r.customer_id  = c.customer_id
WHERE r.return_date IS NULL
ORDER BY dias_sin_devolver DESC;

-- ----------------------------------------------------------------
-- Q10: Idiomas disponibles y cuántas películas tienen cada idioma
-- ----------------------------------------------------------------
SELECT
    l.name          AS idioma,
    COUNT(f.film_id) AS total_peliculas
FROM language l
LEFT JOIN film f ON l.language_id = f.language_id
GROUP BY l.language_id, l.name
ORDER BY total_peliculas DESC;
