# F1 Setups Assist - Universal Setup Assistant

*[Ler em Português / Read in Portuguese (README_pt-BR.md)](README_pt-BR.md)*

A local desktop application for **F1 25** designed as a Universal Setup Assistant. The system automatically extracts the best competitive setups online and allows the player to apply **Driving Profiles** (Esports, Gamepad, or Accessibility for Focal Dystonia). It also features a floating in-game HUD that reads your live telemetry to know exactly which track you are currently racing on.

## 📦 How to Use (For Players)

**The easiest way to use the F1 Setups Assist is by downloading the Executable:**

1. Go to the **[Releases](https://github.com/norisilva/f1-setups-assist/releases)** tab of this repository.
2. Download the `F1SetupsAssist.exe` file.
3. Place it anywhere on your desktop and double-click it.
4. A beautiful Cyberpunk Control Panel will appear!

### Using the Control Panel
- **Download Setups (Baixar Setups):** Click the first button to let the system download the latest setups from the cloud (Uses F1Laps, with a fallback to SimRacingSetup in case of Cloudflare blocks).
- **Configure Profile (Configurar Perfil):** Click the Gear icon to choose your driving mode. You can use raw "Esports" setups, smooth them out for "Gamepad" players, or use the maximum "Accessibility" mode if you have motor difficulties (like Focal Dystonia).
- **In-Game HUD (Iniciar HUD):** Click to start the overlay. A transparent window will appear over your game!

## 🏎️ F1 25 Configuration

In order for the Overlay to identify which track you are racing on, the game's telemetry must be active:
1. Open F1 25
2. Go to **Settings** > **Telemetry Settings**
3. **UDP Telemetry**: On
4. **UDP Port**: `20777`
5. **UDP Send Rate**: 10Hz to 20Hz is enough (to avoid network overload)
6. **UDP Format**: `2025`

> [!CAUTION]
> **Beware of other telemetry software!**
> If you have the official F1Laps app installed on your computer, **it must be closed** before opening our HUD. The original F1Laps app monopolizes Windows port 20777, preventing the data from reaching our Assistant.

## 💻 For Developers (How to build)

If you want to modify the code and run it from Python:

1. Clone the repository
2. Install dependencies: 
```bash
pip install -r requirements.txt
playwright install chromium
```
3. Run `python main.py` to open the panel.
4. To compile the final executable yourself, simply double-click `build.bat`! (The script will use PyInstaller to package the application with embedded chromium browsers).

## Project Structure
* `scraper/`: Playwright scripts responsible for navigating, bypassing anti-bots, and extracting setups.
* `transformer/`: The "brain" of the accessibility rules and mathematical smoothing.
* `overlay/`: UDP server and Always-on-top Tkinter window.
* `data/`: Where the resulting JSON files and your personal rules (`rules.json`) are saved.
