# Tourist Safety Ranker — India

A web app that ranks Indian cities by safety and popularity for travelers. Browse by state, drill into a city, and see its safety ranking alongside top places to visit.

## Live demo
Run locally — see setup below. (Add a hosted link here if you deploy it.)

## Features
- Browse all 28 states and 8 union territories of India
- Cities within each state ranked by popularity and safety
- Safety score blends real crime data with tourism popularity data
- Interactive map showing city locations, color-coded by safety tier
- Top places to visit for cities with researched attraction data

## Data honesty
Not all data here is equally reliable, and the app is upfront about it:
- Cities tagged **NCRB/MoT** use real government crime statistics (National Crime Records Bureau) and tourism footfall data (Ministry of Tourism)
- Cities tagged **Estimated** use reasoned estimates where official data isn't publicly available in structured form
- Cities without researched attraction data show "Coming soon" instead of invented places

This distinction is visible directly in the UI so nothing is presented as more authoritative than it is.

## Tech stack
- **Backend:** Python, Flask, MySQL (`mysql-connector-python`)
- **Frontend:** Vanilla HTML/CSS/JavaScript, Leaflet.js for the map
- **Database:** MySQL

## Project structure
```
tourist-safety/
├── app.py              # Flask API server
├── places.py           # Attraction data lookup
├── index.html          # Frontend
├── requirements.txt    # Python dependencies
├── .env.example        # Template for required environment variables
└── .gitignore
```

## Setup

### 1. Clone the repo
```
git clone https://github.com/11Rishi11/Tourist-Safety-Ranker.git
cd Tourist-Safety-Ranker
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set up the database
Create a MySQL database named `tourist_safety` with a `cities` table containing columns: `id, name, country, crime_score, popularity_score, latitude, longitude, state, data_source`. Populate it with your city data.

### 4. Configure environment variables
Copy `.env.example` to `.env` and fill in your real MySQL password:
```
cp .env.example .env
```
```
DB_PASSWORD=your_actual_mysql_password
```

### 5. Run the backend
```
python app.py
```
This starts the API at `http://127.0.0.1:5000`.

### 6. Open the frontend
Open `index.html` directly in your browser (double-click it, or use a local server). It expects the backend running at `127.0.0.1:5000`.

## API endpoints
| Endpoint | Description |
|---|---|
| `GET /api/cities` | Flat list of all cities, ranked by safety score |
| `GET /api/states` | List of all states/UTs with city counts |
| `GET /api/states/<state_name>/cities` | Cities in a given state, ranked by popularity |
| `GET /api/cities/<city_id>/places` | Top places to visit in a specific city |

## Roadmap / possible next steps
- Expand attraction data coverage beyond the 10 currently researched cities
- Add user reviews or safety tips per city
- Deploy backend + frontend so it's accessible without running locally

## License
Add a license of your choice (MIT is a common permissive default for personal projects).
