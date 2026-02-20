# 4114_Database
# State-Based Wildlife Application (MySQL)

## Overview
A MySQL-backed wildlife management app that supports CRUD operations across multiple related entities
(e.g., biome/habitat/animal/plant/researcher/admin) with a Python desktop UI.

## Tech Stack
- Python, mysql-connector-python
- MySQL
- Tkinter / CustomTkinter (UI)

## Features
- Relational schema with PK/FK relationships
- CRUD: insert/update/delete/search across tables
- Detail view resolves foreign keys to human-readable fields
- Basic statistics / reporting (if applicable)

## How to Run
1. Create MySQL database and tables (include schema.sql if you have it)
2. Update DB credentials in code (host/user/password/database)
3. Install dependencies: `pip install -r requirements.txt`
4. Run: `python database.py` (or your entry file)

## My Contribution
- Designed ER model + implemented MySQL schema
- Implemented CRUD queries and validation
- Built UI pages and FK lookup logic
