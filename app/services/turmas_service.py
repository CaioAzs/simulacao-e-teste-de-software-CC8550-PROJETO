from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Turma, Aluno

def criar_turma_service(turma, db: Session):
    nova = Turma(nome=turma.nome)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


def listar_turmas_service(db: Session):
    turmas = db.query(Turma).all()
    return [
        {
            "id": turma.id,
            "nome": turma.nome,
            "alunos": [
                {
                    "id": aluno.id,
                    "nome": aluno.nome,
                    "idade": aluno.idade,
                    "bolsista": aluno.bolsista,
                }
                for aluno in turma.alunos
            ],
        }
        for turma in turmas
    ]


def listar_alunos_da_turma_service(id: int, db: Session):
    turma = db.query(Turma).filter(Turma.id == id).first()
    if not turma:
        raise HTTPException(status_code=404, detail="Turma não encontrada")
    return turma.alunos


def turmas_com_mais_bolsistas_service(db: Session):
    resultados = (
        db.query(
            Turma.id,
            Turma.nome,
            func.count(Aluno.id).label("total_bolsistas"),
        )
        .join(Turma.alunos)
        .filter(Aluno.bolsista == True)
        .group_by(Turma.id)
        .order_by(func.count(Aluno.id).desc())
        .all()
    )

    return [
        {"id": id, "nome": nome, "total_bolsistas": total}
        for id, nome, total in resultados
    ]
