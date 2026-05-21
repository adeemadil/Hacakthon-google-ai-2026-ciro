# CIRO — Crisis Intelligence & Response Orchestrator

> An AI-powered multi-agent system that predicts floods and heatwaves across Pakistani cities up to 30 days in advance and automatically generates emergency response plans.

---

## What Is CIRO?

CIRO monitors 8 major urban zones across Pakistan around the clock. Every 15 minutes it pulls live data from weather APIs, satellite imagery, river flood sensors, traffic systems, and government disaster feeds. It runs that data through a machine learning model to forecast flood and heatwave risk for each city over the next 30 days. When risk crosses a danger threshold, a panel of three AI expert agents debate the situation and decide how urgent it is. If action is needed, a fourth AI agent generates a concrete, agency-specific emergency response plan — naming who should respond, how many people to evacuate, and what resources to deploy.

The full cycle runs automatically every 2 hours. All results are visible through a Flutter mobile app with live maps, 30-day risk charts, and real-time push notifications.

---

## Monitored Zones

| Zone | City | Province |
|------|------|----------|
| islamabad-g10 | Islamabad G-10 | Federal |
| lahore-gulberg | Lahore Gulberg | Punjab |
| karachi-korangi | Karachi Korangi | Sindh |
| peshawar-hayatabad | Peshawar Hayatabad | KPK |
| quetta-satellite | Quetta Satellite Town | Balochistan |
| multan-cantt | Multan Cantt | Punjab |
| faisalabad-millat | Faisalabad Millat Town | Punjab |
| sukkur-rohri | Sukkur Rohri | Sindh |

---

## Key Features

- **30-day flood and heatwave forecasts** per city, updated every 2 hours
- **Multi-agent AI debate** — three Gemini-powered expert personas analyze and challenge each other before any alert is raised
- **Automatic response planning** — AI generates evacuation orders, shelter activation, agency deployment with before/after impact simulation
- **Live signal stream** — real-time WebSocket feed of weather, traffic, satellite, and social signals
- **Pakistan-specific** — trained on 22 years of local data, references NDMA, PDMA, Rescue 1122, and Pakistan Army
- **Mostly free data sources** — Open-Meteo and GloFAS require no API key
- **Mobile app** — Flutter app with interactive maps, risk charts, and push alerts
- **Full audit trail** — every orchestration cycle is logged with a complete reasoning trace

---

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│              EXTERNAL DATA SOURCES                       │
│  Open-Meteo · GloFAS · OpenWeatherMap · Google Maps     │
│  Google Earth Engine · Social Media · NDMA Alerts        │
└──────────────────┬──────────────────────────────────────┘
                   │ httpx (every 15 min)
┌──────────────────▼──────────────────────────────────────┐
│         AGENT 2: Data Collector                          │
│  Fetches all sources in parallel for all 8 zones         │
│  Normalizes to unified Signal format                     │
│  Stores in SQLite · Broadcasts via WebSocket             │
└────────┬──────────────────────────┬─────────────────────┘
         │                          │
┌────────▼────────┐      ┌──────────▼──────────┐
│  SQLite DB      │      │  WebSocket Manager   │
│  30-day buffer  │      │  /ws/signals         │
│  signal_store   │      │  Real-time stream    │
└────────┬────────┘      └──────────┬───────────┘
         │                          │ live signals
┌────────▼────────────────┐   ┌─────▼───────────┐
│   AGENT 3: ML Predictor │   │  Flutter App    │
│   XGBoost + Prophet     │   │  Notifications  │
│   30-day forecast       │   └─────────────────┘
└────────┬────────────────┘
         │ predictions (every 2 hrs)
┌────────▼────────────────────────────────────────────────┐
│              ORCHESTRATOR                                │
│  Evaluates all 8 zones · Filters risk ≥ 0.30            │
└────────┬────────────────────────────────────────────────┘
         │ high-risk zones
┌────────▼────────────────────────────────────────────────┐
│         DEBATER AGENT (Gemini 2.5)                       │
│  Hydrologist · Meteorologist · Urban Planner             │
│  4 LLM calls per zone → Consensus verdict                │
└────────┬────────────────────────────────────────────────┘
         │ urgency = ACT_NOW or PREPARE
┌────────▼────────────────────────────────────────────────┐
│         AGENT 4: Response Commander (Gemini)             │
│  Generates action plan · Simulates impact                │
│  NDMA · PDMA · Rescue 1122 · Pakistan Army               │
└────────┬────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────┐
│         FastAPI Backend  (port 8000)                     │
│         REST + WebSocket endpoints                       │
└────────┬────────────────────────────────────────────────┘
         │
