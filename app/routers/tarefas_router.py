from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from typing import List
from app.services.tarefas_service import (
    criar_tarefa_service,
    concluir_tarefa_service,
    atribuir_tarefa_para_turma_service,
    listar_tarefas_do_aluno_service,
    atribuir_tarefa_para_aluno_service,
)

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


class TarefaCreate(BaseModel):
    nome: str
    materia_id: int
    aluno_id: int


class TarefaTurmaCreate(BaseModel):
    nome: str
    materia_id: int


class TarefaParaAluno(BaseModel):
    nome: str
    materia_id: int


@router.post("")
def criar_tarefa(tarefa: TarefaCreate, db: Session = Depends(get_db)):
    return criar_tarefa_service(tarefa, db)


@router.put("/{id}/concluir")
def concluir_tarefa(id: int, db: Session = Depends(get_db)):
    return concluir_tarefa_service(id, db)


@router.post("/turma/{turma_id}")
def atribuir_tarefa_para_turma(
    turma_id: int, tarefa_data: TarefaTurmaCreate, db: Session = Depends(get_db)
):
    return atribuir_tarefa_para_turma_service(turma_id, tarefa_data, db)


@router.get("/aluno/{aluno_id}")
def listar_tarefas_do_aluno(aluno_id: int, db: Session = Depends(get_db)):
    return listar_tarefas_do_aluno_service(aluno_id, db)


@router.post("/aluno/{aluno_id}")
def atribuir_tarefa_para_aluno(
    aluno_id: int, dados: TarefaParaAluno, db: Session = Depends(get_db)
):
    return atribuir_tarefa_para_aluno_service(aluno_id, dados, db)
