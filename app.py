import os
from flask import Flask, jsonify, abort
from flask_cors import CORS
from dotenv import load_dotenv
import mysql.connector

from places import get_places_for_city

load_dotenv()  # reads variables from a local .env file (never committed to git)

app = Flask(__name__)
CORS(app)  # allows the frontend (running separately) to call this API

# ---- Database connection settings ----
# The real password lives in a local .env file (see .env.example), not here.
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": "tourist_safety"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


def calculate_safety_score(crime_score, popularity_score, max_crime):
    """
    Converts crime_score into a 0-10 'safety' score (higher = safer),
    then blends it with popularity to produce a final ranking score.
    """
    safety = 10 - (crime_score / max_crime) * 10
    final_score = (safety * 0.6) + (popularity_score / 40 * 10 * 0.4)
    return round(final_score, 2)


def build_ranked_cities(rows):
    """Takes raw DB rows (list of dicts) and returns them enriched with safety_rank_score."""
    if not rows:
        return []

    max_crime = max(float(c["crime_score"]) for c in rows)

    results = []
    for c in rows:
        crime = float(c["crime_score"])
        popularity = float(c["popularity_score"])
        score = calculate_safety_score(crime, popularity, max_crime)
        results.append({
            "id": c["id"],
            "name": c["name"],
            "country": c["country"],
            "crime_score": crime,
            "popularity_score": popularity,
            "safety_rank_score": score,
            "latitude": float(c["latitude"]) if c["latitude"] else None,
            "longitude": float(c["longitude"]) if c["longitude"] else None,
            "state": c["state"],
            "data_source": c["data_source"]
        })

    return results


@app.route("/api/cities", methods=["GET"])
def get_cities():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cities")
    cities = cursor.fetchall()
    cursor.close()
    conn.close()

    results = build_ranked_cities(cities)
    results.sort(key=lambda x: x["safety_rank_score"], reverse=True)
    return jsonify(results)


@app.route("/api/states", methods=["GET"])
def get_states():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT state, COUNT(*) AS city_count
        FROM cities
        GROUP BY state
        ORDER BY state ASC
    """)
    states = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(states)


@app.route("/api/states/<state_name>/cities", methods=["GET"])
def get_cities_by_state(state_name):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM cities WHERE state = %s", (state_name,))
    cities = cursor.fetchall()
    cursor.close()
    conn.close()

    if not cities:
        abort(404, description=f"No cities found for state '{state_name}'")

    results = build_ranked_cities(cities)
    results.sort(key=lambda x: x["popularity_score"], reverse=True)
    return jsonify(results)


@app.route("/api/cities/<int:city_id>/places", methods=["GET"])
def get_places(city_id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id, name, state FROM cities WHERE id = %s", (city_id,))
    city = cursor.fetchone()
    cursor.close()
    conn.close()

    if not city:
        abort(404, description=f"No city found with id {city_id}")

    places, has_real_data = get_places_for_city(city["name"])
    return jsonify({
        "city_id": city["id"],
        "city_name": city["name"],
        "state": city["state"],
        "places": places,
        "has_real_data": has_real_data
    })


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Tourist Safety Ranker API is running"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)