# Agent 2 — Data Collector (CIRO)

## Purpose
Agent 2 handles high-frequency, real-time data collection across 8 target cities in Pakistan:
- Karachi
- Lahore
- Islamabad
- Peshawar
- Quetta
- Multan
- Faisalabad
- Muzaffarabad

Its primary objective is to ingest, parse, validate, and store raw environmental, public, and official telemetry data to build high-fidelity features for the predictive models in Agent 3.

---

## Data Sources
Agent 2 integrates with a diverse array of premium APIs and simulated streams:
1. **Open-Meteo API**: Utilizes ECMWF (European Centre for Medium-Range Weather Forecasts) and GFS (Global Forecast System) data for daily high-resolution weather variables.
2. **GloFAS (Global Flood Awareness System)**: Direct access to river discharge telemetry to monitor flow thresholds.
3. **OpenWeatherMap API**: Provides high-frequency, current local weather metrics for immediate validation.
4. **Google Maps Traffic API**: Monitors logistical and infrastructural blockages near main arterial roads in urban centers.
5. **NDMA / PDMA (Simulated)**: Ingests official government pre-monsoon warnings, emergency advisories, and risk bulletins.
6. **Social Signal Stream (Simulated)**: Extracts crowd-sourced crisis indicators (e.g., local Twitter/X and WhatsApp tips) regarding flooding or extreme heat waves.

---

## SQLite Database Schema
Telemetry and raw signals are persistent in the local `data/signals.db` file.

### `signals` Table Schema
```sql
CREATE TABLE IF NOT EXISTS signals (
    id TEXT PRIMARY KEY,
    zone_id TEXT NOT NULL,
    source TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    data TEXT NOT NULL,
    confidence REAL NOT NULL
);
```

### Deduplication Strategy
To manage redundant data fetches and maintain absolute data integrity, the system applies an `INSERT OR IGNORE` strategy. An index is declared on `(zone_id, timestamp)` to ensure query operations remain fast as the signal stream grows.

---

## Scheduler Configuration
CIRO runs a background scheduling agent powered by `APScheduler` (`AsyncIOScheduler`).
- **Interval**: Triggers every **15 minutes**.
- **Execution Flow**:
  1. Spawns asynchronous tasks to call all 6 data sources simultaneously.
  2. Parses JSON responses into structured signals.
  3. Inserts records into the SQLite store (applying deduplication).
  4. Triggers Agent 3 predictions if thresholds are breached.

---

## Real-Time Websocket Updates
Upon every completed fetch cycle, the scheduler leverages the `WebSocketManager` to broadcast the newly collected signals instantly to all active client connections (such as the Flutter client application or web board).

---

## API Endpoints (`/api/v1/agent2/*`)

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/status` | Returns the health and active monitoring state of Agent 2. |
| `POST` | `/fetch` | Manually triggers a real-time fetch cycle across all 8 zones. |
| `POST` | `/backfill/{zone_id}` | Triggers historical data ingestion for model retraining. |
| `GET` | `/signals/{zone_id}` | Retrieves raw ingested signals within a window. |
| `GET` | `/features/{zone_id}` | Retrieves processed features prepared for the ML model. |
| `GET` | `/forecast/{zone_id}` | Retrieves the 16-day weather forecast from Open-Meteo. |
| `GET` | `/flood-forecast/{zone_id}`| Retrieves the 30-day river discharge forecast from GloFAS. |
| `GET` | `/zones` | Returns the list of the 8 monitored cities. |
