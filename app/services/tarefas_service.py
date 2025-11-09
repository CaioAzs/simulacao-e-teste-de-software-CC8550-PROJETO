from sqlalchemy.orm import Session
from app.models import Tarefa
from app.repositories import TarefaRepository, MateriaRepository, AlunoRepository, TurmaRepository
from app.exceptions import (
    TarefaNotFoundException,
    MateriaNotFoundException,
    AlunoNotFoundException,
    TurmaNotFoundException
)
from app.utils import setup_logger

logger = setup_logger(__name__, log_level="INFO", log_file="logs/tarefas_service.log")


def criar_tarefa_service(tarefa, db: Session):
    logger.info(f"Criando nova tarefa: {tarefa.nome}")
    tarefa_repo = TarefaRepository(db)
    nova = Tarefa(**tarefa.dict())
    resultado = tarefa_repo.create(nova)
    logger.info(f"Tarefa criada com sucesso: ID {resultado.id}")
    return resultado


def concluir_tarefa_service(id: int, db: Session):
    logger.info(f"Marcando tarefa ID {id} como concluída")
    tarefa_repo = TarefaRepository(db)
    tarefa = tarefa_repo.get_by_id(id)
    if not tarefa:
        logger.warning(f"Tarefa com ID {id} não encontrada ao tentar concluir")
        raise TarefaNotFoundException(f"Tarefa com ID {id} não encontrada")

    tarefa_repo.update(id, concluido=True)
    logger.info(f"Tarefa ID {id} concluída com sucesso")
    return {"mensagem": "Tarefa concluída com sucesso"}


def atribuir_tarefa_para_turma_service(turma_id: int, tarefa_data, db: Session):
    logger.info(f"Atribuindo tarefa '{tarefa_data.nome}' para turma ID {turma_id}")
    materia_repo = MateriaRepository(db)
    turma_repo = TurmaRepository(db)
    tarefa_repo = TarefaRepository(db)

    materia = materia_repo.get_by_id(tarefa_data.materia_id)
    if not materia:
        logger.error(f"Matéria {tarefa_data.materia_id} não encontrada ao atribuir tarefa para turma")
        raise MateriaNotFoundException(f"Matéria com ID {tarefa_data.materia_id} não encontrada")

    turma = turma_repo.get_by_id(turma_id)
    if not turma:
        logger.error(f"Turma {turma_id} não encontrada ao atribuir tarefa")
        raise TurmaNotFoundException(f"Turma com ID {turma_id} não encontrada")

    alunos = turma.alunos
    if not alunos:
        logger.warning(f"Nenhum aluno encontrado na turma {turma_id}")
        raise AlunoNotFoundException(f"Nenhum aluno encontrado para a turma {turma_id}")

    tarefas = []
    for aluno in alunos:
        nova_tarefa = Tarefa(
            nome=tarefa_data.nome,
            materia_id=tarefa_data.materia_id,
            aluno_id=aluno.id,
            concluido=False,
        )
        tarefa_criada = tarefa_repo.create(nova_tarefa)
        tarefas.append(tarefa_criada)

    logger.info(f"Tarefa '{tarefa_data.nome}' atribuída com sucesso a {len(tarefas)} alunos da turma {turma_id}")
    return {
        "mensagem": f"Tarefa '{tarefa_data.nome}' atribuída a {len(tarefas)} alunos da turma {turma_id}",
        "tarefas": tarefas,
    }


def listar_tarefas_do_aluno_service(aluno_id: int, db: Session):
    logger.debug(f"Listando tarefas do aluno ID {aluno_id}")
    aluno_repo = AlunoRepository(db)
    aluno = aluno_repo.get_by_id(aluno_id)
    if not aluno:
        logger.warning(f"Aluno com ID {aluno_id} não encontrado ao listar tarefas")
        raise AlunoNotFoundException(f"Aluno com ID {aluno_id} não encontrado")

    tarefas = aluno.tarefas
    logger.info(f"Listadas {len(tarefas)} tarefas do aluno {aluno.nome}")

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
    logger.info(f"Atribuindo tarefa '{dados.nome}' para aluno ID {aluno_id}")
    aluno_repo = AlunoRepository(db)
    materia_repo = MateriaRepository(db)
    tarefa_repo = TarefaRepository(db)

    aluno = aluno_repo.get_by_id(aluno_id)
    if not aluno:
        logger.error(f"Aluno {aluno_id} não encontrado ao atribuir tarefa")
        raise AlunoNotFoundException(f"Aluno com ID {aluno_id} não encontrado")

    materia = materia_repo.get_by_id(dados.materia_id)
    if not materia:
        logger.error(f"Matéria {dados.materia_id} não encontrada ao atribuir tarefa")
        raise MateriaNotFoundException(f"Matéria com ID {dados.materia_id} não encontrada")

    tarefa = Tarefa(
        nome=dados.nome,
        materia_id=dados.materia_id,
        aluno_id=aluno_id,
        concluido=False,
    )
    tarefa_criada = tarefa_repo.create(tarefa)
    logger.info(f"Tarefa '{dados.nome}' atribuída com sucesso ao aluno {aluno.nome}")

    return {
        "mensagem": f"Tarefa '{dados.nome}' atribuída ao aluno {aluno.nome}",
        "tarefa": {
            "id": tarefa_criada.id,
            "nome": tarefa_criada.nome,
            "materia": materia.nome,
            "concluido": tarefa_criada.concluido,
        },
    }