┌────────▼────────────────────────────────────────────────┐
│         Flutter Mobile App                               │
│  Home · Agents · Live Map · Predictions · Alerts         │
└─────────────────────────────────────────────────────────┘
```

---

## AI Agents

### Agent 1 — Satellite Imagery (`agent_imagery.py`)
Connects to Google Earth Engine and processes satellite imagery over each zone. Computes the Normalized Difference Water Index (NDWI) to detect surface water changes and NDSI for snow/ice coverage. Outputs are fed into Agent 2 as `satellite_agent1` signals.

### Agent 2 — Data Collector (`agent_data_collector.py`)
The data ingestion backbone. Runs `run_fetch_cycle()` every 15 minutes via APScheduler, pulling from 6 sources in parallel across all 8 zones:

| Source | Data | Cost |
|--------|------|------|
| Open-Meteo | Weather + 16-day ECMWF/GFS forecast | Free |
| GloFAS via Open-Meteo | 30-day river discharge forecast | Free |
| OpenWeatherMap | Real-time weather | API key |
| Google Maps | Traffic congestion | API key |
| Google Earth Engine | Satellite NDWI/NDSI | Service account |
| Social + NDMA | Crisis keywords, official alerts | Simulated |

All data is normalized into a unified Signal format:
```json
{
  "signal_id": "unique-string",
  "signal_type": "rainfall | temperature | humidity | wind | traffic | social | official",
  "zone_id": "karachi-korangi",
  "value": 47.2,
  "severity": 8,
  "confidence": 0.91,
  "source": "openweathermap",
  "timestamp": "2025-05-21T14:00:00Z",
  "metadata": {}
}
```

Signals are stored in SQLite with deduplication and broadcast live over WebSocket.

### Agent 3 — ML Predictor (`agent_predictor.py`)
Generates a 30-day daily flood and heatwave risk forecast per zone.

**Flood Model — XGBoost**
- Trained on 1,572 samples from 6 Pakistani provinces (2000–2021 GEE data)
- Features: month, temperature, rainfall, NDSI (ice), NDVI (vegetation), province encoding
- Accuracy: ~92%, AUC: ~0.85
- Handles 3.8% flood class imbalance via `scale_pos_weight`

**Heatwave Model — UNICEF Methodology**
- 90th percentile temperature threshold per province and month
- 3+ consecutive days above threshold triggers heatwave classification
- Zone-specific severity multipliers (Jacobabad 1.0×, Islamabad 0.4×, etc.)

**Forecast Horizon**
- Days 1–16: Real ECMWF/GFS data from Open-Meteo
- Days 17–30: Prophet ML forecaster trained on 22 years of Pakistan weather data (autoregressive)

**6 Prediction Enhancements (v3.0)**
1. **Antecedent Moisture Index (AMI)** — exponentially weighted 30-day rainfall to model soil saturation
2. **Discharge Momentum** — rate of change in GloFAS river levels (rising rivers = higher risk)
3. **Monsoon Onset Detection** — detects the inflection point when soil saturation spikes seasonally
4. **EWMA Temporal Smoothing** — alpha=0.3 smoothing across the 30-day window to capture dependency chains
5. **Sigmoid Calibration** — S-curve output to avoid artificially hard probability caps
6. **UNICEF Heatwave Detection** — rolling 90th percentile methodology aligned with international standards

**Sample Output per Day:**
```json
{
  "day": 7,
  "date": "2025-05-28",
  "flood_risk": 0.73,
  "heatstroke_risk": 0.41,
  "alert_level": "HIGH",
  "dominant_factor": "antecedent_moisture",
  "expected_temp_c": 38.4,
  "expected_rain_mm": 22.1,
  "confidence": "high"
}
```

### Debater Agent (`agent_debater.py`)
When a zone's predicted risk crosses the 0.30 threshold, three Gemini-powered expert personas independently analyze the situation and debate each other — 4 LLM calls per zone.

**Expert Personas:**

| Persona | Focus Areas |
|---------|-------------|
| Hydrologist | Antecedent moisture, GloFAS discharge trends, 2022 Pakistan flood patterns |
| Meteorologist | ECMWF/GFS rainfall forecasts, monsoon progression, 48-hour extremes |
| Urban Planner | Drainage capacity, population exposure, evacuation feasibility |

Each persona votes: `MONITOR | PREPARE | ACT_NOW`

A fourth LLM call synthesizes a consensus:
```json
{
  "trigger_type": "FLOOD | HEAT | BOTH",
  "flood_probability": 0.73,
  "heat_probability": 0.41,
  "verdict": "CRITICAL FLOOD — 73% flood risk, ACT before Day 7",
  "urgency": "ACT_NOW",
  "recommended_action_window_days": [5, 9],
  "unanimous": true,
  "rationale": "All three experts agree that saturated soil combined with 22mm forecast rainfall..."
}
```

### Agent 4 — Response Commander (`agent_response.py`)
Activated only for zones where the Debater returns `ACT_NOW` or `PREPARE`. Uses Gemini to generate a structured emergency response plan.

**Action Categories:** `EVACUATE · ALERT · DEPLOY · REROUTE · SHELTER · MEDICAL`

**Priority Tiers:** `IMMEDIATE · WITHIN_6H · WITHIN_24H · PREPARATORY`

Each action includes the responsible Pakistani agency (NDMA, PDMA, Rescue 1122, Pakistan Army, Civil Defense), target population count, required resources, and estimated execution time.

**Impact Simulation — Before vs After:**
```
Before: 45,000 at risk · 0 evacuated · 0 shelters open · 0 medical units
After:  12,000 at risk · 33,000 evacuated · 8 shelters open · 12 medical units
Effectiveness Score: 0.84
```

Falls back to a rule-based plan if the Gemini API is unavailable.

### Orchestrator (`agent_orchestrator.py`)
The central coordinator. Triggered every 2 hours by APScheduler and also manually callable via API.

**Pipeline per cycle:**
1. Fetch 30-day predictions from Agent 3 for all 8 zones in parallel
2. Filter: keep zones with `peak_flood_risk ≥ 0.30` OR `peak_heat_risk ≥ 0.30`
3. Run Debater on every high-risk zone
4. Filter: keep zones with `urgency = ACT_NOW or PREPARE`
5. Run Agent 4 response planning for those zones
6. Log the full cycle — stores last 20 runs with complete reasoning traces

---

## Tech Stack

### Backend
| Component | Technology |
|-----------|------------|
| API Framework | FastAPI + Uvicorn |
| ML — Flood | XGBoost 2.1.0 |
| ML — Weather Forecast | Prophet 1.1.5 |
| LLM | Gemini 2.5 Flash Lite (Google AI) |
| Scheduler | APScheduler 3.10.4 (AsyncIO) |
| Database | SQLite + aiosqlite 0.20.0 |
| HTTP Client | httpx (async) |
| Satellite | Google Earth Engine API 0.1.411 |
| Containerization | Docker |
| Language | Python 3.11 |

### Mobile App
| Component | Technology |
|-----------|------------|
| Framework | Flutter 3.0+ / Dart |
| State Management | Provider 6.1.1 |
| HTTP Client | Dio 5.4.0 |
| Charts | fl_chart 0.66.0 |
| WebSocket | web_socket_channel 2.4.0 |
| Notifications | flutter_local_notifications 17.0.0 |
| Maps | url_launcher 6.2.1 (Google Maps) |

---

## Project Structure

```
Fuckathon/
├── backend/
│   ├── main.py                        # FastAPI app, lifespan, WebSocket endpoint
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   ├── config/
│   │   └── settings.py                # All configuration (Pydantic BaseSettings)
│   ├── agents/
│   │   ├── agent_imagery.py           # Agent 1 — Google Earth Engine satellite
│   │   ├── agent_data_collector.py    # Agent 2 — Data ingestion and normalization
│   │   ├── agent_predictor.py         # Agent 3 — XGBoost + Prophet ML forecasting
│   │   ├── agent_debater.py           # Debater — Gemini multi-persona LLM debate
│   │   ├── agent_response.py          # Agent 4 — Emergency response planning
│   │   └── agent_orchestrator.py      # Orchestrator — Pipeline coordinator
│   ├── services/
│   │   ├── scheduler.py               # APScheduler job definitions
│   │   ├── signal_store.py            # SQLite read/write + pruning
│   │   ├── websocket_manager.py       # WebSocket connection + broadcast manager
│   │   ├── weather_service.py         # OpenWeatherMap wrapper
│   │   ├── openmeteo_service.py       # Open-Meteo weather + GloFAS wrapper
│   │   ├── traffic_service.py         # Google Maps traffic wrapper
│   │   ├── earth_engine_service.py    # GEE satellite wrapper
│   │   ├── social_service.py          # Social media signal simulator
│   │   ├── ndma_service.py            # NDMA alert simulator
│   │   ├── weather_forecaster.py      # Prophet ML weather forecaster (days 17-30)
│   │   ├── gemini_retry.py            # Gemini API retry with exponential backoff
│   │   └── retry_client.py            # HTTP circuit breaker client
│   ├── data/
│   │   ├── signals.db                 # Auto-created SQLite database
│   │   └── training/                  # CSV training data per province (2000-2021)
│   └── models/
│       ├── flood_model.joblib         # Trained XGBoost model
│       └── prophet/                   # Prophet model files (auto-created on first run)
│
└── ciro_app/                          # Flutter mobile app
    ├── lib/
    │   ├── main.dart                  # App entry point + bottom navigation shell
    │   ├── screens/
    │   │   ├── home_screen.dart       # Zone status dashboard
    │   │   ├── agents_screen.dart     # Agent logs and orchestrator results
    │   │   ├── live_map_screen.dart   # Interactive risk map
    │   │   ├── prediction_screen.dart # 30-day risk chart per zone
    │   │   └── alerts_screen.dart     # Alert history and filtering
    │   ├── services/
    │   │   ├── api_service.dart       # REST API calls (Dio)
    │   │   ├── websocket_service.dart # Real-time signal subscription
    │   │   └── notification_service.dart # Push notifications
    │   ├── models/
    │   │   ├── zone.dart
    │   │   └── prediction.dart
    │   ├── theme/
    │   │   └── ciro_theme.dart        # Dark theme configuration
    │   └── config/
    │       └── api_config.dart        # Backend URL configuration
    └── pubspec.yaml
