CIRO — Crisis Intelligence & Response Orchestrator
Multi-Agent AI System for Urban Crisis Prediction & Response in Pakistan

[
[
[
[
[
[

CIRO is a 4-agent AI system that predicts and responds to urban crises
(floods and heatwaves) in Pakistan using Prophet + XGBoost + Open-Meteo

GloFAS, providing 30-day forward-looking crisis risk assessment for
8 cities across 5 provinces.

Agents:

Agent 2 (Data Collector): Open-Meteo, GloFAS, traffic, social, NDMA

Agent 3 (ML Predictor): XGBoost flood classifier + Prophet weather forecast

Agent 1 (Imagery): GeoGemma + GEE — PLANNED

Agent 4 (Orchestrator): Alert dispatch + routing — PLANNED

Tech: Python FastAPI, XGBoost, Prophet, SQLite, WebSocket, Flutter, Docker
