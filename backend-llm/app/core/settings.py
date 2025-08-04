# os to read environment variables
import os

class Settings:
    # Consume environment variables, otherwise use those defined in the arguments.
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "gemma3:4b")

# Initialized to import
settings = Settings()
