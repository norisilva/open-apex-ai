@echo off
echo Instalando PyInstaller...
echo Configurando Playwright para embutir o navegador no .exe...
set PLAYWRIGHT_BROWSERS_PATH=0
python -m playwright install chromium

echo Compilando o F1 Setups Assist para Executavel (.exe)...
python -m PyInstaller --noconfirm --onedir --windowed --name "F1SetupsAssist" --add-data "data;data" --add-data "overlay;overlay" --add-data "scraper;scraper" --add-data "transformer;transformer" --icon=NONE main.py

echo Build concluido!
echo O executavel esta na pasta "dist/F1SetupsAssist/F1SetupsAssist.exe"
pause
