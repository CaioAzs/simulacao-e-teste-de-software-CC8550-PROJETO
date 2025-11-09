from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Aluno, Turma, Tarefa
from app.repositories import AlunoRepository, TurmaRepository
from app.exceptions import AlunoNotFoundException, TurmaNotFoundException
from app.utils import setup_logger

logger = setup_logger(__name__, log_level="INFO", log_file="logs/alunos_service.log")


def criar_aluno_service(aluno, db: Session):
    logger.info(f"Criando novo aluno: {aluno.nome}")
    turma_repo = TurmaRepository(db)
    turma = turma_repo.get_by_id(aluno.turma_id)
    if not turma:
        logger.error(f"Turma {aluno.turma_id} não encontrada ao criar aluno")
        raise TurmaNotFoundException(f"Turma com ID {aluno.turma_id} não encontrada")

    aluno_repo = AlunoRepository(db)
    novo = Aluno(**aluno.dict())
    resultado = aluno_repo.create(novo)
    logger.info(f"Aluno criado com sucesso: ID {resultado.id}, Nome: {resultado.nome}")
    return resultado


def listar_alunos_service(db: Session):
    logger.debug("Listando todos os alunos")
    aluno_repo = AlunoRepository(db)
    alunos = aluno_repo.get_all()
    logger.info(f"Listados {len(alunos)} alunos")
    return alunos


def obter_aluno_service(id: int, db: Session):
    logger.debug(f"Buscando aluno com ID {id}")
    aluno_repo = AlunoRepository(db)
    aluno = aluno_repo.get_by_id(id)
    if not aluno:
        logger.warning(f"Aluno com ID {id} não encontrado")
        raise AlunoNotFoundException(f"Aluno com ID {id} não encontrado")
    logger.info(f"Aluno encontrado: {aluno.nome}")
    return aluno


def atualizar_aluno_service(id: int, dados, db: Session):
    logger.info(f"Atualizando aluno ID {id}")
    aluno_repo = AlunoRepository(db)
    aluno = aluno_repo.update(id, **dados.dict())
    if not aluno:
        logger.error(f"Falha ao atualizar: Aluno ID {id} não encontrado")
        raise AlunoNotFoundException(f"Aluno com ID {id} não encontrado")
    logger.info(f"Aluno ID {id} atualizado com sucesso")
    return aluno


def deletar_aluno_service(id: int, db: Session):
    logger.warning(f"Deletando aluno ID {id}")
    aluno_repo = AlunoRepository(db)
    if not aluno_repo.delete(id):
        logger.error(f"Falha ao deletar: Aluno ID {id} não encontrado")
        raise AlunoNotFoundException(f"Aluno com ID {id} não encontrado")
    logger.info(f"Aluno ID {id} removido com sucesso")
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
    logger.info(f"Criando {len(alunos)} alunos em lote")
    turma_repo = TurmaRepository(db)
    aluno_repo = AlunoRepository(db)
    criados = []

    for i, aluno_data in enumerate(alunos, 1):
        logger.debug(f"Processando aluno {i}/{len(alunos)}: {aluno_data.nome}")
        turma = turma_repo.get_by_id(aluno_data.turma_id)
        if not turma:
            logger.error(f"Turma {aluno_data.turma_id} não encontrada durante criação em lote")
            raise TurmaNotFoundException(f"Turma com ID {aluno_data.turma_id} não encontrada")

        novo = Aluno(**aluno_data.dict())
        criado = aluno_repo.create(novo)
        criados.append(criado)

    logger.info(f"Criação em lote concluída: {len(criados)} alunos criados com sucesso")
    return criados