```

---

## Configuration

Copy `.env.example` to `.env` in the `backend/` folder and fill in the values:

```env
ENVIRONMENT=development

# Required for real weather data
OPENWEATHER_API_KEY=your_key_here

# Required for traffic data
GOOGLE_MAPS_API_KEY=your_key_here

# Required for LLM debate and response planning
GOOGLE_API_KEY=your_gemini_key_here

# Required for satellite imagery (Agent 1)
GEE_PROJECT_ID=your_gee_project
GEE_SERVICE_ACCOUNT=your_service_account@project.iam.gserviceaccount.com
GEE_CREDENTIALS_PATH=./config/gee_credentials.json

# Optional
FIREBASE_PROJECT_ID=your_firebase_project
```

**Key settings in `config/settings.py`:**

| Setting | Default | Description |
|---------|---------|-------------|
| `FETCH_INTERVAL_MINUTES` | `15` | How often Agent 2 collects data |
| `ORCHESTRATOR_INTERVAL_HOURS` | `2` | How often the AI pipeline runs |
| `RISK_ALERT_THRESHOLD` | `0.30` | Minimum risk score to trigger debate |
| `SIGNAL_BUFFER_DAYS` | `30` | Rolling window kept in SQLite |
| `DEBATE_LLM_MODEL` | `gemini-2.5-flash-lite` | Gemini model for all LLM calls |

> **Note:** Open-Meteo and GloFAS work without any API key. The system runs in degraded mode (no LLM features) without a Gemini key.

---

## How to Run

### Backend (Python)

**Prerequisites:** Python 3.11+, pip

```bash
# 1. Navigate to backend
cd backend

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env with your API keys

