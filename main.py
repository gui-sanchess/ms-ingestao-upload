import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # <-- Importação do CORS adicionada aqui
from adapters.inbound.controllers import router
from infrastructure.database import engine, Base

# Essa linha é mágica: se a tabela 'artefatos_brutos' não existir no Azure, ele cria agora!
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Microsserviço de Upload - DocuIA",
    description="Recebe arquivos físicos, extrai o texto e salva no Azure PostgreSQL."
)

# --- CONFIGURAÇÃO DO CORS ---
# Isso é o que permite o seu Front-end (Porta 5000) acessar este Back-end (Porta 5001) sem ser bloqueado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registra as rotas do controller
app.include_router(router)

if __name__ == "__main__":
    # A Azure injeta o PORT. O 8000 fica como fallback seguro para rodar no seu PC.
    porta = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=porta)