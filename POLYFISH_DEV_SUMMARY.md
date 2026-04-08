# PolyFish Dev Summary

## What PolyFish is

PolyFish is a full-stack app that turns a live Polymarket market into:

1. a structured ontology
2. a Zep knowledge graph
3. a multi-agent social simulation
4. a written investment/thesis-style report
5. an interactive post-run analysis surface

The stack is:

- Frontend: Vue SPA in `frontend/src`
- Backend: Flask API in `backend/app`
- Graph / memory layer: Zep Cloud
- LLM layer: OpenAI-compatible API endpoint
- Market data source: Polymarket Gamma API
- Simulation runtime: OASIS-style Twitter/Reddit simulation scripts


## High-Level Flow

The product pipeline is:

`Polymarket market -> ontology -> graph -> agent profiles + sim config -> simulation run -> report -> interaction`

In practice:

1. User selects a live market on the landing page.
2. Frontend sends the market + simulation brief to the backend.
3. Backend pulls live market metadata from Polymarket.
4. Backend asks the LLM to generate an ontology for that market context.
5. Backend chunks the market seed text and builds a Zep graph.
6. Backend reads filtered entities from the graph.
7. Backend generates social-agent profiles and simulation parameters.
8. Backend runs the simulation across two platform archetypes.
9. Backend generates a report using Zep-backed retrieval.
10. User explores the report and chats with simulated agents / the report agent.


## Frontend Structure

Main frontend files:

- `frontend/src/views/Home.vue`
- `frontend/src/views/MainView.vue`
- `frontend/src/components/Step1GraphBuild.vue`
- `frontend/src/components/Step2EnvSetup.vue`
- `frontend/src/components/Step3Simulation.vue`
- `frontend/src/components/Step4Report.vue`
- `frontend/src/components/Step5Interaction.vue`
- `frontend/src/api/*.js`
- `frontend/src/router/index.js`

### Frontend routing

- `/`
  - landing page and market selection
- `/process/:projectId`
  - graph build + simulation prep workflow
- `/simulation/:simulationId`
  - simulation setup view
- `/simulation/:simulationId/start`
  - running simulation view
- `/report/:reportId`
  - generated report
- `/interaction/:reportId`
  - report/agent chat and survey UI

### Landing page flow

`Home.vue` does three things:

- lists active Polymarket markets
- allows direct Polymarket URL/slug lookup
- collects the simulation brief

When the user launches, the selected market and brief are temporarily stored in:

- `frontend/src/store/pendingUpload.js`

Then the app routes to:

- `/process/new`


## Backend Structure

Main backend files:

- `backend/app/__init__.py`
- `backend/app/config.py`
- `backend/app/api/market.py`
- `backend/app/api/graph.py`
- `backend/app/api/simulation.py`
- `backend/app/api/report.py`
- `backend/app/services/ontology_generator.py`
- `backend/app/services/polymarket_service.py`
- `backend/app/services/graph_builder.py`
- `backend/app/services/zep_entity_reader.py`
- `backend/app/services/oasis_profile_generator.py`
- `backend/app/services/simulation_config_generator.py`
- `backend/app/services/simulation_manager.py`
- `backend/app/services/simulation_runner.py`
- `backend/app/services/report_agent.py`
- `backend/app/services/zep_tools.py`
- `backend/app/models/project.py`
- `backend/app/models/task.py`

### App boot

`backend/app/__init__.py`:

- creates the Flask app
- enables CORS for `/api/*`
- registers blueprints
- mounts the built frontend from `frontend/dist`
- exposes `/health`

This is set up so one Railway service can serve both the API and the frontend.


## Core API Flow

### 1. Market selection and project creation

Route:

- `POST /api/markets/project`

Implemented in:

- `backend/app/api/market.py`

What happens:

- frontend sends `market_slug` or `market_id` plus `simulation_requirement`
- backend resolves the market through `PolymarketService`
- backend builds a plain-text market seed from live metadata
- backend creates a filesystem-backed project
- backend asks the LLM to generate ontology types

Important service:

- `backend/app/services/polymarket_service.py`

This service:

- fetches active markets from Polymarket Gamma
- resolves direct market URLs / slugs / ids
- has fallback slug normalization and fuzzy lookup for markets whose slugs changed

Ontology generation lives in:

- `backend/app/services/ontology_generator.py`

The ontology is specifically designed for social simulation, not generic KG extraction.


### 2. Graph build

Route:

- `POST /api/graph/build`

Implemented in:

- `backend/app/api/graph.py`

What happens:

- backend loads the stored project text and ontology
- text is chunked
- a Zep graph is created
- ontology is registered in Zep
- text chunks are uploaded as episodes
- backend waits for Zep extraction / processing
- graph stats are fetched and stored back on the project

Main service:

- `backend/app/services/graph_builder.py`

Notable implementation details:

- graph creation runs asynchronously in a background thread
- graph build progress is exposed through task polling
- transient Zep failures are retried during create / ontology setup / batch upload


### 3. Simulation creation and preparation

Routes:

- `POST /api/simulation/create`
- `POST /api/simulation/prepare`
- `POST /api/simulation/prepare/status`
- `GET /api/simulation/<simulation_id>/profiles/realtime`
- `GET /api/simulation/<simulation_id>/config/realtime`

Implemented in:

- `backend/app/api/simulation.py`

Preparation is handled by:

- `backend/app/services/simulation_manager.py`

What happens during prepare:

1. load the graph
2. read and filter relevant entities from Zep
3. generate agent profiles
4. generate simulation config
5. write all artifacts to the simulation directory

Entity reading:

- `backend/app/services/zep_entity_reader.py`

Agent profile generation:

- `backend/app/services/oasis_profile_generator.py`

