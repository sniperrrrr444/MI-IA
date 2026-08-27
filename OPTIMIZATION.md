# MI-IA · Optimización

Objetivo: maximizar eficiencia **sin sacrificar la calidad de respuesta**.

Principios:

- Mantener el modelo original intacto; optimizar el runtime alrededor de él.
- Detectar CPU/GPU automáticamente y elegir dtype apropiado.
- Usar KV cache para no recalcular contexto innecesariamente.
- Usar cuantización solo cuando las pruebas demuestren que la pérdida de calidad es aceptable.
- Mantener perfiles de rendimiento reproducibles (latencia, tokens/s, RAM/VRAM).
- Comparar cada optimización contra un baseline antes de activarla.
- Evitar optimizaciones que mejoren tokens/s a costa de una degradación relevante de calidad.

## Roadmap

1. Benchmark baseline.
2. KV cache optimizada.
3. Quantización INT8/INT4 con evaluación.
4. Batching/scheduler.
5. Backend nativo CPU/GPU.
6. Kernel optimizados.
7. Selección automática de configuración según hardware.
