from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from pydantic import BaseModel
from typing import List
from app.services.materias_service import (
    criar_materia_service,
    listar_materias_service,
    listar_alunos_por_materia_service,
    listar_materias_mais_populares_service,
    atribuir_materias_para_turma_service,
)

router = APIRouter(prefix="/materias", tags=["Matérias"])


class MateriaCreate(BaseModel):
    nome: str


class MateriasParaTurma(BaseModel):
    materias_ids: List[int]


@router.post("")
def criar_materia(materia: MateriaCreate, db: Session = Depends(get_db)):
    return criar_materia_service(materia, db)


@router.get("")
def listar_materias(db: Session = Depends(get_db)):
    return listar_materias_service(db)


@router.get("/{id}/alunos")
def listar_alunos_por_materia(id: int, db: Session = Depends(get_db)):
    return listar_alunos_por_materia_service(id, db)


@router.get("/mais-alunos")
def listar_materias_mais_populares(db: Session = Depends(get_db)):
    return listar_materias_mais_populares_service(db)


@router.post("/turma/{turma_id}")
def atribuir_materias_para_turma(
    turma_id: int, dados: MateriasParaTurma, db: Session = Depends(get_db)
):
    return atribuir_materias_para_turma_service(turma_id, dados, db)
