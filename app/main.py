from fastapi import FastAPI
from app.database import engine, Base
from app.routers import alunos_router, turmas_router, materias_router, tarefas_router

app = FastAPI(title="Gestão Escolar API")

# Cria tabelas
Base.metadata.create_all(bind=engine)

# Registra os routers
app.include_router(alunos_router.router)
app.include_router(turmas_router.router)
app.include_router(materias_router.router)
app.include_router(tarefas_router.router)
