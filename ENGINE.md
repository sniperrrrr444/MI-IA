# MI-IA Engine

MI-IA ya no necesita Ollama.

El repositorio incluye un runtime propio experimental en `engine/`.

## Arquitectura

```
MI-IA App
   ↓
Local API
   ↓
MI-IA Engine
   ↓
Transformers + PyTorch
   ↓
Modelo local
```

El runtime carga el modelo directamente desde una carpeta local usando `local_files_only=True`. No descarga modelos automáticamente y no necesita una API de nube.

## Uso

1. Instala Python y las dependencias de `engine/requirements.txt`.
2. Coloca un modelo local compatible en tu dispositivo.
3. Copia `engine/.env.example` a `.env`.
4. Configura `MIIA_MODEL_PATH`.
5. Ejecuta:

```bash
python -m engine.server
```

La API estará en `http://127.0.0.1:8080`.

## Importante

Esta es la primera implementación del motor propio. El objetivo siguiente es sustituir progresivamente las partes genéricas por componentes propios: loader, tokenizer adapter, KV cache, scheduler, cuantización y backend de CPU/GPU.

No se debe confundir el dataset de entrenamiento de MI-IA con entrenamiento de pesos: guardar ejemplos no cambia por sí solo el modelo neuronal.
