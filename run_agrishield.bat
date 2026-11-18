@echo off
title AGRISHIELD Multi-Crop Enterprise Platform
echo ===================================================================
echo     AGRISHIELD MULTI-CROP ENTERPRISE CROP PATHOLOGY SUITE V2.5
echo        (Mango, Tomato, Potato, Chili Pathology & Database)
echo ===================================================================
echo [1/3] Checking Python runtime...
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    pause
    exit /b 1
)

echo [2/3] Initializing SQLite database (agrishield.db)...
python -c "import sys; sys.path.append('backend'); import db; db.init_db(); print('SQLite Database verified. Total records:', len(db.get_all_records()))"

echo [3/3] Launching AGRISHIELD Server at http://localhost:8000 ...
start "" "http://localhost:8000"
python backend/server.py
pause
