# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Přehled projektu

Školní Django projekt — systém pro správu turnajů. Umožňuje hráčům tvořit týmy a zakladatelům organizovat turnaje se zápasy.

## Závislosti

```
Django>=5.2
django-bootstrap5
bcrypt
```

## Spuštění

Projekt vyžaduje virtuální prostředí — balíčky jsou instalovány do `venv/`.

```bash
# První spuštění
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

# Další spuštění
venv\Scripts\activate
python manage.py runserver
```

```bash
# Vytvoření admin uživatele
python manage.py createsuperuser

# Vytvoření nových migrací po změně modelů
python manage.py makemigrations
python manage.py migrate
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

- Hesla jsou hashována bcryptem (`bcrypt.hashpw` při registraci, `bcrypt.checkpw` při loginu) — logika v `Tournaments/views.py`
- `django-bootstrap5` verze 26.2+ používá modul `django_bootstrap5` (v `INSTALLED_APPS` i `{% load django_bootstrap5 %}` v šablonách)
- `SECRET_KEY` je hardkódovaný v `settings.py`
- `DEBUG = True` je nastaveno natrvalo
- Autentifikace nepoužívá Django `auth` systém — session ukládá pouze ID uživatele
