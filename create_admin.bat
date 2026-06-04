@echo off
title Hotel Booking - Créer un Admin
pushd "%~dp0backend"

echo ============================================
echo   Création du compte Administrateur Django
echo ============================================
echo.



echo Utilisation des identifiants par défaut :
echo   Nom d'utilisateur : admin
echo   Email             : admin@hotel.com
echo   Mot de passe      : admin1234
echo.
echo Pour personnaliser, modifiez les variables ci-dessous ou passez des arguments :
echo   create_admin.bat --username monAdmin --email moi@hotel.com --password secret123
echo.

REM Déterminer comment lancer Python. Si le venv existe, on l'utilise.
if exist "venv\Scripts\python.exe" (
    set "PYTHON=venv\Scripts\python.exe"
    set "PY_ARGS="
) else if exist "%SystemRoot%\py.exe" (
    set "PYTHON=py"
    set "PY_ARGS=-3"
) else (
    set "PYTHON=python"
    set "PY_ARGS="
)

"%PYTHON%" %PY_ARGS% create_admin.py %*
if errorlevel 1 (
    echo.
    echo [!] Impossible de lancer le script Python. Vérifiez que Python est installé et que vous avez créé le venv dans backend.
    echo    Dans backend : python -m venv venv
    echo    puis : .\venv\Scripts\activate
    echo.
)

echo.
pause

:end
popd
