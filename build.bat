@echo off
echo Instalando PyInstaller...
echo Configurando Playwright para embutir o navegador no .exe...
set PLAYWRIGHT_BROWSERS_PATH=0
python -m playwright install chromium

for /f "delims=" %%i in ('python -c "import playwright; import os; print(os.path.join(os.path.dirname(playwright.__file__), 'driver', 'package', '.local-browsers'))"') do set P_BROWSERS=%%i

echo Compilando o F1 Setups Assist para Executavel (.exe)...
python -m PyInstaller --noconfirm --onedir --windowed --name "F1SetupsAssist" --add-data "data;data" --add-data "overlay;overlay" --add-data "scraper;scraper" --add-data "transformer;transformer" --add-data "%P_BROWSERS%;playwright\driver\package\.local-browsers" --icon=NONE main.py

echo Build concluido!
echo O executavel esta na pasta "dist/F1SetupsAssist/F1SetupsAssist.exe"
pause
