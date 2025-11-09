from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Turma, Aluno
from app.repositories import TurmaRepository
from app.exceptions import TurmaNotFoundException
from app.utils import setup_logger

logger = setup_logger(__name__, log_level="INFO", log_file="logs/turmas_service.log")


def criar_turma_service(turma, db: Session):
    logger.info(f"Criando nova turma: {turma.nome}")
    turma_repo = TurmaRepository(db)
    nova = Turma(nome=turma.nome)
    resultado = turma_repo.create(nova)
    logger.info(f"Turma criada com sucesso: ID {resultado.id}, Nome: {resultado.nome}")
    return resultado


def listar_turmas_service(db: Session):
    logger.debug("Listando todas as turmas")
    turma_repo = TurmaRepository(db)
    turmas = turma_repo.get_all()
    logger.info(f"Listadas {len(turmas)} turmas")
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
    logger.debug(f"Listando alunos da turma ID {id}")
    turma_repo = TurmaRepository(db)
    turma = turma_repo.get_by_id(id)
    if not turma:
        logger.warning(f"Turma com ID {id} não encontrada ao listar alunos")
        raise TurmaNotFoundException(f"Turma com ID {id} não encontrada")
    logger.info(f"Listados {len(turma.alunos)} alunos da turma {turma.nome}")
    return turma.alunos


def turmas_com_mais_bolsistas_service(db: Session):
    logger.debug("Consultando turmas com mais bolsistas")
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
    logger.info(f"Consultadas {len(resultados)} turmas com bolsistas")

    return [
        {"id": id, "nome": nome, "total_bolsistas": total}
        for id, nome, total in resultados
    ]
