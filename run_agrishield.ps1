# AGRISHIELD Multi-Crop Enterprise Platform Launcher
Write-Host "===================================================================" -ForegroundColor DarkTeal
Write-Host "    AGRISHIELD MULTI-CROP ENTERPRISE CROP PATHOLOGY SUITE V2.5     " -ForegroundColor White
Write-Host "        (Mango, Tomato, Potato, Chili Pathology & Database)        " -ForegroundColor Green
Write-Host "===================================================================" -ForegroundColor DarkTeal

Write-Host "`n[1/3] Verifying Python Runtime..." -ForegroundColor Yellow
$pyVer = python --version
Write-Host "Detected: $pyVer" -ForegroundColor Green

Write-Host "`n[2/3] Initializing SQLite Database (agrishield.db)..." -ForegroundColor Yellow
python -c "import sys; sys.path.append('backend'); import db; db.init_db(); print('SQLite Database verified. Total records:', len(db.get_all_records()))"

Write-Host "`n[3/3] Starting AGRISHIELD Server on http://localhost:8000 ..." -ForegroundColor Yellow
Start-Process "http://localhost:8000"
python backend/server.py
