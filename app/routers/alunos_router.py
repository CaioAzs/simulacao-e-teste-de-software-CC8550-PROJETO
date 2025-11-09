from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from pydantic import BaseModel
from app.services.alunos_service import (
    criar_aluno_service,
    listar_alunos_service,
    obter_aluno_service,
    atualizar_aluno_service,
    deletar_aluno_service,
    alunos_com_mais_tarefas_pendentes_service,
    criar_alunos_em_lote_service,
)

router = APIRouter(prefix="/alunos", tags=["Alunos"])

class AlunoCreate(BaseModel):
    nome: str
    idade: int
    turma_id: int
    bolsista: bool = False
@router.post("")
def criar_aluno(aluno: AlunoCreate, db: Session = Depends(get_db)):
    return criar_aluno_service(aluno, db)


@router.get("")
def listar_alunos(db: Session = Depends(get_db)):
    return listar_alunos_service(db)


@router.get("/mais-pendentes")
def alunos_com_mais_tarefas_pendentes(db: Session = Depends(get_db)):
    return alunos_com_mais_tarefas_pendentes_service(db)


@router.get("/{id}")
def obter_aluno(id: int, db: Session = Depends(get_db)):
    return obter_aluno_service(id, db)


@router.put("/{id}")
def atualizar_aluno(id: int, dados: AlunoCreate, db: Session = Depends(get_db)):
    return atualizar_aluno_service(id, dados, db)


@router.delete("/{id}")
def deletar_aluno(id: int, db: Session = Depends(get_db)):
    return deletar_aluno_service(id, db)


@router.post("/lote")
def criar_alunos_em_lote(alunos: List[AlunoCreate], db: Session = Depends(get_db)):
    return criar_alunos_em_lote_service(alunos, db)