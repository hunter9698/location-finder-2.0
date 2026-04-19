# Location Finder 2.0: Cyber-Style Live Tracking

A professional-grade, ethical geolocation demonstration tool specifically designed for Kali Linux and cybersecurity education.

## 🛠️ Redesigned for Kali Linux
This version has been overhauled with a **Cyberpunk / CRT Terminal** aesthetic and advanced tracking features.

## ⚖️ Ethical Usage & Transparency
**This tool is strictly for educational purposes and authorized penetration testing demonstrations.**
- **NGO Verification Theme**: Rebranded as an NGO support portal to demonstrate how location data is collected in social assistance contexts.
- **Explicit Consent**: Requires a user to click "Verify & Proceed".
- **Live Tracking**: Continuous coordinate streaming (5s interval) once consent is granted.

## 🚀 Key Features
- **Cyber Style UI**: High-impact neon aesthetics with CRT scanline effects and noise filters.
- **Real-Time Live Tracking**: Uses `watchPosition` for continuous, throttled updates (Default: 5s).
- **Auto-Tunneling**: Integrated `ngrok` support with custom domain flags.
- **Auto-Browser Launch**: Automatically opens the generated link in your default browser.
- **Terminal UX**: Colorful, structured CLI output with `[LIVE]` and `[DATA]` labeling.

## 🛠️ Installation (Kali Linux)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hunter9698/location-finder-2.0.git
   cd location-finder-2.0
   ```

2. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up Ngrok (One-time):**
   ```bash
   ngrok config add-authtoken <your_token>
   ```

## 💻 Usage

**Start with automatic Ngrok tunnel and Custom Domain:**
```bash
python3 main.py --ngrok --domain your-domain.ngrok-free.dev
```

**Standard start (Local only):**
```bash
python3 main.py
```

## 📁 Project Structure
- `main.py`: CLI entry point (Multi-threaded browser & Ngrok management).
- `server.py`: Flask backend with structured JSON logging and console reporting.
- `templates/`: NGO-branded Cyberpunk HTML templates.
- `static/`: Neon CSS, Glitch assets, and Live-Tracking JS.
- `logs/`: Directory for `capture.json` tracking files.

## ⚠️ Requirements
- Python 3.8+
- Flask, pyngrok, colorama, user-agents, flask-cors
