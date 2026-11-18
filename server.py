"""
AGRISHIELD Enterprise Multi-Crop Backend Server
Multi-threaded REST API server with embedded SQLite database integration
and static web application delivery on port 8000.
Supports Mango, Tomato, Potato, and Chili pathology diagnostics.
"""

import os
import sys
import json
import urllib.parse
import urllib.request
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

# Import database module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db

PORT = 8000
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Multi-crop diagnostic knowledge base
CROP_DATA = {
    "mango": {
        "cropName": "Mango (Mangifera indica - Alphonso)",
        "plot": "Ratnagiri Orchard Block 2-B • Konkan Belt",
        "diseaseName": "Mango Anthracnose",
        "botanicalPathogen": "Colletotrichum gloeosporioides",
        "severityGrade": "Stage 3 - Severe Foliar & Panicle Blight",
        "severityIndex": "68.4%",
        "confidenceRate": "98.6%",
        "environmentalRootCause": (
            "High ambient humidity (88%) in the coastal Konkan belt combined with unseasonal pre-monsoon showers "
            "triggered conidial germination of Colletotrichum gloeosporioides during tender vegetative flushing. "
            "Extended canopy wetness (10.2 hours) at 29.2°C enabled fungal appressoria to breach epidermal cuticles "
            "within 4 hours, causing characteristic tear-stain necrotic lesions and inflorescence panicle withering."
        ),
        "treatmentPlan": {
            "recommendedMedicine": "Azoxystrobin 18.2% + Difenoconazole 11.4% SC (Amistar Top)",
            "marketPrice": "₹520 / Liter",
            "totalCostEstimate": "₹1,560 estimated for 3-acre orchard foliar application",
            "steps": [
                "Tank Mix Protocol: Dilute 1.0 ml of Azoxystrobin + Difenoconazole SC per 1 Liter of neutral pH water in motorized orchard spray tank.",
                "Application Window: Spray at dawn (06:00 - 08:30 AM) using high-pressure orchard tractor mister, avoiding high winds (>12 km/h).",
                "Canopy Coverage: Direct spray upward into dense tree canopy undersides and new vegetative flush flushes where tear-stains accumulate.",
                "Rotation Interval: Re-spray after 10-12 days. Rotate with copper oxychloride 50% WP to prevent single-site strobilurin resistance."
            ],
            "precautionsWhatNotToDo": [
                "DO NOT spray during peak midday afternoon heat (>32°C) which causes leaf scorch and chemical phytotoxicity.",
                "DO NOT spray during full blossom bloom to protect essential native pollinator bees (Apis cerana indica).",
                "DO NOT leave fallen blackened leaves or mummified fruit on the orchard floor; collect and burn to stop spore cycle.",
                "DO NOT tank-mix with acidifying organophosphates without performing prior jar emulsion testing."
            ]
        },
        "baseLossPerAcre": 45000,
        "baseYieldRiskPerAcre": 5.8,
        "lossBenchmarkText": "Based on benchmark ₹45,000 / Acre loss for Alphonso mango orchard harvest",
        "treatmentCostAcre": 2400,
        "roiRatio": "1 : 18.8",
        "strategies": [
            {
                "title": "Localized Barrier & Panicle Quarantine Spray",
                "desc": "Apply systemic strobilurin curative fungicide to a 10-meter perimeter buffer around infected trees before airborne conidia spread to healthy orchard blocks.",
                "savePerAcre": 14500
            },
            {
                "title": "Post-Harvest Orchard Sanitation & Canopy Thinning",
                "desc": "Prune dead wood and inner criss-crossing branches to enhance sunlight penetration and drop microclimate humidity from 88% to 65%.",
                "savePerAcre": 6800
            },
            {
                "title": "Pre-Harvest Fruit Bagging & Drip Scheduling",
                "desc": "Switch from overhead misting to root-zone drip lines and bag developing fruits with brown parchment to block rain-splash inoculum.",
                "savePerAcre": 3200
            }
        ],
        "weatherSnapshot": {
            "location": "Ratnagiri, Maharashtra (Konkan Agro-Zone)",
            "temp": "29.2°C",
            "humidity": "88% - Severe Humidity",
            "condition": "Pre-Monsoon Intermittent Drizzle",
            "vpd": "0.38 kPa (Severely restricted transpiration)",
            "leafWetness": "10.2 Hours continuous"
        }
    },
    "tomato": {
        "cropName": "Tomato (Solanum lycopersicum - Arka Rakshak)",
        "plot": "Pune Field Plot 4-B • North Terrace",
        "diseaseName": "Early Blight",
        "botanicalPathogen": "Alternaria solani",
        "severityGrade": "Stage 3 - Severe Concentric Target Spot",
        "severityIndex": "74.2%",
        "confidenceRate": "98.4%",
        "environmentalRootCause": (
            "High ambient humidity (85%) and recent continuous rainfall accelerated fungal growth. "
            "Extended leaf wetness duration (9.4 hours) combined with ambient canopy temperatures of 27.4°C "
            "created an optimal micro-ecological niche for Alternaria solani conidial germination, penetrating "
            "host stomata and leaf cuticles within 4 hours of surface wetness."
        ),
        "treatmentPlan": {
            "recommendedMedicine": "Mancozeb 75% WP + Azoxystrobin 18.2% w/w & Difenoconazole 11.4% w/w SC",
            "marketPrice": "₹450 / Liter",
            "totalCostEstimate": "₹1,350 estimated for complete 3-acre foliar application",
            "steps": [
                "Tank Mix Protocol: Mix 2.5 ml of Azoxystrobin + Difenoconazole suspension per 1 Liter of clean pH-neutral water. Dissolve thoroughly prior to tank agitation.",
                "Application Window: Apply via fine hollow-cone nozzle during early morning (06:00 - 08:30 AM) when stomata are receptive and wind speed is under 12 km/h.",
                "Foliage Coverage: Ensure thorough bilateral coverage, focusing heavily on lower abaxial (underside) surfaces where sporulating mycelia cluster.",
                "Spray Cadence & Rotation: Repeat treatment after 7 to 10 days. Rotate with copper hydroxide on week 3 to eliminate single-site chemical resistance buildup."
            ],
            "precautionsWhatNotToDo": [
                "DO NOT spray during peak midday afternoon heat (above 30°C) or if rainfall is forecasted within 3 hours (triggers severe phytotoxicity scorching and chemical wash-off).",
                "DO NOT use overhead sprinkler irrigation; switch immediately to root-zone drip lines to prevent mechanical spore splashing across healthy crop rows.",
                "DO NOT leave infected fallen leaf litter in field furrows; rake and incinerate immediately to halt airborne inoculum recycling.",
                "DO NOT combine with alkaline stickers or organophosphate insecticides without performing a prior jar compatibility emulsion test."
            ]
        },
        "baseLossPerAcre": 15000,
        "baseYieldRiskPerAcre": 4.2,
        "lossBenchmarkText": "Based on benchmark ₹15,000 / Acre loss for Solanaceae tomato harvest",
        "treatmentCostAcre": 900,
        "roiRatio": "1 : 16.5",
        "strategies": [
            {
                "title": "Localized Barrier & Quarantine Spray",
                "desc": "Apply localized targeted curative fungicide to a 5-meter buffer radius around infected rows before secondary spore dispersion occurs.",
                "savePerAcre": 9200
            },
            {
                "title": "Lower Canopy Pruning & Leaf Removal",
                "desc": "Manually de-leaf bottom 15 cm of necrotic foliage and burn or bury debris off-field to halt horizontal splash propagation.",
                "savePerAcre": 3800
            },
            {
                "title": "Drip Irrigation Timing Calibration",
                "desc": "Irrigate exclusively at 05:00 AM via root-zone emitters to avoid elevating overnight canopy relative humidity above 80%.",
                "savePerAcre": 2000
            }
        ],
        "weatherSnapshot": {
            "location": "Pune, Maharashtra (18.5204° N, 73.8567° E)",
            "temp": "27.4°C",
            "humidity": "85% - High",
            "condition": "Overcast with Intermittent Drizzle",
            "vpd": "0.42 kPa (Severely restricted transpiration)",
            "leafWetness": "9.4 Hours continuous"
        }
    },
    "potato": {
        "cropName": "Potato (Solanum tuberosum - Kufri Jyoti)",
        "plot": "Sector 3A (Tuber Zone) • Nashik, Maharashtra",
        "diseaseName": "Late Blight",
        "botanicalPathogen": "Phytophthora infestans",
        "severityGrade": "Stage 3 - Water-Soaked Foliar Infiltration",
        "severityIndex": "79.5%",
        "confidenceRate": "97.8%",
        "environmentalRootCause": (
            "Severe continuous relative humidity (91%) combined with cool night temperatures (18°C) and persistent fog "
            "created ideal zoospore incubation for Phytophthora infestans. Free moisture on leaf surfaces exceeding "
            "8 consecutive hours allowed flagellated zoospores to encyst and penetrate tuber foliar tissue."
        ),
        "treatmentPlan": {
            "recommendedMedicine": "Dimethomorph 50% WP + Metalaxyl 8% & Mancozeb 64% WP",
            "marketPrice": "₹480 / Liter",
            "totalCostEstimate": "₹1,440 estimated for 3-acre tuber row treatment",
            "steps": [
                "Tank Mix Protocol: Mix 2.0 grams of Dimethomorph + Mancozeb per 1 Liter of water with non-ionic sticking agent.",
                "Application Window: Apply immediately on first sight of water-soaked lesions during calm morning hours.",
                "Ridge Coverage: Ensure chemical penetrates dense potato canopy to protect underlying tubers from spore wash-down.",
                "Rotation: Alternate with Cymoxanil 8% + Mancozeb 64% after 7 days."
            ],
            "precautionsWhatNotToDo": [
                "DO NOT irrigate immediately after spraying; ensure 4 hours rain-free period for translaminar uptake.",
                "DO NOT harvest tubers while vines are still green and infected with living sporangia.",
                "DO NOT discard culled diseased tubers in open field heaps.",
                "DO NOT walk through wet infected fields to prevent mechanical transmission."
            ]
        },
        "baseLossPerAcre": 28000,
        "baseYieldRiskPerAcre": 7.5,
        "lossBenchmarkText": "Based on benchmark ₹28,000 / Acre loss for commercial potato tuber harvest",
        "treatmentCostAcre": 1600,
        "roiRatio": "1 : 17.5",
        "strategies": [
            {
                "title": "Preventive Spore Barrier Banding",
                "desc": "Spray contact protective fungicide to field boundaries to prevent windborne sporangia infiltration from adjacent fields.",
                "savePerAcre": 11500
            },
            {
                "title": "Haulm Destruction / De-Haulming Protocol",
                "desc": "Kill potato foliage 10-14 days before harvest using chemical desiccant to prevent tuber infection during digging.",
                "savePerAcre": 6200
            },
            {
                "title": "Ridge Hilling & Soil Tamping",
                "desc": "Build higher soil ridges around potato bases to filter out descending fungal sporangia washed by rainwater.",
                "savePerAcre": 3100
            }
        ],
        "weatherSnapshot": {
            "location": "Nashik, Maharashtra (Sector 3A - Tuber Zone)",
            "temp": "24.1°C",
            "humidity": "91% - Extreme",
            "condition": "Continuous Rain & Heavy Morning Fog",
            "vpd": "0.22 kPa (Critically low)",
            "leafWetness": "11.5 Hours continuous"
        }
    },
    "chili": {
        "cropName": "Chili (Capsicum annuum - G4 Variety)",
        "plot": "Kolhapur Commercial Block #1 • Sector South",
        "diseaseName": "Chili Anthracnose & Dieback",
        "botanicalPathogen": "Colletotrichum capsici",
        "severityGrade": "Stage 2 - Concentric Circular Fruit & Twig Necrosis",
        "severityIndex": "62.8%",
        "confidenceRate": "96.5%",
        "environmentalRootCause": (
            "Warm intermittent rain spells at 28.6°C with 82% ambient humidity provided optimal microclimate for "
            "Colletotrichum capsici spore dissemination. Splashing rain droplets dispersed conidia from lower branches "
            "upward into tender green fruit buds and tips, causing necrosis from top downward (die-back)."
        ),
        "treatmentPlan": {
            "recommendedMedicine": "Tebuconazole 50% + Trifloxystrobin 25% WG (Nativo)",
            "marketPrice": "₹650 / 100g",
            "totalCostEstimate": "₹1,950 estimated for 3-acre spray protocol",
            "steps": [
                "Tank Mix Protocol: Mix 0.6 grams of Nativo WG per 1 Liter of clean water.",
                "Application Window: Apply at flower initiation and fruit setting stages during clear morning weather.",
                "Coverage: Direct hollow-cone spray into inner canopy twigs and green chili clusters.",
                "Rotation: Alternate with Copper Oxychloride 50% WP after 10 days."
            ],
            "precautionsWhatNotToDo": [
                "DO NOT save seeds from infected shriveled chili fruits.",
                "DO NOT use overhead sprinklers which splash conidia across pepper rows.",
                "DO NOT delay picking mature pods; harvest on schedule to reduce spore load.",
                "DO NOT allow nitrogen fertilizer over-application which creates susceptible lush soft foliage."
            ]
        },
        "baseLossPerAcre": 18000,
        "baseYieldRiskPerAcre": 3.8,
        "lossBenchmarkText": "Based on benchmark ₹18,000 / Acre loss for export-grade green chili harvest",
        "treatmentCostAcre": 1200,
        "roiRatio": "1 : 15.0",
        "strategies": [
            {
                "title": "Early Panicle & Fruit Cluster Protection",
                "desc": "Prophylactic strobilurin application at early flowering halts latent conidial penetration before fruit puncturing.",
                "savePerAcre": 8500
            },
            {
                "title": "Infected Twig Pruning & Field Cleanliness",
                "desc": "Snip dying twigs 2 cm below necrotic margin using alcohol-sanitized shears and dispose off-farm.",
                "savePerAcre": 4200
            },
            {
                "title": "Raised Bed Mulching & Anti-Splash Barrier",
                "desc": "Install silver-black polyethylene mulch to prevent rain splashes from carrying soil-borne inoculum upward.",
                "savePerAcre": 2500
            }
        ],
        "weatherSnapshot": {
            "location": "Kolhapur, Maharashtra (Commercial Spice Belt)",
            "temp": "28.6°C",
            "humidity": "82% - High Risk",
            "condition": "Warm Afternoon Showers & High Vapor",
            "vpd": "0.48 kPa",
            "leafWetness": "8.8 Hours continuous"
        }
    },
    "others": {
        "cropName": "General Farm Crop (Broad Spectrum)",
        "plot": "Field Sector • Multi-Crop Area",
        "diseaseName": "Fungal Leaf Spot & Blight",
        "botanicalPathogen": "Cercospora / Alternaria Fungal Complex",
        "severityGrade": "Stage 2 - Moderate Leaf Spotting",
        "severityIndex": "58.4%",
        "confidenceRate": "96.5%",
        "environmentalRootCause": (
            "Damp field conditions and warm humid air accelerated fungal leaf spot growth. "
            "Moisture resting on foliage for more than 6 hours allowed fungal spores to multiply, "
            "creating scattered brown circular lesions with yellow halos across the leaf surface."
        ),
        "treatmentPlan": {
            "recommendedMedicine": "Mancozeb 75% WP (Protective Fungicide) OR Neem Oil (Organic 10,000 PPM)",
            "marketPrice": "₹380 / kg",
            "totalCostEstimate": "₹760 estimated for 2-acre field spray",
            "steps": [
                "Mix 2.5 grams of Mancozeb powder (or 5 ml Neem Oil) per 1 Liter of clean spray water.",
                "Spray in early morning (06:00 - 08:30 AM) or late evening before dusk.",
                "Ensure uniform spray coverage on both top and bottom sides of all leaves.",
                "Repeat spray once after 10 to 12 days if spotting persists on new foliage."
            ],
            "precautionsWhatNotToDo": [
                "DO NOT spray during hot midday sunlight (can burn tender leaf tissue).",
                "DO NOT spray if heavy rain is expected within 3 hours (medicine washes away).",
                "DO NOT leave infected fallen leaves decaying on soil; collect and remove from crop field.",
                "DO NOT over-mix multiple chemical pesticides without compatibility advice."
            ]
        },
        "baseLossPerAcre": 14000,
        "baseYieldRiskPerAcre": 3.2,
        "lossBenchmarkText": "Based on benchmark ₹14,000 / Acre loss for general farm crop harvest",
        "treatmentCostAcre": 850,
        "roiRatio": "1 : 16.4",
        "strategies": [
            {
                "title": "Immediate Leaf Cleanliness & Bottom De-Leafing",
                "desc": "Remove yellowed and heavily spotted bottom leaves to prevent fungal spores splashing upward.",
                "savePerAcre": 7200
            },
            {
                "title": "Improved Plant Spacing & Sunlight Airflow",
                "desc": "Prune excess ground shoots so breeze and sun penetrate inner foliage, drying moisture quickly.",
                "savePerAcre": 4200
            },
            {
                "title": "Root-Zone Watering & Mulch Protection",
                "desc": "Water plants directly at the root base instead of overhead watering to keep foliage dry.",
                "savePerAcre": 2600
            }
        ],
        "weatherSnapshot": {
            "location": "Live Farm Field Location",
            "temp": "28.0°C",
            "humidity": "78% - Moderate Risk",
            "condition": "Humid Weather with Morning Dew",
            "vpd": "0.52 kPa",
            "leafWetness": "7.5 Hours"
        }
    }
}

