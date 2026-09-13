@echo off
chcp 65001 >nul
echo.
echo ================================
echo GENERADOR DE TEKAMS FIREBASE
echo ================================
echo.

cd /d "%~dp0"

if exist "generar_tekams_completo.py" (
    echo Ejecutando generador...
    echo.
    python generar_tekams_completo.py
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo ================================
        echo EXITO!
        echo ================================
        echo.
        echo El archivo "tekams_firebase.html" ha sido generado
        echo en: %~dp0tekams_firebase.html
        echo.
        echo Abre el archivo en tu navegador para usarlo.
        echo.
        pause
    ) else (
        echo.
        echo ERROR: Fallo en la generación
        pause
        exit /b 1
    )
) else (
    echo ERROR: No se encontró generar_tekams_completo.py
    echo.
    echo Asegúrate de que ambos archivos están en la misma carpeta:
    echo - generar_tekams_completo.py
    echo - GENERAR_TEKAMS.bat
    echo.
    pause
    exit /b 1
)
