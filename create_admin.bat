@echo off
title Hotel Booking - Créer un Admin
pushd "%~dp0backend"

echo ============================================
echo   Création du compte Administrateur Django
echo ============================================
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\Scripts\python.exe" (
    echo [ERREUR] Environnement virtuel introuvable.
    echo Veuillez d'abord exécuter run_backend.bat pour initialiser le projet.
    pause
    goto :end
)

echo Utilisation des identifiants par défaut :
echo   Nom d'utilisateur : admin
echo   Email             : admin@hotel.com
echo   Mot de passe      : admin1234
echo.
echo Pour personnaliser, modifiez les variables ci-dessous ou passez des arguments :
echo   create_admin.bat --username monAdmin --email moi@hotel.com --password secret123
echo.

REM Passer les arguments éventuels au script Python
venv\Scripts\python.exe create_admin.py %*

echo.
pause

:end
popd
