"""
Script pour créer un compte administrateur Django.
Usage:
    python create_admin.py
    python create_admin.py --username admin --email admin@hotel.com --password secret123

Variables d'environnement supportées:
    ADMIN_USERNAME  (défaut: admin)
    ADMIN_EMAIL     (défaut: admin@hotel.com)
    ADMIN_PASSWORD  (défaut: admin1234)
"""

import os
import sys
import argparse
import django

# Configurer Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.models import User

def create_admin(username, email, password):
    if User.objects.filter(username=username).exists():
        print(f"[!] Un utilisateur '{username}' existe déjà.")
        user = User.objects.get(username=username)
        if not user.is_superuser:
            user.is_staff = True
            user.is_superuser = True
            user.save()
            print(f"[✓] L'utilisateur '{username}' a été promu administrateur.")
        else:
            print(f"[✓] L'utilisateur '{username}' est déjà administrateur. Aucune modification.")
        return

    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"[✓] Administrateur créé avec succès !")
    print(f"    Nom d'utilisateur : {username}")
    print(f"    Email             : {email}")
    print(f"    Mot de passe      : {password}")
    print(f"    Interface admin   : http://localhost:8000/admin/")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Créer un compte administrateur Django")
    parser.add_argument("--username", default=os.environ.get("ADMIN_USERNAME", "admin"),
                        help="Nom d'utilisateur (défaut: admin)")
    parser.add_argument("--email", default=os.environ.get("ADMIN_EMAIL", "admin@hotel.com"),
                        help="Email (défaut: admin@hotel.com)")
    parser.add_argument("--password", default=os.environ.get("ADMIN_PASSWORD", "admin1234"),
                        help="Mot de passe (défaut: admin1234)")

    args = parser.parse_args()

    create_admin(args.username, args.email, args.password)
