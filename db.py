"""
AGRISHIELD Enterprise Multi-Crop Database Engine
Provides SQLite database initialization, automated schema migrations,
and ACID-compliant CRUD operations for multi-crop pathology health records.
Supports Mango (Mangifera indica), Tomato (Solanum lycopersicum), 
Potato (Solanum tuberosum), and Chili (Capsicum annuum).
"""

import os
import sqlite3
import json
from datetime import datetime, timedelta

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "agrishield.db")

def get_connection():
    """Establish and return an optimized SQLite database connection."""
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn

def init_db():
    """Initialize database tables and seed multi-crop records."""
    conn = get_connection()
    with conn:
        cursor = conn.cursor()
        
        # Health records ledger table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_records (
                id TEXT PRIMARY KEY,
                crop_code TEXT NOT NULL DEFAULT 'mango',
                date TEXT NOT NULL,
                formatted_date TEXT,
                formatted_time TEXT,
                crop TEXT,
                plot TEXT,
                disease TEXT,
                pathogen TEXT,
                severity TEXT,
                confidence TEXT,
                location TEXT,
                temperature TEXT,
                humidity TEXT,
                weather_condition TEXT,
                status TEXT,
                prescription TEXT,
                batch_count INTEGER DEFAULT 12,
                acreage INTEGER DEFAULT 1,
                loss_estimate TEXT,
                notes TEXT,
                recovery_uploaded INTEGER DEFAULT 0,
                recovery_notes TEXT,
                recovery_date TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        # Full diagnostic batch runs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS diagnostic_batches (
                id TEXT PRIMARY KEY,
                record_id TEXT,
                crop_code TEXT,
                disease_name TEXT,
                botanical_pathogen TEXT,
                severity_grade TEXT,
                severity_index TEXT,
                confidence_rate TEXT,
                environmental_root_cause TEXT,
                treatment_plan_json TEXT,
                economic_impact_json TEXT,
                weather_snapshot_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (record_id) REFERENCES health_records (id) ON DELETE CASCADE
            );
        """)

        # Check existing count; if empty or missing mango seed, re-seed
        cursor.execute("SELECT COUNT(*) AS cnt FROM health_records WHERE crop_code = 'mango';")
        row = cursor.fetchone()
        if not row or row['cnt'] == 0:
            seed_initial_records(cursor)

    conn.close()

def seed_initial_records(cursor=None):
    """Seed initial records with a guaranteed 4-day-old MANGO record for follow-up alert."""
    should_close = False
    if cursor is None:
        conn = get_connection()
        cursor = conn.cursor()
        should_close = True

    now = datetime.now()
    four_days_ago = now - timedelta(days=4)
    seven_days_ago = now - timedelta(days=7)
    eleven_days_ago = now - timedelta(days=11)
    sixteen_days_ago = now - timedelta(days=16)

    records = [
        # 1. MANGO (4 Days Ago - Follow-up Required milestone!)
        (
            'REC-2026-0894',
            'mango',
            four_days_ago.isoformat(),
            four_days_ago.strftime('%d %b %Y'),
            four_days_ago.strftime('%I:%M %p'),
            'Mango (Mangifera indica - Alphonso)',
            'Ratnagiri Orchard Block 2-B • Konkan Belt',
            'Mango Anthracnose',
            'Colletotrichum gloeosporioides',
            'Stage 3 (Severe Foliar & Panicle Blight)',
            '98.1%',
            'Ratnagiri, Maharashtra (Konkan Agro-Zone)',
            '29.2°C',
            '88% - Severe Humidity',
            'Pre-Monsoon Intermittent Drizzle',
            'Active Treatment',
            'Azoxystrobin 18.2% + Difenoconazole 11.4% SC',
            12,
            2,
            '₹90,000 (2 Acres)',
            'Orchard spray administered on Day 1 dawn. Irregular dark brown foliar lesions and panicle withering detected on new vegetative flush.',
            0,
            None,
            None
        ),
        # 2. POTATO (7 Days Ago - Resolved)
        (
            'REC-2026-0841',
            'potato',
            seven_days_ago.isoformat(),
            seven_days_ago.strftime('%d %b %Y'),
            seven_days_ago.strftime('%I:%M %p'),
            'Potato (Solanum tuberosum - Kufri Jyoti)',
            'Nashik Sector 3A • Tuber Zone',
            'Late Blight',
            'Phytophthora infestans',
            'Stage 2 (Moderate)',
            '95.8%',
            'Nashik, Maharashtra',
            '24.1°C',
            '91% (Extreme)',
            'Continuous Rain & Dense Fog',
            'Resolved',
            'Dimethomorph 50% WP + Metalaxyl 8% SC',
            14,
            1,
            '₹28,000 (1 Acre)',
            'Foliar fungicide application successful. Spore regeneration arrested across tuber rows.',
            1,
            'Canopy recovered completely at Day 6 audit.',
            (now - timedelta(days=2)).strftime('%d %b %Y')
        ),
        # 3. TOMATO (11 Days Ago - Resolved)
        (
            'REC-2026-0792',
            'tomato',
            eleven_days_ago.isoformat(),
            eleven_days_ago.strftime('%d %b %Y'),
            eleven_days_ago.strftime('%I:%M %p'),
            'Tomato (Solanum lycopersicum - Arka Rakshak)',
            'Pune Field Plot 4-B • North Terrace',
            'Early Blight',
            'Alternaria solani',
            'Stage 3 (Severe Concentric Target Spot)',
            '97.4%',
            'Pune, Maharashtra',
            '27.4°C',
            '85% (High)',
            'Overcast with Drizzle',
            'Resolved',
            'Mancozeb 75% WP + Azoxystrobin',
            12,
            1,
            '₹15,000 (1 Acre)',
            'Target lesions treated with systemic copper rotation spray.',
            1,
            'Foliar necrosis stabilized; healthy shoots emerging.',
            (now - timedelta(days=5)).strftime('%d %b %Y')
        ),
        # 4. CHILI (16 Days Ago - Resolved)
        (
            'REC-2026-0720',
            'chili',
            sixteen_days_ago.isoformat(),
            sixteen_days_ago.strftime('%d %b %Y'),
            sixteen_days_ago.strftime('%I:%M %p'),
            'Chili (Capsicum annuum - G4)',
            'Kolhapur Commercial Block #1',
            'Chili Anthracnose & Dieback',
            'Colletotrichum capsici',
            'Stage 1 (Early Inception)',
            '94.2%',
            'Kolhapur, Maharashtra',
            '28.6°C',
            '82% (Elevated)',
            'Warm Afternoon Showers',
            'Resolved',
            'Copper Oxychloride 50% WP + Streptomycin',
            10,
            1,
            '₹18,000 (1 Acre)',
            'Curative localized barrier spray halted twig dieback.',
            1,
            'Post-treatment fruit set healthy.',
            (now - timedelta(days=9)).strftime('%d %b %Y')
        )
    ]

    cursor.executemany("""
        INSERT OR REPLACE INTO health_records (
            id, crop_code, date, formatted_date, formatted_time, crop, plot,
            disease, pathogen, severity, confidence, location,
            temperature, humidity, weather_condition, status,
            prescription, batch_count, acreage, loss_estimate, notes,
            recovery_uploaded, recovery_notes, recovery_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)

    if should_close:
        cursor.connection.commit()
        cursor.connection.close()

