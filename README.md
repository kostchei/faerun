# Faerun Combat - Side Scroller Web App

A browser-based side-scroller combat game with aggressive parallax layering.

## Quick Start (Native Windows)

### Prerequisites
- Node.js 18+ ([Download](https://nodejs.org/))
- Python 3.11+ ([Download](https://www.python.org/downloads/))

### Frontend (Terminal 1)

```powershell
cd D:\Code\Faerun\faerun-combat\client
npm install
npm run dev
```

Open http://localhost:5173 in your browser.

### Backend (Terminal 2)

```powershell
cd D:\Code\Faerun\faerun-combat\server
python -m venv venv
.\venv\Scripts\Activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API available at http://localhost:8000

## Demo Features

- **Parallax Scene**: Move your mouse left/right to see aggressive parallax scrolling
- **5 Depth Layers**: Skybox, background mountains, midground trees, stage, foreground grass
- **API Endpoints**: `/api/combat/start`, `/api/saves/`

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | PixiJS 8, TypeScript, Vite |
| Backend | FastAPI, Python, WebSockets |
