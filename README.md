<div align="center">

<img src="./static/image/MiroFish_logo_compressed.jpeg" alt="MiroFish Logo" width="75%"/>

<a href="https://trendshift.io/repositories/16144" target="_blank"><img src="https://trendshift.io/api/badge/repositories/16144" alt="666ghj%2FMiroFish | Trendshift" style="width: 250px; height: 55px;" width="250" height="55"/></a>

A simple and universal swarm intelligence engine, predicting anything
</br>
<em>A Simple and Universal Swarm Intelligence Engine, Predicting Anything</em>

<a href="https://www.shanda.com/" target="_blank"><img src="./static/image/shanda_logo.png" alt="666ghj%2MiroFish | Shanda" height="40"/></a>

[![GitHub Stars](https://img.shields.io/github/stars/666ghj/MiroFish?style=flat-square&color=DAA520)](https://github.com/666ghj/MiroFish/stargazers)
[![GitHub Watchers](https://img.shields.io/github/watchers/666ghj/MiroFish?style=flat-square)](https://github.com/666ghj/MiroFish/watchers)
[![GitHub Forks](https://img.shields.io/github/forks/666ghj/MiroFish?style=flat-square)](https://github.com/666ghj/MiroFish/network)
[![Docker](https://img.shields.io/badge/Docker-Build-2496ED?style=flat-square&logo=docker&logoColor=white)](https://hub.docker.com/)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/666ghj/MiroFish)

[![Discord](https://img.shields.io/badge/Discord-Join-5865F2?style=flat-square&logo=discord&logoColor=white)](http://discord.gg/ePf5aPaHnA)
[![X](https://img.shields.io/badge/X-Follow-000000?style=flat-square&logo=x&logoColor=white)](https://x.com/mirofish_ai)
[![Instagram](https://img.shields.io/badge/Instagram-Follow-E4405F?style=flat-square&logo=instagram&logoColor=white)](https://www.instagram.com/mirofish_ai/)

[English Documentation](./README-EN.md) | [Project README](./README.md)

</div>

## ⚡ Overview

**MiroFish** is a next-generation AI prediction engine powered by multi-agent technology. By extracting seed information from the real world, such as breaking news, policy drafts, or financial signals, it automatically constructs a high-fidelity parallel digital world. Inside that environment, thousands of agents with independent personalities, long-term memory, and behavioral logic interact freely and evolve socially. You can inject variables dynamically from a God's-eye view and simulate future trajectories with precision, turning the future into a digital rehearsal ground for better decisions.

> You only need to upload seed materials, such as a data analysis report or an interesting story, and describe your prediction goal in natural language.</br>
> MiroFish returns a detailed prediction report and a high-fidelity digital world you can explore interactively.

### Our Vision

MiroFish aims to build a swarm-intelligence mirror of reality. By capturing collective emergence driven by individual interactions, it pushes beyond the limits of traditional forecasting:

- **At the macro level**: a rehearsal lab for decision-makers, where policies and public-relations strategies can be tested without real-world risk.
- **At the micro level**: a creative sandbox for individual users, whether they want to infer a novel's ending or explore an unusual idea in a playful way.

From serious prediction to entertaining simulation, we want every "what if" to become something observable.

## 🌐 Live Demo

Visit the online demo environment to experience a prediction simulation built around a trending public-opinion event: [mirofish-live-demo](https://666ghj.github.io/mirofish-demo/)

## 📸 Screenshots

<div align="center">
<table>
<tr>
<td><img src="./static/image/Screenshot/screenshot-1.png" alt="Screenshot 1" width="100%"/></td>
<td><img src="./static/image/Screenshot/screenshot-2.png" alt="Screenshot 2" width="100%"/></td>
</tr>
<tr>
<td><img src="./static/image/Screenshot/screenshot-3.png" alt="Screenshot 3" width="100%"/></td>
<td><img src="./static/image/Screenshot/screenshot-4.png" alt="Screenshot 4" width="100%"/></td>
</tr>
<tr>
<td><img src="./static/image/Screenshot/screenshot-5.png" alt="Screenshot 5" width="100%"/></td>
<td><img src="./static/image/Screenshot/screenshot-6.png" alt="Screenshot 6" width="100%"/></td>
</tr>
</table>
</div>

## 🎬 Demo Videos

### 1. Wuhan University Public Opinion Forecast + MiroFish Walkthrough

<div align="center">
<a href="https://www.bilibili.com/video/BV1VYBsBHEMY/" target="_blank"><img src="./static/image/wuhan-university-demo-cover.png" alt="MiroFish Demo Video" width="75%"/></a>

Click the image to watch the full demo showing prediction based on the BettaFish-generated "Wuhan University Public Opinion Report."
</div>

### 2. Lost Ending Forecast for *Dream of the Red Chamber*

<div align="center">
<a href="https://www.bilibili.com/video/BV1cPk3BBExq" target="_blank"><img src="./static/image/dream-of-the-red-chamber-demo-cover.jpg" alt="MiroFish Demo Video" width="75%"/></a>

Click the image to watch MiroFish infer the lost ending based on the first 80 chapters of *Dream of the Red Chamber*.
</div>

> More examples, including finance and current-events forecasting, are on the way.

## 🔄 Workflow

1. **Graph Construction**: extract real-world seeds, inject individual and collective memory, and build GraphRAG.
2. **Environment Setup**: extract entity relationships, generate personas, and configure simulation agents.
3. **Simulation**: run dual-platform simulations in parallel, parse prediction requirements automatically, and update temporal memory dynamically.
4. **Report Generation**: let ReportAgent use its toolset to interact deeply with the simulated environment.
5. **Deep Interaction**: talk with any individual in the simulated world and continue the conversation with ReportAgent.

## 🚀 Quick Start

### Option 1: Source Deployment (Recommended)

#### Prerequisites

| Tool | Version Requirement | Description | Install Check |
|------|---------------------|-------------|---------------|
| **Node.js** | 18+ | Frontend runtime including npm | `node -v` |
| **Python** | ≥3.11, ≤3.12 | Backend runtime | `python --version` |
| **uv** | Latest | Python package manager | `uv --version` |

#### 1. Configure Environment Variables

```bash
# Copy the example configuration file
cp .env.example .env

# Edit the .env file and fill in the required API keys
```

**Required environment variables:**

```env
# LLM API configuration (supports any OpenAI SDK-compatible LLM API)
# Recommended: Alibaba Bailian qwen-plus model: https://bailian.console.aliyun.com/
# Consumption can be high, so start with fewer than 40 rounds
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL_NAME=qwen-plus

# Zep Cloud configuration
# The free monthly quota is enough for light usage: https://app.getzep.com/
ZEP_API_KEY=your_zep_api_key
```

#### 2. Install Dependencies

```bash
# Install all dependencies in one command (root + frontend + backend)
npm run setup:all
```

Or install them step by step:

```bash
# Install Node dependencies (root + frontend)
npm run setup

# Install Python dependencies (backend, creates the virtual environment automatically)
npm run setup:backend
```

#### 3. Start Services

```bash
# Start frontend and backend together from the project root
npm run dev
```

**Service URLs:**
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:5001`

**Run individually:**

```bash
npm run backend   # Start only the backend
npm run frontend  # Start only the frontend
```

### Option 2: Docker Deployment

```bash
# 1. Configure environment variables (same as source deployment)
cp .env.example .env

# 2. Pull the image and start
docker compose up -d
```

By default, Docker reads `.env` from the project root and maps ports `3000 (frontend) / 5001 (backend)`.

> `docker-compose.yml` includes a commented mirror image source you can switch to if pulls are slow.

### Option 3: Railway Deployment

This repository is now set up for a single Railway web service using the root `Dockerfile`.

How it works:

- Railway builds the Vue frontend during the Docker build.
- Flask serves the built frontend from `frontend/dist`.
- API requests use the same origin via `/api`, so no separate frontend service is required.
- Gunicorn runs the production web process on Railway's injected `PORT`.

Required environment variables:

```env
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o-mini
ZEP_API_KEY=your_zep_api_key
SECRET_KEY=replace_this_in_production
```

Optional but recommended on Railway:

```env
UPLOAD_FOLDER=/data/uploads
OASIS_SIMULATION_DATA_DIR=/data/uploads/simulations
GUNICORN_WORKERS=2
GUNICORN_THREADS=4
GUNICORN_TIMEOUT=300
```

Notes:

- Attach a Railway volume and mount it at `/data` if you want uploaded files and generated simulation artifacts to persist across deploys.
- The health check endpoint is `/health`.
- Railway will detect the root `Dockerfile` automatically and use it for build/deploy.

## 📬 Community

<div align="center">
<img src="./static/image/qq-group.png" alt="QQ Group" width="60%"/>
</div>

&nbsp;

The MiroFish team is recruiting for full-time and internship roles. If you are interested in multi-agent applications, send your resume to **mirofish@shanda.com**.

## 📄 Acknowledgments

**MiroFish has received strategic support and incubation from Shanda Group.**

MiroFish's simulation engine is powered by **[OASIS](https://github.com/camel-ai/oasis)**. We sincerely thank the CAMEL-AI team for their open-source contributions.

## 📈 Project Statistics

<a href="https://www.star-history.com/#666ghj/MiroFish&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=666ghj/MiroFish&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=666ghj/MiroFish&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=666ghj/MiroFish&type=date&legend=top-left" />
 </picture>
</a>
