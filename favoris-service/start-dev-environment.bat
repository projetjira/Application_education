@echo off
echo ===== Démarrage de l'environnement de développement pour le service de favoris =====

echo.
echo 1. Lancement des services Docker (MongoDB et Redis)...
docker-compose up -d
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Impossible de démarrer les services Docker.
    pause
    exit /b 1
)

echo.
echo 2. Compilation du service avec Maven...
call mvnw.cmd clean install -DskipTests
if %ERRORLEVEL% NEQ 0 (
    echo ERREUR: Échec de la compilation Maven.
    pause
    exit /b 1
)

echo.
echo 3. Démarrage du service de favoris...
echo Appuyez sur Ctrl+C pour arrêter le service.
call mvnw.cmd spring-boot:run

echo.
echo ===== Arrêt des services Docker =====
docker-compose down

echo.
echo Environnement de développement arrêté.
pause
