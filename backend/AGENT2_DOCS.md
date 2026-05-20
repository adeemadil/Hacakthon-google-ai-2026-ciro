# CIRO Multi-Agent Architecture: Agent 2 — Real-Time Telemetry Data Collector

## 1. Operational Purpose
Agent 2 operates as the persistent real-time data collection and ingestion engine for the Crisis Intelligence & Response Orchestrator (CIRO). It manages high-frequency telemetry harvesting across **8 critical geographic zones** in Pakistan representing high-risk areas across 5 provinces:
1. `islamabad-g10` (Capital Territory)
2. `lahore-city` (Punjab)
3. `karachi-south` (Sindh)
4. `peshawar-city` (Khyber Pakhtunkhwa)
5. `multan-city` (Punjab)
6. `jacobabad-city` (Sindh)
7. `sukkur-city` (Sindh)
8. `quetta-city` (Balochistan)

By continuously sourcing, validating, and structuring atmospheric, hydrological, municipal, and crowdsourced streams, Agent 2 populates the underlying features that feed the predictive ML engines in Agent 3.

---

## 2. Integrated Data Sources
The ingestion layer standardizes telemetry from 6 distinct real-time APIs and simulated feeds:

| Source Name | Ingestion Method | Telemetry Ingested | Mode |
| :--- | :--- | :--- | :--- |
| **Open-Meteo (ECMWF/GFS)** | HTTPS REST API | High-resolution daily pressure, temperature vectors, relative humidity, wind velocity, and 16-day cumulative rainfall forecast. | **Real** |
| **GloFAS (Copernicus)** | API Polling | Medium-range 30-day river discharge simulation projections ($m^3/s$) for major river basins in Pakistan. | **Real** |
| **OpenWeatherMap** | Live HTTP Client | Immediate local current temperature ($^\circ C$), pressure ($hPa$), humidity ($[\%]$), and local cloud cover parameters. | **Real** |
| **Google Maps Traffic API** | Scraped Geolocation | Arterial road velocity delays and traffic bottlenecks surrounding main urban centers to identify escape route disruptions. | **Real** |
| **NDMA & PDMA Bulletins** | Simulated Push Stream | Ingestion of official government pre-monsoon warnings, emergency high-water level alerts, and disaster response staging triggers. | **Simulated** |
| **Social Signals Stream** | Simulated NLP Parse | Raw crisis indicators (e.g., local WhatsApp alerts, geotagged X/Twitter reports) referencing flash floods, severe waterlogging, or heatwave conditions. | **Simulated** |

---

## 3. SQLite Ingestion & Schema Design
To support low-footprint deployment, high read concurrency, and resilience during network dropouts, telemetry is persisted in a local SQLite database (`backend/data/signals.db`).

### Schema Definition
```sql
CREATE TABLE IF NOT EXISTS signals (
    signal_hash TEXT PRIMARY KEY,   -- Idempotent SHA-256 fingerprint (UNIQUE)
    zone_id TEXT NOT NULL,          -- Targeted city/zone identifier
    source TEXT NOT NULL,           -- Telemetry source identifier
    timestamp TEXT NOT NULL,        -- ISO-8601 UTC timestamp of ingestion
    data TEXT NOT NULL,             -- JSON stringified payload of telemetry variables
    confidence REAL NOT NULL        -- Source/channel confidence weight (0.0 to 1.0)
);

-- Optimize spatio-temporal indexes for low-latency client dashboard requests
CREATE INDEX IF NOT EXISTS idx_signals_zone_time ON signals(zone_id, timestamp);
```

### Signal Hash Deduplication Engine
To ensure exact-once processing and defend against network failures or duplicate scheduler cycles, Agent 2 computes an idempotent SHA-256 fingerprint for every inbound signal:

$$\text{signal\_hash} = \text{SHA256}(\text{zone\_id} \mathbin{\Vert} \text{"\_"} \mathbin{\Vert} \text{source} \mathbin{\Vert} \text{"\_"} \mathbin{\Vert} \text{rounded\_timestamp\_str})$$

Where `rounded_timestamp_str` represents the signal's ISO-8601 timestamp rounded to the nearest **15-minute boundary**. 
* Any overlapping fetch cycle targeting the same city and source within that 15-minute window generates an identical signature.
* During database writes, the system executes an `INSERT OR IGNORE` transaction, rejecting the redundant payload without throwing database exceptions or corrupting feature history.

