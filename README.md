# MI-IA

**MI-IA es un asistente de IA local y privado con su propio motor de inferencia experimental.**

## Componentes

- **MI-IA App:** interfaz, memoria y herramientas.
- **MI-IA Engine:** runtime local que carga directamente un modelo desde disco.
- **Cerebro:** memoria local + dataset de entrenamiento.
- **PWA:** interfaz instalable.

## Motor propio

MI-IA ya no depende de Ollama. El backend se conecta por defecto a:

`http://127.0.0.1:8080/v1`

El motor está en `engine/` y utiliza PyTorch + Transformers en esta primera etapa. Esto nos da una base real sobre la que desarrollar nuestro propio runtime.

Consulta [ENGINE.md](ENGINE.md) y [engine/README.md](engine/README.md).

## Ejecutar

### Motor

```bash
pip install -r engine/requirements.txt
```

Configura `MIIA_MODEL_PATH` en `.env` apuntando a un modelo local compatible y ejecuta:

```bash
python -m engine.server
```

### Aplicación

En otra terminal:

```bash
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload
```

Abre `frontend/index.html`.

## Privacidad

Por defecto todo funciona sobre `127.0.0.1`. El motor no descarga modelos automáticamente ni necesita una API de nube.

## Roadmap del motor

- [x] API local propia
- [x] Carga directa de modelos
- [x] Inferencia CPU/GPU básica
- [ ] Streaming de tokens
- [ ] KV cache optimizada
- [ ] Cuantización
- [ ] Scheduler de inferencia
- [ ] Backend nativo C/C++
- [ ] Fine-tuning local integrado
- [ ] Gestor de modelos

## Estado

**v0.3 — MI-IA Engine foundation**
