# CIRO — Agent Specifications

This document defines the role, data contracts, communication patterns,
and implementation status of each agent in the CIRO multi-agent system.

> **Note:** This document should be read before any code is written.
> It is the authoritative reference for inter-agent contracts.

***

## System Overview

```
[Open-Meteo] [GloFAS] [OWM] [Traffic] [NDMA*] [Social*]
       |           |      |       |        |        |
       +-----+-----+------+-------+--------+--------+
             |
       [Agent 2: Data Collector]
             | SQLite signals.db
             |
       [Agent 3: ML Predictor] <---[Agent 1: Imagery (GEE/GeoGemma)]
             |                              *PLANNED
             | prediction events (flood_risk > threshold)
             |
       [Agent 4: Orchestrator]
             |         |
      [DebaterAgent]  [ResponseAgent]
             |         |
          [Alerts] [Evacuation Routes]
             |
       [Flutter App] [Web Dashboard] [FCM Push]

* = Simulated in v1
```

***

## Agent 1 — Imagery Agent

**File:** `backend/agents/agent_imagery.py`  
**Class:** `ImageryAgent`  
**Status:** PLANNED (stub with mock output)

**Purpose:**  
Analyses satellite imagery via Google Earth Engine (GEE) and GeoGemma
to detect current flood extent, surface water anomalies, and infrastructure damage.

**Inputs:**
- Zone bounding box (lat/lng)
- Date range (last 7 days)
- GEE credentials (EE_PROJECT_ID env var)

**Outputs:**
```json
{
  "zone_id": "karachi-south",
  "flood_extent_km2": 12.4,
  "surface_water_pct": 34.2,
  "anomaly_score": 0.78,
  "imagery_date": "2026-05-21",
  "confidence": "MODERATE"
}
```

**APIs Used:**
- Google Earth Engine Python API (earthengine-api==0.1.415)
- GeoGemma (via google-generativeai)
- Sentinel-1 SAR Collection (via GEE)

**Trigger:** Daily cron at 06:00 PKT + on-demand via Orchestrator

**Communication:** Called directly by Agent 4 (Orchestrator) — tight coupling
justified because imagery is synchronous and Orchestrator owns the full pipeline.

***

## Agent 2 — Data Collector

**File:** `backend/agents/agent_data_collector.py`  
**Router:** `APIRouter(prefix="/api/v1/agent2")`  
**Status:** ACTIVE (stub endpoints, services layer complete)

**Purpose:**  
Continuously ingests real-time signals from 6 data sources, normalises them,
deduplicates via signal_hash, stores to SQLite, and broadcasts via WebSocket.

**Inputs:**
- Open-Meteo API (free, no key) — ECMWF/GFS weather + GloFAS discharge
- OpenWeatherMap API (OPENWEATHER_API_KEY) — verification layer
- Google Maps Traffic API (GOOGLE_MAPS_API_KEY) — road disruptions
- NDMA advisories (simulated in v1)
- Social signals — WhatsApp/Twitter crisis mentions (simulated in v1)

**Outputs (SQLite schema):**
```sql
CREATE TABLE signals (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  zone_id TEXT NOT NULL,
  source TEXT NOT NULL,
  signal_type TEXT NOT NULL,
  value REAL,
  confidence REAL DEFAULT 0.5,
  timestamp TEXT NOT NULL,
  signal_hash TEXT UNIQUE NOT NULL,
  raw_json TEXT
);
```

**Deduplication Strategy:**
```
signal_hash = SHA256(zone_id + source + signal_type + floor(timestamp / 900s))
```
Rounds timestamps to the nearest 15-minute window before hashing.
INSERT OR IGNORE ensures no duplicate signals even if the scheduler fires twice.

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Agent health + active zone count |
| POST | /fetch | Manually trigger one full fetch cycle |
| POST | /backfill/{zone_id} | Backfill historical data for a zone |
| GET | /signals/{zone_id} | Recent signals for a zone (last 24h) |
| GET | /features/{zone_id} | Aggregated ML feature vector |
| GET | /forecast/{zone_id} | 16-day Open-Meteo forecast |
| GET | /flood-forecast/{zone_id} | 30-day GloFAS discharge forecast |
| GET | /zones | List all 8 monitored zone IDs |

**Trigger:** APScheduler every 15 minutes via `setup_scheduler()` in services/scheduler.py

***

## Agent 3 — ML Predictor

**File:** `backend/agents/agent_predictor.py`  
**Router:** `APIRouter(prefix="/api/v1/agent3")`  
**Status:** ACTIVE (stub endpoints, model architecture defined)

**Purpose:**  
Produces 30-day flood risk and heatwave risk predictions per zone using a
two-model ensemble: XGBoost for days 1-16 (deterministic) and Prophet for
days 17-30 (statistical climatology).

**Model 1 — XGBoost Flood Classifier:**
- Training samples: 1,572
- Flood events: 60 (positive class)
- Features: temp_avg, temp_max, precip_monthly_cumulative, month,
  province_encoded, antecedent_moisture (30-day rolling precip)
