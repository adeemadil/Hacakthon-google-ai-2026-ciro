# CIRO — User Stories

**Format:** As a [role], I want to [action] so that [outcome].  
**Priority:** P0 = Must have for hackathon demo | P1 = Should have | P2 = Nice to have

***

## Epic 1: Crisis Prediction

**US-001** [P0]  
As an NDMA operator, I want to see a 30-day flood risk forecast for any of the 8 monitored
cities so that I can pre-position emergency resources before a crisis hits.

**Acceptance Criteria:**
- /api/v1/agent3/predict/{zone_id} returns 30 daily risk scores
- Each score includes a confidence tier (HIGH/MODERATE/LOW)
- Days 1-7 labeled HIGH confidence, 8-16 MODERATE, 17-30 LOW
- Response time < 2 seconds

***

**US-002** [P0]  
As an NDMA operator, I want to see heatwave risk alongside flood risk so that I can
distinguish between two distinct crisis types affecting the same zone.

**Acceptance Criteria:**
- heat_risk array returned alongside flood_risk
- Jacobabad and Sukkur zones show elevated heatwave baselines (historically hottest)
- Risk score between 0.0 and 1.0

***

**US-003** [P1]  
As a provincial coordinator, I want to see which data sources are currently active
so that I know whether the prediction is based on fresh or cached data.

**Acceptance Criteria:**
- /api/v1/agent2/status returns per-source last_updated timestamps
- Stale data (>30 min old) flagged with a warning indicator

***

## Epic 2: Real-Time Data Ingestion

**US-004** [P0]  
As the system, I want to automatically fetch weather and river data every 15 minutes
so that predictions are always based on the most recent available signals.

**Acceptance Criteria:**
- APScheduler fires every 15 minutes
- All 6 data sources polled per cycle
- Duplicate signals rejected via signal_hash (INSERT OR IGNORE)
- New signals broadcast to all connected WebSocket clients

***

**US-005** [P1]  
As a developer, I want to manually trigger a data backfill for any zone so that I can
populate historical data for a newly added city without waiting for scheduled cycles.

**Acceptance Criteria:**
- POST /api/v1/agent2/backfill/{zone_id} accepts a days parameter
- Returns number of days successfully backfilled
- Idempotent — running twice produces no duplicates

***

## Epic 3: Alert Dispatch

**US-006** [P0]  
As a resident in a high-risk zone, I want to receive a push notification on my phone
when flood risk exceeds 30% so that I have enough time to evacuate safely.

**Acceptance Criteria:**
- FCM notification triggers when flood_risk > settings.RISK_ALERT_THRESHOLD (0.30)
- Notification includes zone name, risk level, and recommended action
- No duplicate notifications for the same event within 2 hours

***

**US-007** [P1]  
As an emergency coordinator, I want the system to propose evacuation routes that avoid
flooded roads so that I can communicate actionable directions to field teams.

**Acceptance Criteria:**
- Agent 4 ResponseAgent returns at least 1 alternative route per affected zone
- Route excludes roads flagged by TrafficService as disrupted
- Output format: list of waypoints with estimated travel time

***

## Epic 4: Transparency & Explainability

**US-008** [P0]  
As a hackathon reviewer, I want to see the AI reasoning process behind a HIGH-risk
alert so that I can verify the system isn't a black box.

**Acceptance Criteria:**
- DebaterAgent produces a visible debate transcript with 3 personas
  (Hydrologist, Meteorologist, Emergency Coordinator)
- Each persona provides a named argument for or against the alert
- Final consensus decision and confidence score shown

***

**US-009** [P1]  
As an NDMA operator, I want to see model performance metrics so that I can judge
whether to trust the prediction.

**Acceptance Criteria:**
- /api/v1/agent3/model/info returns xgboost_accuracy, training_samples, prophet_provinces
- Accuracy displayed on the dashboard

***

## Epic 5: Dashboard & Monitoring

**US-010** [P0]  
As any user visiting the web dashboard, I want to see the live status of all agents
and current risk levels for all 8 zones on a single screen so that I get an immediate
situational overview.

**Acceptance Criteria:**
- Dashboard loads in < 1 second (static HTML, no JS fetch)
- Shows Agent 2 and Agent 3 status (active/inactive badge)
- Shows all 8 zone names with current risk placeholder
- Pulsing LIVE indicator visible

***

**US-011** [P1]  
As a mobile user, I want to open the Flutter app and see a map of Pakistan with
risk indicators overlaid on each monitored city so that I can visually identify
the most dangerous zones.

**Acceptance Criteria:**
- Google Maps widget loads centred on Pakistan
- 8 markers placed at exact city coordinates
- Marker colour reflects risk level (green/amber/red)

***

## Epic 6: Developer Experience

**US-012** [P0]  
As a developer, I want to run the entire backend with a single docker run command
so that setup takes under 5 minutes on any machine.

**Acceptance Criteria:**
- docker build + docker run works from a clean clone
- /health endpoint returns 200 with {"status": "ok"}
- All environment variables documented in .env.example

***

**US-013** [P1]  
As a developer, I want to run download_data.py to seed the training data directory
so that model training can begin immediately after setup.

**Acceptance Criteria:**
- Script is idempotent (safe to run twice)
- Creates backend/data/training/ structure
- Prints progress for each of the 6 provinces