# 5. Start the server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server starts at `http://localhost:8000`. On startup it will:
- Initialize the SQLite database
- Train the XGBoost model if not already built
- Start APScheduler (15-min fetch, 2-hour orchestrator, daily prune)
- Connect to Earth Engine (if credentials are set)

**Interactive API docs:** `http://localhost:8000/docs`

---

### Backend (Docker)

```bash
cd backend

# Build image
docker build -t ciro-backend .

# Run container
docker run -p 8000:8000 --env-file .env ciro-backend
```

---

### Flutter Mobile App

**Prerequisites:** Flutter 3.0+, Android Studio or Xcode

```bash
# 1. Navigate to app
cd ciro_app

# 2. Set backend URL
# Edit lib/config/api_config.dart and set baseUrl to your backend address
# e.g. http://192.168.1.x:8000 for local network, or your deployed URL

# 3. Install dependencies
flutter pub get

# 4. Run on connected device or emulator
flutter run

# Build release APK
flutter build apk --release
```

---

## API Endpoints

### Agent 2 — Data Collection
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/agent2/fetch` | Manually trigger a full fetch cycle |
| `GET` | `/api/v1/agent2/signals/{zone_id}` | Latest signals for a zone |
| `GET` | `/api/v1/agent2/signals/{zone_id}/history` | 30-day signal history |
| `GET` | `/api/v1/agent2/forecast/{zone_id}` | 16-day weather forecast |
| `GET` | `/api/v1/agent2/flood-forecast/{zone_id}` | 30-day GloFAS discharge forecast |
| `GET` | `/api/v1/agent2/features/{zone_id}` | Current ML feature values |
| `POST` | `/api/v1/agent2/backfill/{zone_id}` | Backfill historical signals |

### Agent 3 — Predictions
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/agent3/predict/{zone_id}` | Get 30-day flood + heat forecast |
| `GET` | `/api/v1/agent3/model/info` | Model metadata and accuracy stats |
| `POST` | `/api/v1/agent3/retrain` | Force model retraining |
| `POST` | `/api/v1/agent3/backtest` | Backtest against known flood events |

