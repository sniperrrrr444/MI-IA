# MI-IA — Local AI

MI-IA now uses a local inference engine by default.

## Default configuration

- Engine: Ollama
- Endpoint: `http://127.0.0.1:11434/v1`
- Model: `llama3.2:3b`
- No API key is required.

## Start

Install Ollama, then run:

```bash
ollama pull llama3.2:3b
ollama serve
```

In another terminal:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

The MI-IA backend and model both run locally.

## Change model

Set `AI_MODEL` in your local `.env`, for example:

```text
AI_MODEL=your-local-model
```

Do not put API keys or private credentials into GitHub.
