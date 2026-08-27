# Entrenamiento real de MI-IA

El Cerebro recopila conversaciones y ejemplos localmente. Esta capa **no cambia pesos automáticamente**.

## Flujo

1. Recopilar datos locales.
2. Revisar y limpiar el dataset.
3. Separar entrenamiento y validación.
4. Entrenar explícitamente un checkpoint.
5. Evaluar el checkpoint nuevo contra una evaluación fija.
6. Solo usar el nuevo modelo si supera el criterio elegido.

`trainer.py` permite inspeccionar y dividir el dataset. `evaluator.py` aporta una métrica determinista básica para pruebas. El entrenamiento de pesos se mantiene como una operación explícita para evitar que una conversación cambie silenciosamente el modelo.

## Privacidad

Los datos se guardan localmente. Antes de entrenar, revisa el dataset y elimina cualquier información que no quieras conservar. El sistema incluye controles para borrar los datos de aprendizaje.
