from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import agentes_langchain_router

app = FastAPI(
    title="HiChatChain API",
    description="Gerenciamento de agentes com LangChain",
    version="1.0.0"
)

# CORS Middleware (para frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rotas com LangChain
app.include_router(agentes_langchain_router.router, prefix="/executar", tags=["Execução Langchain"])

@app.get("/")
def home():
    return {"msg": "API da HiChatChain rodando 🎯"}
