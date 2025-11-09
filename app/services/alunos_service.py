from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Aluno, Turma, Tarefa

def criar_aluno_service(aluno, db: Session):
    turma = db.query(Turma).filter(Turma.id == aluno.turma_id).first()
    if not turma:
        raise HTTPException(status_code=400, detail="Turma não existe")

    novo = Aluno(**aluno.dict())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def listar_alunos_service(db: Session):
    return db.query(Aluno).all()


def obter_aluno_service(id: int, db: Session):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


def atualizar_aluno_service(id: int, dados, db: Session):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    for campo, valor in dados.dict().items():
        setattr(aluno, campo, valor)
    db.commit()
    return aluno


def deletar_aluno_service(id: int, db: Session):
    aluno = db.query(Aluno).filter(Aluno.id == id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    db.delete(aluno)
    db.commit()
    return {"mensagem": "Aluno removido com sucesso"}


def alunos_com_mais_tarefas_pendentes_service(db: Session):
    resultados = (
        db.query(
            Aluno.id,
            Aluno.nome,
            func.count(Tarefa.id).label("pendentes")
        )
        .outerjoin(Aluno.tarefas)
        .filter(Tarefa.concluido == False)
        .group_by(Aluno.id, Aluno.nome)
        .order_by(func.count(Tarefa.id).desc())
        .all()
    )
    return [
        {"id": id, "nome": nome, "pendentes": pendentes}
        for id, nome, pendentes in resultados
    ]


def criar_alunos_em_lote_service(alunos, db: Session):
    criados = []
    for aluno_data in alunos:
        turma = db.query(Turma).filter(Turma.id == aluno_data.turma_id).first()
        if not turma:
            raise HTTPException(status_code=400, detail=f"Turma {aluno_data.turma_id} não existe")

        novo = Aluno(**aluno_data.dict())
        db.add(novo)
        criados.append(novo)
    db.commit()
    for aluno in criados:
        db.refresh(aluno)
    return criados