Simulation config generation:

- `backend/app/services/simulation_config_generator.py`

Generated artifacts typically include:

- `state.json`
- `simulation_config.json`
- `reddit_profiles.json`
- `twitter_profiles.csv`


### 4. Simulation run

Primary runtime service:

- `backend/app/services/simulation_runner.py`

What it does:

- launches the simulation scripts as background subprocesses
- tracks run state
- parses actions and round progress
- exposes run-status APIs
- optionally updates the graph memory back into Zep during the run

Graph-memory feedback path:

- `backend/app/services/zep_graph_memory_updater.py`

The UI for this phase is mainly:

- `frontend/src/components/Step3Simulation.vue`
- `frontend/src/views/SimulationRunView.vue`

The simulation is presented as two parallel platform archetypes:

- a Twitter-like information plaza
- a Reddit-like topic community


### 5. Report generation

Routes:

- `POST /api/report/generate`
- `POST /api/report/generate/status`
- report fetch / log fetch / chat endpoints under `/api/report`

Implemented in:

- `backend/app/api/report.py`

Main service:

- `backend/app/services/report_agent.py`

Supporting retrieval tools:

- `backend/app/services/zep_tools.py`

What the report agent does:

- builds an outline
- searches the graph using Zep-backed tools
- writes the report section by section
- stores progress logs
- exposes both final markdown and detailed agent logs

The report flow is not just a template render. It is an agent loop with planning, retrieval, and staged writing.


## State and Persistence Model

### Projects

Projects are persisted by:

- `backend/app/models/project.py`

Stored under:

- `UPLOAD_FOLDER/projects/<project_id>/`

Project state includes:

- metadata
- extracted seed text
- ontology
- graph id
- simulation requirement

### Simulations

Simulations are persisted by:

- `backend/app/services/simulation_manager.py`

Stored under:

- `OASIS_SIMULATION_DATA_DIR/<simulation_id>/`

Simulation state is mostly JSON/file-based, not database-backed.

### Tasks

Long-running tasks are tracked by:

- `backend/app/models/task.py`

Important limitation:

- task state is in-memory only
- if the backend process restarts, task progress history is lost

This means project/simulation files are durable, but task polling is not durable across restarts.


## LLM Layer

Primary wrapper:

- `backend/app/utils/llm_client.py`

Used by:

- ontology generation
- simulation config generation
- profile generation
- report generation
- some Zep search helper logic

Important implementation detail:

- the codebase treats the LLM provider as OpenAI-compatible
- some providers only partially support structured outputs
- there is provider-specific handling around JSON schema mode vs prompt-constrained JSON parsing


## Why Zep matters here

Zep is not just a storage dependency. It is central to the app’s architecture.

PolyFish uses Zep to:

- build the graph from chunked market text
- read entities and their context back out
- enrich agent profile generation
- power report retrieval/search tools
- optionally absorb simulation activity back into graph memory

So the graph is not a side feature. It is the connective tissue between:

- market ingestion
- simulation prep
- report generation
- interactive analysis


## Current User-Facing Workflow Mapping

### Step 1: Graph Build

Frontend:

- `MainView.vue`
- `Step1GraphBuild.vue`

Backend:

- `/api/markets/project`
- `/api/graph/build`

Result:

- project created
- ontology generated
- graph built

### Step 2: Environment Setup

Frontend:

- `Step2EnvSetup.vue`

Backend:

- `/api/simulation/create`
- `/api/simulation/prepare`

Result:

- entities loaded from graph
- agent personas generated
- simulation config generated

### Step 3: Run Simulation

Frontend:

- `Step3Simulation.vue`
- `SimulationRunView.vue`

Backend:

- simulation start / stop / run-status APIs

Result:

- dual-platform simulation actions and rounds

### Step 4: Report

Frontend:

- `Step4Report.vue`
- `ReportView.vue`

Backend:

- report generation + report retrieval

Result:

- written thesis / report plus logs

### Step 5: Interaction

Frontend:

- `Step5Interaction.vue`
- `InteractionView.vue`

Backend:

- report chat / agent chat / survey endpoints

Result:

- user can interrogate the report and simulated agents


## Deployment Shape

The app is set up to run as a single deployable web service.

Production shape:

- Vite frontend builds into `frontend/dist`
- Flask serves API + static frontend
- same-origin frontend API calls use `/api`
- Railway can run the app through the root `Dockerfile`

Important env vars include:

- `LLM_API_KEY`
- `LLM_BASE_URL`
- `LLM_MODEL_NAME`
- `ZEP_API_KEY`
- `SECRET_KEY`
- `UPLOAD_FOLDER`
- `OASIS_SIMULATION_DATA_DIR`


## Practical Engineering Notes

### Strengths

- clear end-to-end product pipeline
- same-service deploy is simple
- graph and report layers are meaningfully integrated
- filesystem persistence makes local debugging easy

### Weak spots

- a lot of state is file-based and process-local
- task tracking is not durable
- there is legacy naming drift (`MiroFish` vs `PolyFish`)
- several backend modules still carry formatting / readability debt
- external dependency reliability matters a lot because Polymarket, Zep, and the LLM provider all sit on the critical path

### Reality of the codebase

This is not a generic CRUD app. It is an orchestration app.

The hard parts are:

- external API reliability
- async task sequencing
- filesystem state consistency
- graph/provider compatibility
- keeping frontend polling aligned with backend task/file states


## Short Mental Model

If you need a one-sentence engineering summary:

PolyFish is a Flask + Vue orchestration layer that ingests a live Polymarket market, converts it into a Zep-backed knowledge graph, turns that graph into agent personas and a simulation config, runs a dual-platform social simulation, and then generates a retrieval-backed written thesis plus interactive follow-up analysis.