- GloFAS modulation: daily discharge multiplied into flood probability
- Accuracy: 0.94 F1 score on held-out test set

**Model 2 — Prophet Weather Forecaster:**
- 12 models: 6 provinces x (temperature + rainfall)
- Training data: 22 years GEE daily observations
- Used for: days 17-30 (beyond deterministic NWP horizon)
- Output: temp_c and precip_mm daily forecasts

**Output Schema:**
```json
{
  "zone_id": "lahore-city",
  "prediction_days": 30,
  "generated_at": "2026-05-21T04:30:00Z",
  "flood_risk": [
    {"day": 1, "date": "2026-05-21", "risk": 0.12, "confidence": "HIGH",
     "discharge_m3s": 450.2},
    ...
  ],
  "heat_risk": [
    {"day": 1, "date": "2026-05-21", "risk": 0.05, "temp_max_c": 38.2},
    ...
  ],
  "model_used": {"days_1_16": "xgboost", "days_17_30": "prophet"}
}
```

**Confidence Tiers:**
- HIGH: Days 1-7 (deterministic NWP + real-time discharge)
- MODERATE: Days 8-16 (NWP + statistical modulation)
- LOW: Days 17-30 (Prophet climatology only)

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | /status | Model load status (xgboost/prophet) |
| POST | /predict/{zone_id} | Generate 30-day forecast |
| GET | /model/info | Training metadata + accuracy |
| POST | /backtest | Run historical accuracy test |

***

## Agent 4 — Orchestrator

**File:** `backend/agents/agent_orchestrator.py`  
**Class:** `CIROOrchestrator`  
**Status:** PLANNED (stub with mock output)

**Purpose:**  
The master coordination agent. Receives predictions from Agent 3, imagery from
Agent 1, runs DebaterAgent for high-risk zones, and dispatches alerts via ResponseAgent.

**Trigger Strategy (chosen: Option C — hybrid):**
- Scheduled: every 2 hours via APScheduler
- Event-driven: whenever Agent 3 prediction returns flood_risk > 0.30
- Rationale: Scheduled ensures freshness for demo; event-driven ensures no
  critical alerts are missed between cycles

**Coupling Strategy (chosen: Option A — direct import):**
- Orchestrator imports Agent 3 functions directly (not via HTTP)
- Rationale: Avoids network hop latency, simpler error handling,
  acceptable for single-process hackathon deployment

**Sub-Agents Called:**
1. `DebaterAgent.debate(zone_id, prediction)` — for zones with risk > 0.30
2. `ResponseAgent.generate_response(zone_id, consensus)` — for confirmed alerts

**Output:**
```json
{
  "orchestration_id": "orch-20260521-0430",
  "zones_assessed": 8,
  "high_risk_zones": ["jacobabad-city", "sukkur-city"],
  "alerts_dispatched": 2,
  "debate_triggered": true,
  "consensus": "EVACUATE",
  "routes": [...]
}
```

***

## DebaterAgent (Sub-Agent of Orchestrator)

**File:** `backend/agents/agent_debater.py`  
**Class:** `DebaterAgent`  
**Status:** PLANNED (stub with mock debate transcript)

**Purpose:**  
Reduces false positives by simulating a multi-persona expert debate before
any alert is dispatched. Only fires when flood_risk > RISK_ALERT_THRESHOLD.

**Personas:**
- Hydrologist: Evaluates river discharge and antecedent moisture
- Meteorologist: Evaluates atmospheric pressure and precipitation forecast
- Emergency Coordinator: Weighs population density and evacuation feasibility

**Output:** Structured debate transcript + consensus score + final decision

***

## ResponseAgent (Sub-Agent of Orchestrator)

**File:** `backend/agents/agent_response.py`  
**Class:** `ResponseAgent`  
**Status:** PLANNED (stub with mock routes)

**Purpose:**  
Generates actionable emergency response packages: evacuation routes,
SMS message drafts, FCM push notification payloads.

**Output:**
```json
{
  "zone_id": "sukkur-city",
  "evacuation_routes": [...],
  "sms_draft": "CIRO ALERT: Flood risk HIGH in Sukkur...",
  "fcm_payload": {...}
}
```

***

## Inter-Agent Communication Contracts

| From | To | Method | When |
|------|-----|--------|------|
| Scheduler | Agent 2 | Direct call | Every 15 min |
| Agent 2 | SignalStore | Direct call | After each fetch |
| SignalStore | WebSocketManager | Direct call | After each insert |
| Agent 4 | Agent 3 | Direct import | Every 2h + event |
| Agent 4 | Agent 1 | Direct import | Every 2h |
| Agent 4 | DebaterAgent | Direct import | When risk > 0.30 |
| DebaterAgent | GeminiRetryClient | Direct call | Per debate |
| Agent 4 | ResponseAgent | Direct import | After consensus |
