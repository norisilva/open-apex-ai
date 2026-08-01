@echo off
echo Instalando PyInstaller...
echo Configurando Playwright para embutir o navegador no .exe...
set PLAYWRIGHT_BROWSERS_PATH=0
python -m playwright install chromium

for /f "delims=" %%i in ('python -c "import playwright; import os; print(os.path.join(os.path.dirname(playwright.__file__), 'driver', 'package', '.local-browsers'))"') do set P_BROWSERS=%%i

echo Limpando builds anteriores...
if exist build rd /s /q build
if exist dist rd /s /q dist
if exist OpenApexAI.spec del /q OpenApexAI.spec

echo Compilando o OpenApex AI para Executavel (.exe)...
python -m PyInstaller --clean --noconfirm --onefile --windowed --name "OpenApexAI" --add-data "data;data" --add-data "ui\overlay;ui\overlay" --add-data "core\scraper;core\scraper" --add-data "core\transformer;core\transformer" --add-data "%P_BROWSERS%;playwright\driver\package\.local-browsers" --icon=NONE main.py

echo Build concluido!
echo O executavel esta na pasta "dist/OpenApexAI.exe"
