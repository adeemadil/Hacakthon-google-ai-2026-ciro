# CIRO — Product Requirements Document (PRD)

**Version:** 1.0  
**Date:** May 2026  
**Challenge:** Google Antigravity Hackathon — Challenge 3: Crisis Intelligence  
**Team:** CIRO Dev Team  
**Status:** Active Development

***

## 1. Executive Summary

CIRO (Crisis Intelligence & Response Orchestrator) is a 4-agent AI system that provides
30-day forward-looking flood and heatwave risk assessment for 8 Pakistani cities across
5 provinces. The system ingests real-time weather, river discharge, satellite, and social
signals, processes them through XGBoost + Prophet ML models, and dispatches structured
alerts to emergency responders and the public via a Flutter mobile app and WebSocket dashboard.

***

## 2. Problem Statement

Pakistan's 2022 monsoon floods killed 1,739 people, displaced 33 million, and caused
$30B USD in damages. Existing early warning systems provide only 24-48 hour windows —
insufficient for meaningful evacuation planning. The gap is not data; it's intelligence:
the ability to fuse multi-source signals and reason forward 30 days with calibrated confidence.

**Target Users:**
- Primary: NDMA (National Disaster Management Authority) operators
- Secondary: Provincial emergency coordinators (Punjab, Sindh, KP, Balochistan, GB)
- Tertiary: General public in high-risk zones via mobile alerts

***

## 3. Goals & Success Metrics

| Goal | Metric | Target |
|------|--------|--------|
| 30-day prediction horizon | Days of reliable forecast | 30 days (vs 2-day baseline) |
| Prediction accuracy | XGBoost flood classifier F1 | >0.90 |
| Coverage | Pakistani cities monitored | 8 cities, 5 provinces |
| Latency | Time from signal ingestion to alert | <15 minutes |
| Reliability | Uptime during monsoon season | >99% |
| Alert precision | False positive rate | <10% (via LLM debate layer) |

***

## 4. Agent Architecture

### Agent 1 — Imagery Agent (GeoGemma + GEE) [PLANNED]
- **Input:** Google Earth Engine satellite tiles, Sentinel-1 SAR
- **Output:** Flood extent polygons, surface water anomaly scores
- **Trigger:** Daily at 06:00 PKT + on demand
- **Status:** Stub implemented, integration pending GEE auth

### Agent 2 — Data Collector (Real-time Ingestion)
- **Input:** Open-Meteo API, GloFAS river discharge, OpenWeatherMap,
  Google Maps Traffic, NDMA advisories (simulated), social signals (simulated)
- **Output:** Normalised signals stored in SQLite with deduplication
- **Trigger:** APScheduler every 15 minutes
- **Status:** Fully stubbed, service layer complete

### Agent 3 — ML Predictor (XGBoost + Prophet)
- **Input:** Feature vectors from SignalStore (temp, precip, discharge, antecedent moisture)
- **Output:** 30-day flood risk + heatwave risk arrays per zone with confidence tiers
- **Model:** XGBoost (days 1-16), Prophet (days 17-30)
- **Status:** Model architecture complete, training pipeline ready

### Agent 4 — Orchestrator (Alert Dispatch + Routing) [PLANNED]
- **Input:** Agent 3 predictions, Agent 1 imagery, DebaterAgent consensus
- **Output:** Structured evacuation routes, SMS alerts, FCM push notifications
- **Trigger:** Every 2 hours + event-driven when flood_risk > 0.30
- **Status:** Stub implemented with mock output

***

## 5. Non-Functional Requirements

- **Stack:** Python 3.11, FastAPI 0.115, XGBoost 2.1, Prophet 1.1.5, SQLite, Flutter, Docker
- **Deployment:** Docker container, Railway/Cloud Run compatible
- **API Rate Limits:** Open-Meteo (free tier), GloFAS (free), Gemini (pay-per-token)
- **Offline Resilience:** All agents fall back to cached data on API failure
- **Security:** API keys via environment variables only, never committed to repo

***

## 6. Out of Scope (v1)

- Real NDMA API integration (simulated in v1)
- Real social media scraping (simulated in v1)
- Agent 1 GEE full integration (stubbed)
- Multi-language UI (English only for hackathon)
- User authentication

***

## 7. Milestones

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 0 | Architecture plan + PRD | Done |
| 1 | Root config files (README, .gitignore, Dockerfile) | Done |
| 2 | Backend core (main.py, settings, requirements) | Done |
| 3 | Agents layer (6 files) | Done |
| 4 | Services layer (11 files) | Done |
| 5 | Frontend (dashboard + Flutter app) | Done |
| 6 | Docs + verification + commit | In Progress |
| 7 | PowerShell swap (real code from Fuckathon repo) | Pending |
| 8 | Demo video recording | Pending |
