-- ============================================================
-- unique_constraints.sql — Mejora de integridad en Sakila
-- Agrega UNIQUE constraints para evitar datos duplicados
-- Fase I | Caso Práctico 2
-- ============================================================

-- NOTA: Ejecutar en MySQL Workbench o desde línea de comandos
-- mysql -u root -p sakila < unique_constraints.sql

-- ----------------------------------------------------------------
-- 1. COUNTRY — nombre de país único
-- ----------------------------------------------------------------
-- Verificar duplicados primero
SELECT country, COUNT(*) AS n FROM country GROUP BY country HAVING n > 1;

-- Agregar constraint
ALTER TABLE country
    ADD CONSTRAINT uq_country_name UNIQUE (country);

-- ----------------------------------------------------------------
-- 2. CITY — combinación ciudad + país única (no puede haber
--    dos ciudades con el mismo nombre en el mismo país)
-- ----------------------------------------------------------------
SELECT city, country_id, COUNT(*) AS n
FROM city
GROUP BY city, country_id
HAVING n > 1;

ALTER TABLE city
    ADD CONSTRAINT uq_city_country UNIQUE (city, country_id);

-- ----------------------------------------------------------------
-- 3. FILM — título único por año de lanzamiento
-- ----------------------------------------------------------------
SELECT title, release_year, COUNT(*) AS n
FROM film
GROUP BY title, release_year
HAVING n > 1;

ALTER TABLE film
    ADD CONSTRAINT uq_film_title_year UNIQUE (title, release_year);

-- ----------------------------------------------------------------
-- 4. LANGUAGE — nombre de idioma único
-- ----------------------------------------------------------------
ALTER TABLE language
    ADD CONSTRAINT uq_language_name UNIQUE (name);

-- ----------------------------------------------------------------
-- 5. CATEGORY — nombre de categoría único
-- ----------------------------------------------------------------
ALTER TABLE category
    ADD CONSTRAINT uq_category_name UNIQUE (name);

-- ----------------------------------------------------------------
-- 6. ACTOR — combinación nombre+apellido única
-- ----------------------------------------------------------------
SELECT first_name, last_name, COUNT(*) AS n
FROM actor
GROUP BY first_name, last_name
HAVING n > 1;

ALTER TABLE actor
    ADD CONSTRAINT uq_actor_fullname UNIQUE (first_name, last_name);

-- ----------------------------------------------------------------
-- Verificar todos los constraints creados
-- ----------------------------------------------------------------
SELECT
    TABLE_NAME,
    CONSTRAINT_NAME,
    CONSTRAINT_TYPE
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'sakila'
  AND CONSTRAINT_TYPE = 'UNIQUE'
ORDER BY TABLE_NAME;


-- ============================================================
-- 10 CONSULTAS ADICIONALES (post constraints)
-- ============================================================

-- Q11: Verificar que no hay países duplicados
SELECT country, COUNT(*) AS n
FROM country
GROUP BY country
ORDER BY n DESC
LIMIT 5;

-- Q12: Ciudades duplicadas en distintos países (válido)
SELECT ci.city, COUNT(DISTINCT ci.country_id) AS num_paises
FROM city ci
GROUP BY ci.city
HAVING num_paises > 1
ORDER BY num_paises DESC
LIMIT 10;

-- Q13: Películas con el mismo título en distintos años
SELECT title, GROUP_CONCAT(release_year ORDER BY release_year) AS years
FROM film
GROUP BY title
HAVING COUNT(*) > 1;

-- Q14: Resumen de constraints UNIQUE por tabla
SELECT TABLE_NAME, COUNT(*) AS unique_constraints
FROM information_schema.TABLE_CONSTRAINTS
WHERE TABLE_SCHEMA = 'sakila'
  AND CONSTRAINT_TYPE = 'UNIQUE'
GROUP BY TABLE_NAME
ORDER BY TABLE_NAME;

-- Q15: Actores con nombres completos únicos vs. repetidos
SELECT first_name, last_name, COUNT(*) AS ocurrencias
FROM actor
GROUP BY first_name, last_name
ORDER BY ocurrencias DESC
LIMIT 10;

-- Q16: Top 5 categorías con mayor tarifa de renta promedio
SELECT cat.name AS categoria, ROUND(AVG(f.rental_rate), 2) AS tarifa_promedio
FROM film f
JOIN film_category fc ON f.film_id = fc.film_id
JOIN category cat     ON fc.category_id = cat.category_id
GROUP BY cat.name
ORDER BY tarifa_promedio DESC
LIMIT 5;

-- Q17: Clientes sin rentas en los últimos 3 meses (simulado con fecha max)
SELECT c.customer_id,
       CONCAT(c.first_name,' ',c.last_name) AS cliente,
       MAX(r.rental_date) AS ultima_renta
FROM customer c
LEFT JOIN rental r ON c.customer_id = r.customer_id
GROUP BY c.customer_id, cliente
HAVING ultima_renta < DATE_SUB((SELECT MAX(rental_date) FROM rental), INTERVAL 90 DAY)
   OR ultima_renta IS NULL
ORDER BY ultima_renta
LIMIT 10;

-- Q18: Películas sin inventario registrado
SELECT f.film_id, f.title
FROM film f
LEFT JOIN inventory i ON f.film_id = i.film_id
WHERE i.inventory_id IS NULL
ORDER BY f.title;

-- Q19: Promedio de días entre renta y devolución por categoría
SELECT cat.name AS categoria,
       ROUND(AVG(DATEDIFF(r.return_date, r.rental_date)), 1) AS dias_promedio_renta
FROM rental r
JOIN inventory i    ON r.inventory_id = i.inventory_id
JOIN film_category fc ON i.film_id    = fc.film_id
JOIN category cat   ON fc.category_id = cat.category_id
WHERE r.return_date IS NOT NULL
GROUP BY cat.name
ORDER BY dias_promedio_renta DESC;

-- Q20: Empleados (staff) y total de rentas procesadas
SELECT
    CONCAT(s.first_name,' ',s.last_name) AS empleado,
    s.store_id,
    COUNT(r.rental_id) AS rentas_procesadas,
    ROUND(SUM(p.amount), 2) AS ingresos_gestionados
FROM staff s
JOIN rental  r ON s.staff_id = r.staff_id
JOIN payment p ON r.rental_id = p.rental_id
GROUP BY s.staff_id, empleado, s.store_id
ORDER BY ingresos_gestionados DESC;
