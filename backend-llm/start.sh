#!/bin/bash

echo "🚀 Iniciando Ollama en segundo plano..."
ollama serve &

# Esperar a que Ollama esté disponible
echo "⏳ Esperando a que el servidor de Ollama responda..."
until curl -s http://localhost:11434 > /dev/null; do
  sleep 1
done
echo "✅ Ollama está activo en http://localhost:11434"

# Verifica y descarga modelos si no están presentes
echo "📦 Verificando modelos requeridos..."

if ollama list | grep -q "gemma3:4b"; then
  echo "✅ Modelo 'gemma3:4b' ya está disponible."
else
  echo "⬇️ Descargando modelo 'gemma3:4b'..."
  ollama pull gemma3:4b && echo "✅ Descarga de 'gemma3:4b' completada." || {
    echo "❌ Error al descargar 'gemma3:4b'. Abortando."
    exit 1
  }
fi

# Iniciar la API
echo "🚀 Iniciando FastAPI en http://0.0.0.0:8000"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
