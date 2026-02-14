@echo off
echo ================================================
echo Multi Browser Launcher - EXE Build
echo ================================================
echo.

REM Check PyInstaller
python -c "import pyinstaller" 2>NUL
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Check Pillow
python -c "import PIL" 2>NUL
if errorlevel 1 (
    echo Installing Pillow...
    pip install Pillow
)

echo.
echo Creating icon...
python create_icon.py

echo.
echo Building EXE with icon...
echo.

REM Build EXE with icon
python -m PyInstaller --onefile --console --name "BrowserLauncher" --icon=browser_launcher.ico --clean browser_launcher.py

echo.
echo ================================================
echo Build Complete!
echo ================================================
echo.
echo Created: dist\BrowserLauncher.exe
echo.
echo Usage:
echo 1. Copy dist\BrowserLauncher.exe to your desired location
echo 2. Copy config.ini to the same folder
echo 3. Edit config.ini to set URLs
echo 4. Run BrowserLauncher.exe
echo.

pause
