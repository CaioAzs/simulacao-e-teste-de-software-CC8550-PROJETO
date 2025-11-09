from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Aluno, Turma, Tarefa
from app.repositories import AlunoRepository, TurmaRepository
from app.exceptions import AlunoNotFoundException, TurmaNotFoundException


def criar_aluno_service(aluno, db: Session):
    turma_repo = TurmaRepository(db)
    turma = turma_repo.get_by_id(aluno.turma_id)
    if not turma:
        raise TurmaNotFoundException(f"Turma com ID {aluno.turma_id} não encontrada")

    aluno_repo = AlunoRepository(db)
    novo = Aluno(**aluno.dict())
    return aluno_repo.create(novo)


def listar_alunos_service(db: Session):
    aluno_repo = AlunoRepository(db)
    return aluno_repo.get_all()


def obter_aluno_service(id: int, db: Session):
    aluno_repo = AlunoRepository(db)
    aluno = aluno_repo.get_by_id(id)
    if not aluno:
        raise AlunoNotFoundException(f"Aluno com ID {id} não encontrado")
    return aluno


def atualizar_aluno_service(id: int, dados, db: Session):
    aluno_repo = AlunoRepository(db)
    aluno = aluno_repo.update(id, **dados.dict())
    if not aluno:
        raise AlunoNotFoundException(f"Aluno com ID {id} não encontrado")
    return aluno


def deletar_aluno_service(id: int, db: Session):
    aluno_repo = AlunoRepository(db)
    if not aluno_repo.delete(id):
        raise AlunoNotFoundException(f"Aluno com ID {id} não encontrado")
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
    turma_repo = TurmaRepository(db)
    aluno_repo = AlunoRepository(db)
    criados = []

    for aluno_data in alunos:
        turma = turma_repo.get_by_id(aluno_data.turma_id)
        if not turma:
            raise TurmaNotFoundException(f"Turma com ID {aluno_data.turma_id} não encontrada")

        novo = Aluno(**aluno_data.dict())
        criado = aluno_repo.create(novo)
        criados.append(criado)

    return criados
