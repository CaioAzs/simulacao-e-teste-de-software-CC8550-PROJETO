from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models import Tarefa, Materia, Aluno

def criar_tarefa_service(tarefa, db: Session):
    nova = Tarefa(**tarefa.dict())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


def concluir_tarefa_service(id: int, db: Session):
    tarefa = db.query(Tarefa).filter(Tarefa.id == id).first()
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    tarefa.concluido = True
    db.commit()
    return {"mensagem": "Tarefa concluída com sucesso"}


def atribuir_tarefa_para_turma_service(turma_id: int, tarefa_data, db: Session):
    materia = db.query(Materia).filter(Materia.id == tarefa_data.materia_id).first()
    if not materia:
        raise HTTPException(status_code=400, detail="Matéria não existe")

    alunos = db.query(Aluno).filter(Aluno.turma_id == turma_id).all()
    if not alunos:
        raise HTTPException(status_code=404, detail="Nenhum aluno encontrado para essa turma")

    tarefas = []
    for aluno in alunos:
        nova_tarefa = Tarefa(
            nome=tarefa_data.nome,
            materia_id=tarefa_data.materia_id,
            aluno_id=aluno.id,
            concluido=False,
        )
        db.add(nova_tarefa)
        tarefas.append(nova_tarefa)

    db.commit()
    for tarefa in tarefas:
        db.refresh(tarefa)

    return {
        "mensagem": f"Tarefa '{tarefa_data.nome}' atribuída a {len(tarefas)} alunos da turma {turma_id}",
        "tarefas": tarefas,
    }


def listar_tarefas_do_aluno_service(aluno_id: int, db: Session):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    tarefas = db.query(Tarefa).filter(Tarefa.aluno_id == aluno_id).all()

    return [
        {
            "id": tarefa.id,
            "nome": tarefa.nome,
            "concluido": tarefa.concluido,
            "materia": tarefa.materia.nome if tarefa.materia else None,
        }
        for tarefa in tarefas
    ]


def atribuir_tarefa_para_aluno_service(aluno_id: int, dados, db: Session):
    aluno = db.query(Aluno).filter(Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    materia = db.query(Materia).filter(Materia.id == dados.materia_id).first()
    if not materia:
        raise HTTPException(status_code=400, detail="Matéria não existe")

    tarefa = Tarefa(
        nome=dados.nome,
        materia_id=dados.materia_id,
        aluno_id=aluno_id,
        concluido=False,
    )
    db.add(tarefa)
    db.commit()
    db.refresh(tarefa)

    return {
        "mensagem": f"Tarefa '{dados.nome}' atribuída ao aluno {aluno.nome}",
        "tarefa": {
            "id": tarefa.id,
            "nome": tarefa.nome,
            "materia": materia.nome,
            "concluido": tarefa.concluido,
        },
    }