def get_all_records(search="", status="", crop=""):
    """Query all records with optional search, crop, and status filtering."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM health_records WHERE 1=1"
    params = []

    if search:
        search_term = f"%{search.lower()}%"
        query += " AND (LOWER(disease) LIKE ? OR LOWER(crop) LIKE ? OR LOWER(plot) LIKE ? OR LOWER(id) LIKE ?)"
        params.extend([search_term, search_term, search_term, search_term])

    if crop and crop != 'ALL':
        query += " AND LOWER(crop_code) = ?"
        params.append(crop.lower())

    if status and status != 'ALL':
        if status == 'RESOLVED':
            query += " AND status = 'Resolved'"
        elif status == 'ACTIVE':
            query += " AND status = 'Active Treatment'"

    query += " ORDER BY date DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()

    results = []
    now = datetime.now()
    for row in rows:
        item = dict(row)
        try:
            record_date = datetime.fromisoformat(item['date'].replace('Z', ''))
            days_ago = (now - record_date).days
        except Exception:
            days_ago = 0
            
        item['days_ago'] = days_ago
        # 3 to 5 days old rule: triggers flashing amber badge if not resolved
        item['is_follow_up_due'] = (3 <= days_ago <= 5 and item['status'] != 'Resolved')
        results.append(item)

    conn.close()
    return results

def get_record_by_id(record_id):
    """Fetch single health record by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM health_records WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def insert_record(data):
    """Insert a new diagnostic health record committed by user."""
    conn = get_connection()
    cursor = conn.cursor()
    
    now = datetime.now()
    record_id = data.get('id') or f"REC-2026-{int(now.timestamp()) % 10000:04d}"
    iso_date = data.get('date') or now.isoformat()
    formatted_date = data.get('formatted_date') or now.strftime('%d %b %Y')
    formatted_time = data.get('formatted_time') or now.strftime('%I:%M %p')

    crop_code = (data.get('crop_code') or 'mango').lower()

    cursor.execute("""
        INSERT INTO health_records (
            id, crop_code, date, formatted_date, formatted_time, crop, plot,
            disease, pathogen, severity, confidence, location,
            temperature, humidity, weather_condition, status,
            prescription, batch_count, acreage, loss_estimate, notes,
            recovery_uploaded, recovery_notes, recovery_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record_id,
        crop_code,
        iso_date,
        formatted_date,
        formatted_time,
        data.get('crop', 'Mango (Mangifera indica)'),
        data.get('plot', 'Ratnagiri Orchard Block 2-B'),
        data.get('disease', 'Mango Anthracnose'),
        data.get('pathogen', 'Colletotrichum gloeosporioides'),
        data.get('severity', 'Stage 3 (Severe)'),
        data.get('confidence', '98.4%'),
        data.get('location', 'Ratnagiri, Maharashtra (Konkan Agro-Zone)'),
        data.get('temperature', '29.2°C'),
        data.get('humidity', '88% (High)'),
        data.get('weather_condition', 'Pre-Monsoon Intermittent Drizzle'),
        data.get('status', 'Active Treatment'),
        data.get('prescription', 'Azoxystrobin 18.2% + Difenoconazole 11.4% SC'),
        data.get('batch_count', 12),
        data.get('acreage', 1),
        data.get('loss_estimate', '₹45,000 / Acre'),
        data.get('notes', ''),
        data.get('recovery_uploaded', 0),
        data.get('recovery_notes', None),
        data.get('recovery_date', None)
    ))
    conn.commit()
    conn.close()
    return get_record_by_id(record_id)

def update_recovery(record_id, efficacy='remission', notes='', photo_count=1):
    """Update record after post-treatment recovery audit upload."""
    conn = get_connection()
    cursor = conn.cursor()
    
    new_status = 'Resolved' if efficacy == 'remission' else 'In Observation'
    recovery_date = datetime.now().strftime('%d %b %Y')
    recovery_notes = notes or f"Recovery photo inspection batch ({photo_count} photos) confirmed. Necrotic lesions arrested; active foliar regeneration."

    cursor.execute("""
        UPDATE health_records
        SET status = ?,
            recovery_uploaded = 1,
            recovery_notes = ?,
            recovery_date = ?
        WHERE id = ?
    """, (new_status, recovery_notes, recovery_date, record_id))

    conn.commit()
    conn.close()
    return get_record_by_id(record_id)

def delete_record(record_id):
    """Delete a health record by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM health_records WHERE id = ?", (record_id,))
    conn.commit()
    rows_affected = cursor.rowcount
    conn.close()
    return rows_affected > 0

init_db()
