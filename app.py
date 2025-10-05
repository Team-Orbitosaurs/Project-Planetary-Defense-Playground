import os
import math
import requests
from functools import lru_cache
from typing import Dict, Any
from datetime import date
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

NASA_API_KEY = "API_KEY"
NEO_FEED_URL = "https://api.nasa.gov/neo/rest/v1/feed"
SBDB_URL = "https://ssd-api.jpl.nasa.gov/sbdb.api"
USGS_EQ_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe_get_json(url, params=None, timeout=12):
    try:
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("HTTP error:", e)
        return None

def format_size_text(diameter_m: float) -> str:
    if diameter_m < 10:
        return "Small (car-sized)"
    if diameter_m < 50:
        return "Building-sized"
    if diameter_m < 200:
        return "Stadium-sized"
    return "City-block sized"

def estimate_casualties(diameter_m: float) -> int:
    k = 100 
    return int(k * (diameter_m ** 2))

def energy_to_richter(joules: float) -> float:
    if joules <= 0:
        return 0.0
    return (math.log10(joules) - 4.8) / 1.5

def fetch_neows_feed(date_str: str):
    params = {"start_date": date_str, "end_date": date_str, "api_key": NASA_API_KEY}
    data = safe_get_json(NEO_FEED_URL, params=params)
    if not data or "near_earth_objects" not in data:
        raise RuntimeError("NeoWs feed error or empty response")
    return data["near_earth_objects"].get(date_str, [])

def pick_most_relevant_neo(neos: list):
    if not neos:
        raise ValueError("No NEOs found")
    best = None
    best_dist = float("inf")
    for neo in neos:
        cad = neo.get("close_approach_data", [])
        if not cad:
            continue
        dist_km = float(cad[0]["miss_distance"]["kilometers"])
        if dist_km < best_dist:
            best_dist = dist_km
            best = neo
    return best or neos[0]

@lru_cache(maxsize=256)
def fetch_sbdb(designation: str):
    params = {"des": designation}
    return safe_get_json(SBDB_URL, params=params)

def build_student_payload(date_str: str = None, user_choice: str = None) -> Dict[str, Any]:
    if date_str is None:
        date_str = date.today().strftime("%Y-%m-%d")
    neos = fetch_neows_feed(date_str)
    neo = pick_most_relevant_neo(neos)

    cad = neo["close_approach_data"][0]
    diameter_m = neo["estimated_diameter"]["meters"]["estimated_diameter_max"]
    speed_km_s = float(cad["relative_velocity"]["kilometers_per_second"])
    distance_km = float(cad["miss_distance"]["kilometers"])
    name = neo["name"]
    designation = neo.get("neo_reference_id") or neo.get("designation") or name

    risk_prob = 0.02 if distance_km < 5_000_000 else 0.001
    casualties = estimate_casualties(diameter_m)

    density = 3000
    radius = diameter_m / 2.0
    mass = (4/3) * 3.14159 * (radius**3) * density
    velocity_m_s = speed_km_s * 1000.0
    energy_j = 0.5 * mass * velocity_m_s**2
    eq_mag = energy_to_richter(energy_j)

    final_status = "Unresolved"
    new_prob = risk_prob
    new_casualties = casualties

    if user_choice == "Survey":
        new_prob *= 0.9
        final_status = "Improved orbit tracking, still at risk"
    elif user_choice == "Deflect":
        new_prob *= 0.25
        final_status = "Asteroid deflected successfully"
    elif user_choice == "Evacuate":
        new_casualties = int(casualties * 0.3)
        final_status = "Mass evacuation reduced casualties"
    else:
        final_status = "No action taken"

    timeline = [
        {"phase": "Discovery", "description": f"Asteroid {name} spotted by NASA telescopes.",
         "data": {"date_detected": date_str, "confidence": "Low"}},
        {"phase": "Risk Assessment", "description": "NASA analyzes orbit, size, and speed.",
         "data": {"impact_probability": f"{risk_prob*100:.2f}%", "hazard_level": "High" if risk_prob > 0.01 else "Low"}},
        {"phase": "Mitigation Action", "description": "User selects a response.",
         "data": {"user_choice": user_choice or "None", "new_impact_probability": f"{new_prob*100:.2f}%", "new_casualties_estimate": new_casualties}},
        {"phase": "Final Outcome", "description": final_status,
         "data": {"status": "✅ Safe" if new_prob < 0.005 else "⚠ Still Risk", "remaining_risk": f"{new_prob*100:.2f}%"}}]

    return {
        "alert": f"🚨 Breaking News: Asteroid {name} detected!",
        "asteroid": {
            "id": designation,
            "name": name,
            "size_m": diameter_m,
            "size_text": format_size_text(diameter_m),
            "speed_km_s": speed_km_s,
            "distance_km": distance_km,
            "impact_probability": f"{risk_prob*100:.2f}%",
            "casualties_estimate": casualties,
            "impact_energy_j": energy_j,
            "equivalent_eq_mag": eq_mag
        },
        "timeline": timeline
    }

@app.get("/asteroid")
def asteroid(choice: str = None, date: str = None):
    return build_student_payload(date_str=date, user_choice=choice)

@app.get("/demo")
def demo():
    return {
        "alert": "🚨 Breaking News: Asteroid 2025-AB detected!",
        "asteroid": {"id": "2025AB", "name": "2025-AB", "size_m": 320, "size_text": "Stadium-sized",
                     "speed_km_s": 21.0, "distance_km": 4500000,
                     "impact_probability": "1.20%", "casualties_estimate": 2000000,
                     "impact_energy_j": 4.5e+16, "equivalent_eq_mag": 7.1},
        "timeline": [
            {"phase": "Discovery", "description": "Asteroid spotted by NASA telescopes.", "data": {"date_detected": "2025-10-05", "confidence": "Low"}},
            {"phase": "Risk Assessment", "description": "NASA analyzes orbit, size, and speed.", "data": {"impact_probability": "1.20%", "hazard_level": "⚠ High"}},
            {"phase": "Mitigation Action", "description": "User selects a response.", "data": {"user_choice": "None", "new_impact_probability": "1.20%", "new_casualties_estimate": 2000000}},
            {"phase": "Final Outcome", "description": "No action taken.", "data": {"status": "⚠ Still Risk", "remaining_risk": "1.20%"}}
        ]
    }

@app.get("/")
def root():
    return FileResponse("static/index.html")  # make sure index.html is in the same folder

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Serve the "static" folder
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html at "/"
@app.get("/")
def read_index():
    return FileResponse("static/index.html")