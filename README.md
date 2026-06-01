# Caso Práctico 2 — Sakila CRUD/ORM en Python

## Estructura del proyecto

```
caso_practico_2/
├── config.py                        ← Credenciales de conexión MySQL
├── test_connection.py               ← Verifica la conexión a Sakila
├── README.md
│
├── fase1/
│   ├── queries.sql                  ← 10 consultas SQL (Q1–Q10)
│   ├── unique_constraints.sql       ← ALTER TABLE + 10 consultas (Q11–Q20)
│   ├── crud_city.py                 ← CRUD city + CSV/JSON + métricas
│   ├── crud_country.py              ← CRUD country + CSV/JSON
│   ├── crud_film.py                 ← CRUD film + CSV/JSON
│   └── metrics.py                   ← Métricas: media, rango, desv, var, cov
│
├── fase2/
│   ├── __init__.py
│   ├── db_context.py                ← DbContext (Singleton, conexión MySQL)
│   ├── entities.py                  ← Entity: Country, City, Film, Customer
│   ├── models.py                    ← Model (List<Entity>) con acceso a BD
│   ├── controllers.py               ← Controller MVC por entidad
│   └── main.py                      ← Demo completo del ORM
│
└── data/                            ← CSV/JSON generados al exportar
```

## Requisitos

```bash
pip install mysql-connector-python
```

## Pasos para ejecutar

### 1. Verificar conexión
```bash
python test_connection.py
```

### 2. Ejecutar las 10 consultas SQL (Fase I)
Abrir `fase1/queries.sql` en MySQL Workbench y ejecutar.

### 3. Agregar UNIQUE constraints (Fase I - Paso 5)
Abrir `fase1/unique_constraints.sql` en MySQL Workbench y ejecutar.

### 4. Probar CRUD básico
```bash
python fase1/crud_city.py
python fase1/crud_country.py
python fase1/crud_film.py
```

### 5. Ver métricas descriptivas
```bash
python fase1/metrics.py
```

### 6. Demo ORM completo (Fase II)
```bash
python fase2/main.py
```

## Arquitectura ORM (Fase II)

```
Request
   ↓
Controller  ← orquesta la lógica
   ↓
Model (List<Entity>)  ← colección de objetos en memoria
   ↓
Entity  ← espejo de la tabla en la BD
   ↓
DbContext  ← conexión Singleton a MySQL
   ↓
MySQL Sakila
```

## Métricas implementadas (sin librerías externas)
- Media aritmética
- Rango (max - min)
- Varianza muestral
- Desviación estándar
- Covarianza
