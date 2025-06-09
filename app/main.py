import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from . import security, models, database
from fastapi.responses import JSONResponse, RedirectResponse
import traceback

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Importar rotas
try:
    from app.routes import perfis, orcamentos, acessorios, vidros, projetos, estoque, auth
    logger.info("Rotas importadas com sucesso")
except ImportError as e:
    logger.error(f"Erro ao importar rotas: {e}")
    logger.error(traceback.format_exc())

app = FastAPI(title="API de Orçamentos", description="API para gerenciamento de orçamentos de esquadrias")

# Middleware para log de requisições
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Requisição recebida: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logger.info(f"Resposta: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"Erro ao processar requisição: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=500,
            content={"detail": f"Erro interno do servidor: {str(e)}"}
        )

# Configuração CORS
# ATENÇÃO: Em produção, restrinja as origens!
origins = [
    "https://jrglassworks.netlify.app",
    "https://68463dca3f442000999f39c--jrglassworks.netlify.app",
    "https://jrglassworks.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Rota raiz que redireciona para a documentação
@app.get("/", include_in_schema=False)
async def read_root():
    return RedirectResponse(url="/docs")

# Incluindo roteadores com prefixo /api
app.include_router(perfis.router, prefix="/api", tags=["perfis"])
app.include_router(orcamentos.router, prefix="/api", tags=["orçamentos"])
app.include_router(acessorios.router, prefix="/api", tags=["acessórios"])
app.include_router(vidros.router, prefix="/api", tags=["vidros"])
app.include_router(projetos.router, prefix="/api", tags=["projetos"])
app.include_router(estoque.router, prefix="/api", tags=["estoque"])
app.include_router(auth.router, prefix="/api", tags=["autenticacao"])

from sqlalchemy import text

@app.get("/api/health")
async def health_check():
    try:
        # Testa conexão com o banco de dados
        from app.database import SessionLocal
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        logger.error(f"Erro na verificação de saúde: {str(e)}")
        return {"status": "error", "database": "disconnected", "error": str(e)}
