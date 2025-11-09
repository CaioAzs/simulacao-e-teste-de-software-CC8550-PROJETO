from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Materia, aluno_materia, Aluno

def criar_materia_service(materia, db: Session):
    nova = Materia(nome=materia.nome)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


def listar_materias_service(db: Session):
    return db.query(Materia).all()


def listar_alunos_por_materia_service(id: int, db: Session):
    materia = db.query(Materia).filter(Materia.id == id).first()
    if not materia:
        raise HTTPException(status_code=404, detail="Matéria não encontrada")
    return materia.alunos


def listar_materias_mais_populares_service(db: Session):
    resultados = (
        db.query(
            Materia.id,
            Materia.nome,
            func.count(aluno_materia.c.aluno_id).label("total_alunos"),
        )
        .join(aluno_materia, Materia.id == aluno_materia.c.materia_id)
        .group_by(Materia.id)
        .order_by(func.count(aluno_materia.c.aluno_id).desc())
        .all()
    )

    return [
        {"id": id, "nome": nome, "total_alunos": total}
        for id, nome, total in resultados
    ]


def atribuir_materias_para_turma_service(turma_id: int, dados, db: Session):
    alunos = db.query(Aluno).filter(Aluno.turma_id == turma_id).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para essa turma")

    materias = db.query(Materia).filter(Materia.id.in_(dados.materias_ids)).all()
    if not materias:
        raise HTTPException(status_code=404, detail="Nenhuma matéria válida encontrada")

    for aluno in alunos:
        for materia in materias:
            if materia not in aluno.materias:
                aluno.materias.append(materia)

    db.commit()
    return {
        "mensagem": f"{len(materias)} matérias atribuídas a {len(alunos)} alunos da turma {turma_id}"
    }
