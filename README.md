# Hotel Booking Application

A full-stack hotel booking with Django (Backend) and React (Frontend).

## Features
- Browsing Hotels and Rooms
- User Authentication (JWT)
- Room Reservation (with double-booking prevention)
- User Profile/History
- Django Admin Panel

## Prerequisites
- Python 3.8+
- Node.js & npm

## Setup & Running

1. **Backend**
   ```bash
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py runserver
   ```
   *Alternatively, run `run_backend.bat`*

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   *Alternatively, run `run_frontend.bat`*

3. **Access**
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000/api/`
   - Django Admin: `http://localhost:8000/admin/`

---

## Créer un compte Administrateur

Un administrateur permet d'accéder au panneau Django Admin (`/admin/`) pour gérer les hôtels, chambres et réservations.

### Méthode 1 — Script batch (recommandé, Windows)

Depuis la racine du projet, double-cliquez ou exécutez dans le terminal :

```bash
./create_admin.bat
```

Crée un admin avec les identifiants par défaut :
| Champ | Valeur |
|-------|--------|
| Nom d'utilisateur | `admin` |
| Email | `admin@hotel.com` |
| Mot de passe | `admin1234` |

### Méthode 2 — Identifiants personnalisés

```bash
./create_admin.bat --username monAdmin --email moi@hotel.com --password MonMotDePasse!
```

### Méthode 3 — Script Python directement

```bash
cd backend
venv\Scripts\activate
python create_admin.py
# ou avec des arguments personnalisés :
python create_admin.py --username monAdmin --email moi@hotel.com --password secret123
```

> **Note :** Si un utilisateur avec ce nom existe déjà, le script le promoit administrateur sans créer de doublon.

---

## Technology Stack
- **Backend**: Django, Django REST Framework, SimpleJWT
- **Frontend**: React, Vite, Axios, React Router Dom
