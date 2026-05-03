# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Přehled projektu

Školní Django projekt — systém pro správu turnajů. Umožňuje hráčům tvořit týmy a zakladatelům organizovat turnaje se zápasy.

## Závislosti

```
Django>=5.2
django-bootstrap5
```

Instalace:
```bash
pip install -r requirements.txt
```

## Spuštění

```bash
# Aplikuj migrace (první spuštění nebo po změně modelů)
python manage.py migrate

# Spuštění vývojového serveru
python manage.py runserver

# Vytvoření admin uživatele
python manage.py createsuperuser

# Vytvoření nových migrací po změně modelů
python manage.py makemigrations
```

Aplikace běží na `http://127.0.0.1:8000/`. Django admin je na `/admin/`.

## Architektura

Projekt má jednu Django aplikaci `Tournaments/` s function-based views.

**Dva typy uživatelů** (vlastní modely, nezávislé na Django auth):
- **Player** — registruje se, vytváří/přidává se do týmů, tým přidává do turnajů
- **Founder** — registruje se, vytváří turnaje a spravuje zápasy

**Datový model:**
```
Player ─┐
        ├── Team ─── Tournament ─── Match
Founder ─┘
```
- `Team.players` → ManyToMany → `Player`
- `Tournament.teams` → ManyToMany → `Team`
- `Tournament.founder` → ForeignKey → `Founder`
- `Match.teams` → ManyToMany → `Team`
- `Match.state` → `'ongoing'` nebo `'finished'`

**URL struktura:**
- `/playerLogin`, `/registerPlayer` — autentifikace hráče
- `/playerMainWindow/<player_id>/` — hlavní okno hráče (týmy, turnaje)
- `/founderLogin`, `/registerFounder` — autentifikace zakladatele
- `/founderMainWindow/<founder_id>/` — hlavní okno zakladatele (turnaje, zápasy)

**Šablony** jsou v `templates/` (ne uvnitř aplikace).

## Databáze

SQLite, soubor `db.sqlite3` v kořeni projektu. Migrace jsou v `Tournaments/migrations/`.

## Kontextová varování (školní projekt)

- Hesla jsou uložena v plaintextu — záměrné zjednodušení pro školní účely
- `SECRET_KEY` je hardkódovaný v `settings.py`
- `DEBUG = True` je nastaveno natrvalo
- Autentifikace nepouží Django `auth` systém — session ukládá pouze ID uživatele
