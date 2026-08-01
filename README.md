# OpenApex AI

**Open-Source AI Race Engineer & Telemetry Hub for F1 Simulations**

OpenApex AI (formerly F1 Setups Assist) is a modern, open-source tool designed for sim racers who want to elevate their gameplay. It provides intelligent tyre wear predictions, live setup overlays, and telemetry-driven accessibility adjustments for F1 24 and F1 25.

## 🚀 Features

- **Smart Tyre HUD (AI Predictor):** Real-time tyre degradation tracking with mathematical wear predictions to estimate optimal pit stop windows.
- **Live Setup Overlay:** Automatically detects the current track and displays your predefined setup directly on your screen as a transparent HUD.
- **Zero Focus Stealing:** Advanced OS-level geometry manipulation ensures that overlays appear without ever stealing focus or minimizing your game.
- **Accessibility Transformer:** Tweaks the game's hardware configuration files dynamically (XML) to provide maximum stability for controller/gamepad players.
- **Multi-language Support (i18n):** Native support for English, Portuguese, Spanish, German, Hindi, and Arabic.
- **Customizable Hotkeys:** Easily map HUD controls to your steering wheel or pedals using the built-in hotkey manager.

## 📥 Installation

**The easiest way to use OpenApex AI is by downloading the Executable:**
1. Go to the [Releases](https://github.com/norisilva/open-apex-ai/releases) page.
2. Download the latest `OpenApexAI.exe` file.
3. Place it in a folder of your choice and run it.

*Note: You may need to authorize the application in Windows Defender since the `.exe` is built via PyInstaller without a digital certificate.*

## 🔧 Running from Source

If you prefer to run the Python code directly:

1. Clone the repository:
   ```cmd
   git clone https://github.com/norisilva/open-apex-ai.git
   ```
2. Install the dependencies:
   ```cmd
   pip install -r requirements.txt
   ```
3. Run the application:
   ```cmd
   python main.py
   ```

## 🤝 Contributing

Contributions are welcome! If you have ideas for new AI telemetry modules, new games support, or UI improvements, feel free to open an issue or submit a Pull Request.

## 📄 License

This project is open-source and available under the MIT License.
