# 🌿 AGRISHIELD — Autonomous Crop Disease Detection & Microclimate Pathology

[![React](https://img.shields.io/badge/React-18.3-61DAFB?logo=react&logoColor=black)](https://reactjs.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![SQLite3](https://img.shields.io/badge/SQLite-3_WAL_Mode-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**AGRISHIELD** is an autonomous full-stack agricultural pathology platform designed for Indian farmers. It pairs **multi-spectral foliar computer vision** with **localized microclimate sensors** to identify crop diseases in under 6 seconds, prescribe ICAR-compliant chemical/biological remedies, calculate real-time economic risk in Indian Rupees (₹), and manage automated 4-day recovery follow-ups.

---

## 📸 Key Features

- **Multi-Crop Support**: Dedicated pathology models for **Mango 🥭**, **Tomato 🍅**, **Potato 🥔**, **Chili 🌶️**, and **Other Farm Crops 🌱**.
- **Accurate Batch Ingestion**: Requires 10–15 leaf specimens per batch to avoid single-leaf false positives.
- **Live Microclimate Telemetry**: Real-time GPS location, temperature, humidity risk scoring, and leaf wetness correlation via Open-Meteo & BigDataCloud APIs.
- **Disease & Root Cause Correlation**: Automatically matches local humidity and temperature to pathogen germination without confusing medical jargon.
- **Actionable Spray Instructions & Warnings**: Dosage, market prices (₹/L), application schedules, and high-contrast red warning boxes on what **NOT** to do.
- **Real-Time Acreage Calculator**: Interactive acreage toggles (**1 Acre, 2 Acres, 5 Acres, 10 Acres**) recalculate **Potential Money Loss (₹)**, **Projected Yield at Risk (MT)**, and **Strategy Savings** on the fly.
- **Digital Health Records (SQLite Database)**: Stores all scan reports, prescription histories, and flags 4-day-old scans with an automated **"Follow-up Required"** recovery audit modal.

---

## 📂 Project Structure

```
Agrishild New/
├── .vscode/
│   ├── extensions.json             # Recommended VS Code extensions
│   └── settings.json               # Formatting & editor preferences
├── backend/
│   ├── db.py                       # SQLite database manager (WAL mode, CRUD, schema)
│   └── server.py                   # Multi-threaded Python HTTP/REST API server
├── src/
│   ├── App.jsx                     # Modular React 18 component
│   ├── main.jsx                    # React DOM entry point
│   └── index.css                   # Tailwind CSS imports & custom styles
├── agrishield.db                   # SQLite database file with pre-seeded records
├── index.html                      # Complete standalone production single-page app
├── netlify.toml                    # Netlify deployment configuration
├── package.json                    # Node.js dependencies (React, Vite, Lucide React)
├── run_agrishield.bat              # 1-Click Windows batch launcher
├── run_agrishield.ps1              # PowerShell launch script
├── run_with_public_tunnel.bat      # 1-Click launcher with Cloudflare public link
├── tailwind.config.js              # Tailwind design tokens & font settings
├── vercel.json                     # Vercel deployment configuration
├── vite.config.js                  # Vite bundler configuration
├── .gitignore                      # Git ignore rules for clean repository
└── README.md                       # Documentation
```

---

## 💻 How to Open and Run in VS Code

### 1. Open Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File ➔ Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select the folder: `c:\Users\NILUTPAL NATH\Agrishild New`.
4. When prompted by VS Code: *"Do you trust the authors of the files in this folder?"*, click **Yes, I trust the authors**.

### 2. Recommended Extensions
When opening the folder, VS Code will prompt you to install recommended extensions (or press `Ctrl + Shift + X` and install):
- **Python** (`ms-python.python`)
- **Tailwind CSS IntelliSense** (`bradlc.vscode-tailwindcss`)
- **SQLite Viewer** (`qwtel.sqlite-viewer`) — allows clicking `agrishield.db` to view database tables directly in VS Code!
- **ES7+ React/Redux/React-Native snippets** (`dsznajder.es7-react-js-snippets`)

### 3. Run the App in VS Code Terminal
1. Open a terminal inside VS Code: Press `Ctrl + ` ` ` (tilde) or click **Terminal ➔ New Terminal**.
2. Run either of the following:

#### Option A: 1-Click Launcher (Recommended)
```cmd
.\run_agrishield.bat
```
*This starts the Python API server on port 8000 and immediately opens `http://localhost:8000` in your default browser.*

#### Option B: Direct Python Server
```powershell
python backend/server.py
```
*Then open `http://localhost:8000` in your web browser.*

#### Option C: Vite Development Server
```bash
npm install
npm run dev
```

---

## 🚀 How to Upload to GitHub

You can upload this project to GitHub using **any of the 3 methods below**:

### Method 1: Using GitHub Web Interface (Easiest & No Install Needed)

1. Open your browser and go to [github.com/new](https://github.com/new).
2. Enter a repository name, e.g., `agrishield` or `agrishield-crop-pathology`.
3. Set visibility to **Public** (or **Private**).
4. Do **NOT** check "Add a README file" (as this project already has a complete one).
5. Click **Create repository**.
6. On the empty repository page, click the link that says:
   **"uploading an existing file"**.
7. Open Windows File Explorer to `c:\Users\NILUTPAL NATH\Agrishild New`.
8. Drag and drop all the project files into the GitHub browser window (except `node_modules` if present).
9. Scroll down, type a commit message like `Initial commit: AGRISHIELD full-stack crop pathology platform`, and click **Commit changes**.

---

### Method 2: Using GitHub Desktop (Free & Easy GUI)

1. Download and install **GitHub Desktop** from [desktop.github.com](https://desktop.github.com/).
2. Open GitHub Desktop and log in with your GitHub account.
3. Click **File ➔ Add Local Repository...** (or press `Ctrl + O`).
4. Browse to: `c:\Users\NILUTPAL NATH\Agrishild New` and select it.
5. If prompted *"This directory does not appear to be a Git repository. Would you like to create a repository here?"*, click **Create a Repository**.
6. Enter repository name `agrishield`, click **Create Repository**.
7. Click the top button: **Publish repository** to push it to your GitHub account!

---

### Method 3: Using Git Command Line (CLI)

If you have Git installed (or install it via Windows PowerShell using `winget install --id Git.Git -e`):

1. Open a terminal in `c:\Users\NILUTPAL NATH\Agrishild New`:
   ```bash
   git init
   git branch -M main
   ```
2. Add and commit all files:
   ```bash
   git add .
   git commit -m "feat: complete AGRISHIELD crop pathology platform with SQLite & React"
   ```
3. Link your new GitHub repository (replace `USERNAME` and `REPO` with yours):
   ```bash
   git remote add origin https://github.com/USERNAME/agrishield.git
   ```
4. Push the code:
   ```bash
   git push -u origin main
   ```

---

## 🌐 Public Sharing & Cloud Deployment

- **Instant Public Link**: Run `run_with_public_tunnel.bat` to generate a live, secure Cloudflare tunnel URL accessible from any mobile phone or computer worldwide.
- **Vercel / Netlify**: Pre-configured with `vercel.json` and `netlify.toml` for 1-click frontend hosting.

---

## 📜 License
This project is licensed under the **MIT License**.
