# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Přehled projektu

Školní Django projekt — systém pro správu turnajů s Google OAuth2 autentizací. Umožňuje hráčům tvořit týmy a zakladatelům organizovat turnaje se zápasy.

## Závislosti

```
Django>=5.2
django-bootstrap5
django-allauth[google]
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

**Dva typy uživatelů** (vlastní modely rozšiřující Django auth přes Google OAuth2 přes django-allauth):
- **Player** — přihlašuje se přes Google, vytváří/přidává se do týmů, tým přidává do turnajů
- **Founder** — přihlašuje se přes Google, vytváří turnaje a spravuje zápasy

**Přístupová ochrana** pomocí dekorátorů v `Tournaments/decorators.py`:
- `@player_required` — ověří, že přihlášený uživatel má profil Player
- `@founder_required` — ověří, že přihlášený uživatel má profil Founder

Po přihlášení přes Google je uživatel přesměrován na `/role-select/`, kde si zvolí roli (Player nebo Founder), pokud ji ještě nemá.

**Datový model:**
```
auth.User ── Player ─┐
                     ├── Team ─── Tournament ─── Match
auth.User ── Founder ─┘
```
- `Player.user` → OneToOneField → `auth.User`
- `Founder.user` → OneToOneField → `auth.User`
- `Team.players` → ManyToMany → `Player`
- `Tournament.teams` → ManyToMany → `Team`
- `Tournament.founder` → ForeignKey → `Founder`
- `Match.teams` → ManyToMany → `Team`
- `Match.state` → `'ongoing'` nebo `'finished'`

**URL struktura:**
- `/accounts/google/login/` — přihlášení přes Google (django-allauth)
- `/role-select/` — výběr role po prvním přihlášení
- `/player/dashboard/` — hlavní okno hráče (týmy, turnaje)
- `/founder/dashboard/` — hlavní okno zakladatele (turnaje, zápasy)

**Šablony** jsou v `templates/` (ne uvnitř aplikace).

## Databáze

SQLite, soubor `db.sqlite3` v kořeni projektu. Migrace jsou v `Tournaments/migrations/`.

## Setup Google OAuth

### 1. Vytvoření Google Cloud Console projektu
1. Otevřít https://console.cloud.google.com
2. Vytvořit nový projekt
3. Přejít na "APIs & Services" → "OAuth consent screen" → nakonfigurovat
4. Přejít na "APIs & Services" → "Credentials" → "Create credentials" → "OAuth 2.0 Client ID"
   - Application type: Web application
   - Authorized redirect URIs: `http://127.0.0.1:8000/accounts/google/login/callback/`
5. Zkopírovat Client ID a Client Secret

### 2. Nastavení přes .env

Credentials se konfigurují v souboru `.env` v kořeni projektu:

```
GOOGLE_CLIENT_ID=...
GOOGLE_CLIENT_SECRET=...
```

`settings.py` je načítá automaticky přes `SOCIALACCOUNT_PROVIDERS['google']['APP']`.
**Admin → Social Applications není potřeba nastavovat** — konfigurace z `.env` má přednost.

> Pokud byl dříve vytvořen záznam v Admin → Social Applications, smaž ho — jinak může dojít ke konfliktu.

### 3. Testování
Otevřít `http://127.0.0.1:8000/` → kliknout "Přihlásit přes Google" → ověřit OAuth flow

## Poznámky (školní projekt)

- `django-bootstrap5` verze 26.2+ používá modul `django_bootstrap5` (v `INSTALLED_APPS` i `{% load django_bootstrap5 %}` v šablonách)
- `SECRET_KEY` je hardkódovaný v `settings.py`
- `DEBUG = True` je nastaveno natrvalo
