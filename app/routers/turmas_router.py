from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from app.services.turmas_service import (
    criar_turma_service,
    listar_turmas_service,
    listar_alunos_da_turma_service,
    turmas_com_mais_bolsistas_service,
)

router = APIRouter(prefix="/turmas", tags=["Turmas"])


class TurmaCreate(BaseModel):
    nome: str


@router.post("")
def criar_turma(turma: TurmaCreate, db: Session = Depends(get_db)):
    return criar_turma_service(turma, db)


@router.get("")
def listar_turmas(db: Session = Depends(get_db)):
    return listar_turmas_service(db)


@router.get("/{id}/alunos")
def listar_alunos_da_turma(id: int, db: Session = Depends(get_db)):
    return listar_alunos_da_turma_service(id, db)


@router.get("/mais-bolsistas")
def turmas_com_mais_bolsistas(db: Session = Depends(get_db)):
    return turmas_com_mais_bolsistas_service(db)
