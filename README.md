# MI-IA

**MI-IA es un asistente de IA local y privado.** El modelo se ejecuta en el propio dispositivo.

## Qué incluye

- Interfaz de chat responsive.
- Historial persistente en almacenamiento local del navegador.
- Backend FastAPI local.
- Motor de inferencia local compatible con OpenAI.
- Ollama como configuración predeterminada.
- PWA instalable como aplicación.
- Sin API key de nube.
- Preparado para añadir memoria, voz, visión, archivos y herramientas.

## Arquitectura

```
MI-IA/
├── backend/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── manifest.json
│   └── sw.js
├── .env.example
└── README.md
```

## Ejecutarlo

### 1. Instala un motor local

Con Ollama, instala el programa en el dispositivo y descarga un modelo:

```bash
ollama pull llama3.2:3b
ollama serve
```

### 2. Instala MI-IA

```bash
python -m venv .venv
```

Linux/macOS:

```bash
source .venv/bin/activate
```

Windows:

```powershell
.venv\\Scripts\\Activate.ps1
```

Instala dependencias:

```bash
pip install -r backend/requirements.txt
```

### 3. Arranca MI-IA

```bash
uvicorn backend.main:app --reload
```

Abre `frontend/index.html` en el navegador.

## Configuración

Copia `.env.example` a `.env` para cambiar el modelo o endpoint.

Por defecto:

```text
AI_BASE_URL=http://127.0.0.1:11434/v1
AI_MODEL=llama3.2:3b
```

Puedes cambiar `AI_MODEL` por cualquier modelo local compatible con tu motor.

## Privacidad

Por defecto, MI-IA conecta únicamente con `127.0.0.1`. Las conversaciones no se envían a una API de IA externa.

Si cambias manualmente `AI_BASE_URL` a un servidor remoto, ese servidor podrá recibir los mensajes.

## Estado

**v0.2 — Local-first foundation**

## Próximamente

- Streaming de respuestas.
- Memoria semántica local.
- Gestor de modelos.
- Adjuntar y analizar archivos.
- Entrada y salida por voz.
- Modelos de visión.
- Herramientas locales.
- Empaquetado nativo para Windows/Linux/Android.
