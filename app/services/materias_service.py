from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Materia, aluno_materia
from app.repositories import MateriaRepository, TurmaRepository
from app.exceptions import MateriaNotFoundException, TurmaNotFoundException, AlunoNotFoundException
from app.utils import setup_logger

logger = setup_logger(__name__, log_level="INFO", log_file="logs/materias_service.log")


def criar_materia_service(materia, db: Session):
    logger.info(f"Criando nova matéria: {materia.nome}")
    materia_repo = MateriaRepository(db)
    nova = Materia(nome=materia.nome)
    resultado = materia_repo.create(nova)
    logger.info(f"Matéria criada com sucesso: ID {resultado.id}, Nome: {resultado.nome}")
    return resultado


def listar_materias_service(db: Session):
    logger.debug("Listando todas as matérias")
    materia_repo = MateriaRepository(db)
    materias = materia_repo.get_all()
    logger.info(f"Listadas {len(materias)} matérias")
    return materias


def listar_alunos_por_materia_service(id: int, db: Session):
    logger.debug(f"Listando alunos da matéria ID {id}")
    materia_repo = MateriaRepository(db)
    materia = materia_repo.get_by_id(id)
    if not materia:
        logger.warning(f"Matéria com ID {id} não encontrada ao listar alunos")
        raise MateriaNotFoundException(f"Matéria com ID {id} não encontrada")
    logger.info(f"Listados {len(materia.alunos)} alunos da matéria {materia.nome}")
    return materia.alunos


def listar_materias_mais_populares_service(db: Session):
    logger.debug("Consultando matérias mais populares")
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
    logger.info(f"Consultadas {len(resultados)} matérias populares")

    return [
        {"id": id, "nome": nome, "total_alunos": total}
        for id, nome, total in resultados
    ]


def atribuir_materias_para_turma_service(turma_id: int, dados, db: Session):
    logger.info(f"Atribuindo matérias para turma ID {turma_id}")
    turma_repo = TurmaRepository(db)
    materia_repo = MateriaRepository(db)

    turma = turma_repo.get_by_id(turma_id)
    if not turma:
        logger.error(f"Turma {turma_id} não encontrada ao atribuir matérias")
        raise TurmaNotFoundException(f"Turma com ID {turma_id} não encontrada")

    alunos = turma.alunos
    if not alunos:
        logger.warning(f"Nenhum aluno encontrado na turma {turma_id}")
        raise AlunoNotFoundException(f"Nenhum aluno encontrado para a turma {turma_id}")

    materias = [materia_repo.get_by_id(mid) for mid in dados.materias_ids]
    materias = [m for m in materias if m is not None]

    if not materias:
        logger.error("Nenhuma matéria válida encontrada para atribuição")
        raise MateriaNotFoundException("Nenhuma matéria válida encontrada")

    for aluno in alunos:
        for materia in materias:
            if materia not in aluno.materias:
                aluno.materias.append(materia)

    db.commit()
    logger.info(f"{len(materias)} matérias atribuídas a {len(alunos)} alunos da turma {turma_id}")
    return {
        "mensagem": f"{len(materias)} matérias atribuídas a {len(alunos)} alunos da turma {turma_id}"
    }
