# Clase base para declarar y validar los datos que
# llegan en las peticiones (JSON) o salen en las respuestas.
from pydantic import BaseModel


class ChatRequest(BaseModel):
    prompt: str
    stream: bool = False


class ChatResponse(BaseModel):
    response: str