### Debater Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/debater/debate/{zone_id}` | Manually run expert debate for a zone |
| `GET` | `/api/v1/debater/last-results` | Results from the most recent debate batch |

### Agent 4 — Response Planning
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/agent4/respond/{zone_id}` | Generate a full response plan |
| `GET` | `/api/v1/agent4/last-response/{zone_id}` | Most recent response plan for a zone |
| `GET` | `/api/v1/agent4/trace/{zone_id}` | Full AI reasoning trace |

### Orchestrator
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/orchestrator/run` | Manually trigger a full orchestration cycle |
| `GET` | `/api/v1/orchestrator/status` | Last run info + next scheduled run time |
| `GET` | `/api/v1/orchestrator/logs` | All 20 stored run logs |
| `GET` | `/api/v1/orchestrator/logs/{run_id}` | Full log for a specific run |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health (scheduler, DB, WebSocket) |
| `GET` | `/metrics` | Full system metrics |
| `WS` | `/ws/signals` | Real-time signal stream |

**WebSocket filter params:**
- `?zone=karachi-korangi` — filter to a single zone
- `?min_severity=7` — only high-severity signals
- No params — receive all signals

---

## Mobile App Screens

| Screen | Description |
|--------|-------------|
| **Home** | Zone cards with live risk status, color-coded severity (red = critical, yellow = moderate, green = safe), recent alerts |
| **Agents** | Agent 2 fetch status, Agent 3 model status, full orchestrator run logs with expandable debate results and response plans |
| **Live Map** | Interactive map of all 8 zones with risk-colored pins, opens Google Maps via url_launcher |
| **Predictions** | 30-day flood + heatwave risk chart for any zone, day-by-day breakdown with confidence levels and dominant risk factors |
| **Alerts** | Chronological alert history with zone filter and severity sort |

Push notifications are sent automatically for any signal with severity ≥ 7. Tapping a notification navigates directly to that zone's prediction screen.

---

## Scheduled Jobs

| Job | Interval | Function |
|-----|----------|----------|
| Data fetch | Every 15 minutes | Agent 2 `run_fetch_cycle()` |
| AI pipeline | Every 2 hours | Orchestrator `run_cycle()` |
| Signal pruning | Daily at 3 AM UTC | `SignalStore.prune_expired()` |
| Historical backfill | Once on startup | Optional per-zone backfill |

---

## Health Check

```bash
curl http://localhost:8000/health
```

```json
{
  "status": "healthy",
  "scheduler_running": true,
  "websocket_clients": 3,
  "database": "ok",
  "last_fetch": "2025-05-21T14:00:00Z",
  "last_orchestrator_run": "2025-05-21T14:00:00Z"
}
```

---

## Limitations and Known Constraints

- **Social media and NDMA signals are simulated** — real integrations would require API access to Pakistan Telecom and NDMA feeds
- **Earth Engine quota** — GEE free tier has daily compute limits; high-frequency satellite processing may need a paid account
- **Gemini rate limits** — the debater runs 4 LLM calls per high-risk zone; under load the `gemini_retry.py` exponential backoff may add latency
- **SQLite concurrency** — suitable for single-instance deployment; swap for PostgreSQL if scaling to multiple workers
- **Prophet training time** — first run builds Prophet models for all zones; expect 2–5 minutes before days 17–30 forecasts are available

---

## License

Built for humanitarian disaster response research. Contact the project team before commercial use.
