from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Turma, Aluno
from app.repositories import TurmaRepository
from app.exceptions import TurmaNotFoundException


def criar_turma_service(turma, db: Session):
    turma_repo = TurmaRepository(db)
    nova = Turma(nome=turma.nome)
    return turma_repo.create(nova)


def listar_turmas_service(db: Session):
    turma_repo = TurmaRepository(db)
    turmas = turma_repo.get_all()
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
    turma_repo = TurmaRepository(db)
    turma = turma_repo.get_by_id(id)
    if not turma:
        raise TurmaNotFoundException(f"Turma com ID {id} não encontrada")
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
