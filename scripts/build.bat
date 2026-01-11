@echo off
echo ========================================
echo Building DeviceManager Application
echo ========================================
echo.

cd /d "%~dp0\.."

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install -r requirement.txt

echo.
echo Building executable with PyInstaller...
pyinstaller --onefile --windowed --name=DeviceManager .\src\main.py

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo Executable location: dist\DeviceManager.exe
echo ========================================
pause
