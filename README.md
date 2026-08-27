# MI-IA

A modular personal AI assistant project.

## Vision

MI-IA is designed to grow into a complete AI assistant with:
- Conversational chat
- Pluggable AI providers
- Conversation history
- Configurable personality and system instructions
- A simple web interface
- A clean architecture for adding tools and capabilities

## Project structure

```
MI-IA/
├── backend/
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   └── index.html
├── .env.example
├── .gitignore
└── README.md
```

## Quick start

1. Copy `.env.example` to `.env`.
2. Add your AI provider/API configuration.
3. Install the backend dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
4. Start the API:
   ```bash
   uvicorn backend.main:app --reload
   ```
5. Open `frontend/index.html` in a browser.

## Status

Early foundation — the architecture is intentionally simple so MI-IA can evolve without becoming a spaghetti monster.
