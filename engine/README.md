# MI-IA Engine

Motor local de inferencia experimental de MI-IA.

La primera versión usa una arquitectura de **backend propio + runtime de modelo intercambiable**. No depende de Ollama. El motor expone una API HTTP local compatible con el formato de chat que ya utiliza MI-IA.

## Objetivo

Evolucionar hacia un runtime propio capaz de:

1. descubrir modelos locales;
2. cargar un modelo;
3. tokenizar y generar texto;
4. gestionar KV cache y contexto;
5. usar CPU/GPU cuando sea posible;
6. hacer streaming;
7. integrar memoria y entrenamiento local.

## Estado

v0.1: runtime local experimental basado en Python y Transformers. Es una primera capa propia de MI-IA; no pretende ser todavía un reemplazo optimizado de llama.cpp.

## Arranque

Instala las dependencias:

```bash
pip install -r engine/requirements.txt
```

Configura:

```text
MIIA_MODEL_PATH=/ruta/al/modelo
MIIA_HOST=127.0.0.1
MIIA_PORT=8080
```

Arranca:

```bash
python -m engine.server
```

El servidor escucha en `127.0.0.1:8080`.

> Los modelos no se incluyen en Git. Descarga únicamente modelos que tengas derecho a usar y conserva sus licencias.