---

## 4. Background Scheduler Architecture
Ingestion cycles are managed by a persistent daemon leveraging `APScheduler` (`AsyncIOScheduler`) embedded within the FastAPI application lifecycle:

* **Frequency**: Runs on a strict **15-minute interval**.
* **Ingestion Flow**:
  1. Scheduler fires and initializes concurrent asynchronous fetch coroutines for all 8 zones and all 6 data sources.
  2. Network inputs are channeled through `RetryClient` using exponential backoff to handle external rate limiting.
  3. Response payloads are normalized, validated, and annotated with a confidence rating.
  4. The deduplicated signals are written to the database via `INSERT OR IGNORE`.
  5. The active `WebSocketManager` broadcasts the fresh signal payloads to all connected Flutter dashboards.
  6. If signal levels exceed safe thresholds (e.g., rainfall $> 50mm$ or temperature $> 43^\circ C$), a direct execution request is dispatched to Agent 3 (ML Predictor).

---

## 5. Real-Time WebSocket Gateway
Upon successful completion of any collection cycle, Agent 2 leverages a global `WebSocketManager` to broadcast signals to `/ws/signals`. Connected Flutter dashboards ingest the JSON stream in real-time, refreshing widgets and geographical overlays instantly without polling the API endpoints.

---

## 6. API Endpoint Routing (`/api/v1/agent2/*`)

Agent 2 exposes 8 specialized REST endpoints for telemetry queries, historical backfilling, and monitoring:

### 1. `GET` `/api/v1/agent2/status`
* **Description**: Returns the active operational state of the collector, the count of monitored zones, and active thread statuses.
* **Response**:
  ```json
  {"agent": "DataCollector", "status": "active", "zones": 8}
  ```

### 2. `POST` `/api/v1/agent2/fetch`
* **Description**: Triggers a manual, out-of-band ingestion sweep across all 6 data sources for all 8 zones (primarily used for demo runs and judge evaluations).
* **Response**:
  ```json
  {"message": "Fetch cycle triggered", "zones_processed": 8}
  ```

### 3. `POST` `/api/v1/agent2/backfill/{zone_id}`
* **Description**: Requests historical data backfill for a specific zone across an arbitrary range of days, pulling historic Open-Meteo coordinates to seed predictive training sets.
* **Parameters**: `days` (Query, default: 30)
* **Response**:
  ```json
  {"zone": "karachi-south", "days_backfilled": 30}
  ```

### 4. `GET` `/api/v1/agent2/signals/{zone_id}`
* **Description**: Retrieves recent raw ingested signals (social feeds, NDMA alerts, current weather) for a specific zone within the past 24 hours.
* **Response**:
  ```json
  {"zone": "lahore-city", "signals": [...], "count": 24}
  ```

### 5. `GET` `/api/v1/agent2/features/{zone_id}`
* **Description**: Exposes preprocessed and mathematically aggregated feature vectors engineered for immediate machine learning ingestion.
* **Response**:
  ```json
  {
    "zone_id": "islamabad-g10",
    "temp_mean_24h": 32.8,
    "precip_sum_24h": 4.2,
    "river_discharge_mean_24h": 155.0,
    "antecedent_moisture_index": 0.45,
    "ndma_alert_active": 0
  }
  ```

### 6. `GET` `/api/v1/agent2/forecast/{zone_id}`
* **Description**: Retrieves the raw 16-day weather forecast variables from the Open-Meteo GFS/ECMWF api for geographical coordinate overlays.
* **Response**:
  ```json
  {"zone": "quetta-city", "forecast_days": 16, "data": [...]}
  ```

### 7. `GET` `/api/v1/agent2/flood-forecast/{zone_id}`
* **Description**: Exposes Copernicus-derived 30-day river discharge simulation projections ($m^3/s$) for flood risk modeling.
* **Response**:
  ```json
  {"zone": "sukkur-city", "discharge_days": 30, "data": [...]}
  ```

### 8. `GET` `/api/v1/agent2/zones`
* **Description**: Returns the active geographic configuration of the 8 monitored cities across Pakistan's 5 administrative provinces.
* **Response**:
  ```json
  {"zones": ["islamabad-g10", "lahore-city", "karachi-south", "peshawar-city", "multan-city", "jacobabad-city", "sukkur-city", "quetta-city"]}
  ```
