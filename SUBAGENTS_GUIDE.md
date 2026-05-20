# CIRO — Sub-Agent Usage in Antigravity IDE

## What Are Sub-Agents in Antigravity?

In Antigravity, sub-agents are specialised AI instances spawned by the
primary agent to handle specific subtasks in parallel. When you see entries
like "Planning Sub-Agent", "File Creation Sub-Agent", or "Verification Sub-Agent"
in the Antigravity trace logs, those ARE sub-agents at work.

The key insight: **sub-agents are triggered by task complexity and ambiguity,
not by explicit instruction.** The prompts in this repo are designed to
produce sub-agent traces organically by structuring tasks with enough
reasoning complexity that Antigravity cannot complete them in a single pass.

***

## Sub-Agents Observed in CIRO Build

### Phase 1 (Prompt 1) — Architecture Planning
Antigravity spawned:
- `Planning Sub-Agent` — analysed 30-day prediction problem space
- `Architecture Sub-Agent` — designed 4-agent topology
- `Risk Analysis Sub-Agent` — identified 3 technical risks
- `File Creation Sub-Agent` — created README, .gitignore, Dockerfile, .env.example

Artifacts produced: `implementation_plan.md`, `task.md`, `walkthrough.md`

### Phase 2 (Prompt 2) — Backend Core
Antigravity spawned:
- `Compatibility Analysis Sub-Agent` — checked XGBoost/Prophet/pandas versions
- `Architecture Decision Sub-Agent` — decided on grace startup vs hard fail
- `File Creation Sub-Agent` — created all 5 core backend files

### Phase 3 (Prompt 3) — Agents Layer
Antigravity spawned:
- `Design Debate Sub-Agent` — reasoned through 3 coupling tensions
- `Code Generation Sub-Agent` — created all 6 agent files
- `Verification Sub-Agent` — validated all files importable

### Phases 4-5 — Services + Frontend
- `Data Flow Sub-Agent` — drew signal ingestion diagram
- `Hashing Strategy Sub-Agent` — determined signal_hash algorithm
- `Frontend Layout Sub-Agent` — decided information hierarchy

***

## How to Maximise Sub-Agent Traces

### Technique 1: Force explicit reasoning BEFORE action
The prompts in this repo always ask Antigravity to "reason through X before
creating files." This ensures the planning sub-agents fire and produce
visible trace entries rather than being skipped.

BAD (no sub-agents triggered):
  "Create backend/services/signal_store.py with these methods..."

GOOD (planning sub-agents triggered):
  "Before creating signal_store.py, explain what the signal_hash should
  be computed from and why. Then create the file."

### Technique 2: Introduce genuine design tensions
Asking "Option A vs Option B — which is better?" forces Antigravity to spawn
a reasoning sub-agent that evaluates both options. This shows up in the trace.

### Technique 3: Ask for artifacts alongside code
Asking for "a structured implementation plan" or "a text-based data flow diagram"
alongside file creation causes Antigravity to maintain multiple parallel tracks —
artifact generation and code generation — which typically involves separate sub-agents.

### Technique 4: Request verification as a separate step
The final line "verify the complete structure matches exactly" in Prompt 6 triggers
a dedicated verification sub-agent that walks the file tree independently.

***

## Prompt 7 — Activating Real Implementation Sub-Agents

After the scaffold is committed, use this pattern to activate Antigravity's
code generation sub-agents for the real implementation:

```
Now implement the real XGBoost training pipeline in Agent 3.

Before writing any code, I want you to:
1. Review the existing agent_predictor.py stub — what are the current
   placeholder return values and what real logic needs to replace them?
2. Review services/signal_store.py get_features() — what feature vector
   does it currently return and is that compatible with what XGBoost expects?
3. Identify any pandas 2.x compatibility issues with the current Prophet
   model loading pattern.

Then implement:
backend/agents/agent_predictor.py — replace the predict/{zone_id} stub
with real XGBoost inference:
- Load model from backend/models/xgboost_flood.joblib
- Call signal_store.get_features(zone_id) to get the feature vector
- Run model.predict_proba() and return calibrated probabilities
- For days 17-30, call weather_forecaster.forecast_rainfall() and
  forecast_temperature() to get Prophet projections
- Return the full 30-day risk array with confidence tiers

Show your compatibility analysis first, then implement.
```

This pattern — analyse existing code + identify issues + implement — reliably
produces 3-4 sub-agent traces per prompt and is the correct way to use
Antigravity for iterative implementation rather than greenfield scaffolding.

***

## Token Budget Guide for CIRO Completion

Remaining implementation tasks and estimated token cost at gemini-2.0-flash rates:

| Task | Estimated Tokens | Notes |
|------|-----------------|-------|
| Prompt 6 (docs + verify) | ~15K | Current step |
| XGBoost real inference | ~20K | Replace stub in agent_predictor.py |
| Prophet integration | ~18K | weather_forecaster.py real logic |
| GloFAS HTTP calls | ~12K | openmeteo_service.py real HTTP |
| Agent 4 real orchestration | ~25K | Most complex — full pipeline |
| DebaterAgent Gemini calls | ~20K | 3-persona debate logic |
| Flutter risk map integration | ~15K | Connect API to GoogleMap markers |
| Demo data fixtures | ~8K | Seed realistic Pakistani data |
| **Total estimate** | **~133K tokens** | At $0.075/1M = ~$0.01 total |

At these costs, the full remaining implementation costs well under $1 in Flash tokens.
The only expensive model to avoid is gemini-1.5-pro (~15x more expensive).
