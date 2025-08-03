#!/bin/bash
# Inicia Ollama en segundo plano
ollama serve &

# Espera a que Ollama esté listo
until curl -s http://localhost:11434 > /dev/null; do
  echo "⏳ Esperando a que Ollama esté listo..."
  sleep 1
done

# Opcional: realiza el pull si el modelo no está presente
ollama list | grep -q "gemma3:4b" || ollama pull gemma3:4b

# Ejecuta tu API
uvicorn app.main:app --host 0.0.0.0 --port 8000