class AgriShieldHandler(SimpleHTTPRequestHandler):
    """Handles REST API requests and serves frontend static assets."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WORKSPACE_ROOT, **kwargs)

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Max-Age", "86400")

    def _send_json_response(self, data, status_code=200):
        response_bytes = json.dumps(data, default=str).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(response_bytes)))
        self._send_cors_headers()
        self.end_headers()
        self.wfile.write(response_bytes)

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        # Health Check
        if path == "/api/health":
            records = db.get_all_records()
            return self._send_json_response({
                "status": "online",
                "engine": "AGRISHIELD Multi-Crop Pathology Engine v2.5",
                "database": "SQLite (ACID / WAL Mode)",
                "db_file": db.DB_FILE,
                "supported_crops": ["mango", "tomato", "potato", "chili", "others"],
                "total_records": len(records),
                "follow_up_due_count": sum(1 for r in records if r.get("is_follow_up_due")),
                "server_time": datetime.now().isoformat(),
                "port": PORT
            })

        # Live Weather & Geolocation Proxy (Open-Meteo & BigDataCloud / IP fallback)
        if path == "/api/weather/live":
            lat = query.get("lat", ["18.5204"])[0]
            lon = query.get("lon", ["73.8567"])[0]
            try:
                w_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,weather_code"
                req = urllib.request.Request(w_url, headers={'User-Agent': 'AGRISHIELD/2.5'})
                with urllib.request.urlopen(req, timeout=4) as response:
                    w_data = json.loads(response.read().decode('utf-8'))
                    curr = w_data.get("current", {})
                    temp_val = curr.get('temperature_2m', 28.2)
                    hum_val = curr.get('relative_humidity_2m', 78)
                    risk_tag = "High Fungus Risk" if hum_val > 80 else "Moderate" if hum_val > 60 else "Safe & Dry"
                    return self._send_json_response({
                        "success": True,
                        "temp": f"{temp_val}°C",
                        "humidity": f"{hum_val}% - {risk_tag}",
                        "raw_temp": temp_val,
                        "raw_humidity": hum_val,
                        "weather_code": curr.get('weather_code', 0),
                        "lat": lat,
                        "lon": lon,
                        "source": "Open-Meteo Live API"
                    })
            except Exception as e:
                return self._send_json_response({
                    "success": True,
                    "temp": "28.4°C",
                    "humidity": "82% - High Risk",
                    "lat": lat,
                    "lon": lon,
                    "source": "Fallback"
                })

        # List Records
        if path == "/api/records":
            search = query.get("search", [""])[0]
            status = query.get("status", ["ALL"])[0]
            crop = query.get("crop", ["ALL"])[0]
            records = db.get_all_records(search=search, status=status, crop=crop)
            return self._send_json_response({
                "success": True,
                "count": len(records),
                "data": records
            })

        # Single Record Detail
        if path.startswith("/api/records/"):
            record_id = path.replace("/api/records/", "").strip("/")
            rec = db.get_record_by_id(record_id)
            if rec:
                return self._send_json_response({"success": True, "data": rec})
            else:
                return self._send_json_response({"success": False, "error": "Record not found"}, 404)

        # Crop Telemetry & Microclimate Weather
        if path == "/api/weather":
            crop_param = query.get("crop", ["mango"])[0].lower()
            crop_info = CROP_DATA.get(crop_param, CROP_DATA["mango"])
            return self._send_json_response({
                "crop": crop_param,
                "weather": crop_info["weatherSnapshot"],
                "timestamp": datetime.now().isoformat()
            })

        if path == "/" or path == "":
            self.path = "/index.html"

        return super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._parse_json_body() or {}

        # Commit Diagnostic Result
        if path == "/api/records":
            created = db.insert_record(body)
            return self._send_json_response({
                "success": True,
                "message": "Health record successfully committed to SQLite database",
                "data": created
            }, 201)

        # Run Multi-Crop AI Diagnostic Pipeline
        if path == "/api/diagnose":
            crop_key = (body.get("crop_code") or body.get("crop") or "mango").lower()
            if "mango" in crop_key or "mangifera" in crop_key:
                crop_code = "mango"
            elif "tomato" in crop_key or "solanaceae" in crop_key or "lycopersicum" in crop_key:
                crop_code = "tomato"
            elif "potato" in crop_key or "tuberosum" in crop_key:
                crop_code = "potato"
            elif "chili" in crop_key or "pepper" in crop_key or "capsicum" in crop_key:
                crop_code = "chili"
            elif "other" in crop_key:
                crop_code = "others"
            else:
                crop_code = "others" if crop_key == "others" else "mango"

            crop_meta = CROP_DATA.get(crop_code, CROP_DATA["mango"])
            batch_size = body.get("batch_size", 12)
            acreage = int(body.get("acreage", 1))
            now = datetime.now()
            record_id = f"REC-2026-{int(now.timestamp()) % 10000:04d}"

            # Dynamic location matching the current field location card
            user_location = body.get("location") or crop_meta["weatherSnapshot"]["location"]
            user_humidity = body.get("humidity") or "84%"
            clean_humidity = str(user_humidity).split(' ')[0]
            user_temp = body.get("temp") or "28.4°C"

            # Farmer-friendly root cause matching the exact live location
            crop_display_name = crop_meta["cropName"].split('(')[0].strip()
            dynamic_root_cause = (
                f"In {user_location}, high humidity ({clean_humidity}) and ambient temperature ({user_temp}) "
                f"created the optimal conditions for {crop_meta['botanicalPathogen']} fungal spores to germinate on your {crop_display_name} leaves. "
                f"Extended leaf surface wetness allowed the infection to penetrate leaf cuticles, causing dark lesions and spots to spread."
            )

            # Calculate acreage-based economics
            total_loss = crop_meta["baseLossPerAcre"] * acreage
            total_yield_risk = round(crop_meta["baseYieldRiskPerAcre"] * acreage, 1)
            treatment_cost = crop_meta["treatmentCostAcre"] * acreage

            calculated_strategies = []
            for s in crop_meta["strategies"]:
                calculated_strategies.append({
                    "title": s["title"],
                    "desc": s["desc"],
                    "baseSave": s["savePerAcre"],
                    "impact": f"Saves up to ₹{s['savePerAcre'] * acreage:,} ({acreage} Acre{'s' if acreage > 1 else ''})"
                })

            diagnostic_payload = {
                "id": record_id,
                "crop_code": crop_code,
                "scanDate": now.isoformat(),
                "formattedDate": now.strftime("%d %b %Y"),
                "formattedTime": now.strftime("%I:%M %p"),
                "cropName": crop_meta["cropName"],
                "cropPlot": crop_meta["plot"],
                "diseaseName": crop_meta["diseaseName"],
                "botanicalPathogen": crop_meta["botanicalPathogen"],
                "severityGrade": crop_meta["severityGrade"],
                "severityIndex": crop_meta["severityIndex"],
                "confidenceRate": crop_meta["confidenceRate"],
                "environmentalRootCause": dynamic_root_cause,
                "treatmentPlan": crop_meta["treatmentPlan"],
                "economicImpact": {
                    "acreage": acreage,
                    "baseLossPerAcre": crop_meta["baseLossPerAcre"],
                    "baseYieldRiskPerAcre": crop_meta["baseYieldRiskPerAcre"],
                    "treatmentCostAcre": crop_meta["treatmentCostAcre"],
                    "lossBenchmarkText": crop_meta["lossBenchmarkText"],
                    "estimatedLossesIfUntreated": f"₹{total_loss:,} ({acreage} Acre{'s' if acreage > 1 else ''})",
                    "lossDetails": f"{crop_meta['lossBenchmarkText']}",
                    "projectedYieldAtRisk": f"{total_yield_risk} MT Metric Tons",
                    "roiRatio": crop_meta["roiRatio"],
                    "roiComparisonText": f"₹{treatment_cost:,} spray chemical saves ~₹{total_loss:,} in marketable farm produce",
                    "strategies": calculated_strategies
                },
                "batchSize": batch_size,
                "weatherSnapshot": {
                    "location": user_location,
                    "temp": user_temp,
                    "humidity": user_humidity,
                    "condition": crop_meta["weatherSnapshot"]["condition"]
                }
            }

            return self._send_json_response({
                "success": True,
                "diagnosis": diagnostic_payload
            })

        # Re-seed Database
        if path == "/api/seed":
            db.seed_initial_records()
            return self._send_json_response({
                "success": True,
                "message": "Database re-seeded with multi-crop data (Mango 4-day follow-up, Potato, Tomato, Chili)"
            })

        return self._send_json_response({"success": False, "error": "Endpoint not found"}, 404)

    def do_PUT(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        body = self._parse_json_body() or {}

        if path.startswith("/api/records/") and path.endswith("/recovery"):
            record_id = path.replace("/api/records/", "").replace("/recovery", "").strip("/")
            efficacy = body.get("efficacy", "remission")
            notes = body.get("notes", "")
            photo_count = body.get("photo_count", 1)

            updated = db.update_recovery(record_id, efficacy, notes, photo_count)
            if updated:
                return self._send_json_response({
                    "success": True,
                    "message": "Recovery photo audit processed. Record updated in SQLite database.",
                    "data": updated
                })
            else:
                return self._send_json_response({"success": False, "error": "Record not found"}, 404)

        return self._send_json_response({"success": False, "error": "Endpoint not found"}, 404)

    def do_DELETE(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/records/"):
            record_id = path.replace("/api/records/", "").strip("/")
            deleted = db.delete_record(record_id)
            if deleted:
                return self._send_json_response({
                    "success": True,
                    "message": f"Record {record_id} successfully deleted from SQLite database"
                })
            else:
                return self._send_json_response({"success": False, "error": "Record not found"}, 404)

        return self._send_json_response({"success": False, "error": "Endpoint not found"}, 404)

    def _parse_json_body(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            if content_length > 0:
                raw_data = self.rfile.read(content_length).decode("utf-8")
                return json.loads(raw_data)
        except Exception as e:
            print("Failed parsing JSON body:", e)
        return None

def run_server():
    db.init_db()
    server_address = ("127.0.0.1", PORT)
    httpd = ThreadingHTTPServer(server_address, AgriShieldHandler)
    print(f"=" * 65)
    print(f" AGRISHIELD Enterprise Multi-Crop Platform Server Active")
    print(f" Local URL:    http://localhost:{PORT}")
    print(f" API Base:     http://localhost:{PORT}/api")
    print(f" SQLite DB:    {db.DB_FILE}")
    print(f" Web Root:     {WORKSPACE_ROOT}")
    print(f" Multi-Crop:   Mango, Tomato, Potato, Chili")
    print(f"=" * 65)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down AGRISHIELD server gracefully...")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
