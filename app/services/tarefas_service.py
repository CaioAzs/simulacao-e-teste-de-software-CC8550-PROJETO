from sqlalchemy.orm import Session
from app.models import Tarefa
from app.repositories import TarefaRepository, MateriaRepository, AlunoRepository, TurmaRepository
from app.exceptions import (
    TarefaNotFoundException,
    MateriaNotFoundException,
    AlunoNotFoundException,
    TurmaNotFoundException
)


def criar_tarefa_service(tarefa, db: Session):
    tarefa_repo = TarefaRepository(db)
    nova = Tarefa(**tarefa.dict())
    return tarefa_repo.create(nova)


def concluir_tarefa_service(id: int, db: Session):
    tarefa_repo = TarefaRepository(db)
    tarefa = tarefa_repo.get_by_id(id)
    if not tarefa:
        raise TarefaNotFoundException(f"Tarefa com ID {id} não encontrada")

    tarefa_repo.update(id, concluido=True)
    return {"mensagem": "Tarefa concluída com sucesso"}


def atribuir_tarefa_para_turma_service(turma_id: int, tarefa_data, db: Session):
    materia_repo = MateriaRepository(db)
    turma_repo = TurmaRepository(db)
    tarefa_repo = TarefaRepository(db)

    materia = materia_repo.get_by_id(tarefa_data.materia_id)
    if not materia:
        raise MateriaNotFoundException(f"Matéria com ID {tarefa_data.materia_id} não encontrada")

    turma = turma_repo.get_by_id(turma_id)
    if not turma:
        raise TurmaNotFoundException(f"Turma com ID {turma_id} não encontrada")

    alunos = turma.alunos
    if not alunos:
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

    return {
        "mensagem": f"Tarefa '{tarefa_data.nome}' atribuída a {len(tarefas)} alunos da turma {turma_id}",
        "tarefas": tarefas,
    }


def listar_tarefas_do_aluno_service(aluno_id: int, db: Session):
    aluno_repo = AlunoRepository(db)
    aluno = aluno_repo.get_by_id(aluno_id)
    if not aluno:
        raise AlunoNotFoundException(f"Aluno com ID {aluno_id} não encontrado")

    tarefas = aluno.tarefas

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
    aluno_repo = AlunoRepository(db)
    materia_repo = MateriaRepository(db)
    tarefa_repo = TarefaRepository(db)

    aluno = aluno_repo.get_by_id(aluno_id)
    if not aluno:
        raise AlunoNotFoundException(f"Aluno com ID {aluno_id} não encontrado")

    materia = materia_repo.get_by_id(dados.materia_id)
    if not materia:
        raise MateriaNotFoundException(f"Matéria com ID {dados.materia_id} não encontrada")

    tarefa = Tarefa(
        nome=dados.nome,
        materia_id=dados.materia_id,
        aluno_id=aluno_id,
        concluido=False,
    )
    tarefa_criada = tarefa_repo.create(tarefa)

    return {
        "mensagem": f"Tarefa '{dados.nome}' atribuída ao aluno {aluno.nome}",
        "tarefa": {
            "id": tarefa_criada.id,
            "nome": tarefa_criada.nome,
            "materia": materia.nome,
            "concluido": tarefa_criada.concluido,
        },
    }
