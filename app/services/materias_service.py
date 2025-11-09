from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Materia, aluno_materia
from app.repositories import MateriaRepository, TurmaRepository
from app.exceptions import MateriaNotFoundException, TurmaNotFoundException, AlunoNotFoundException


def criar_materia_service(materia, db: Session):
    materia_repo = MateriaRepository(db)
    nova = Materia(nome=materia.nome)
    return materia_repo.create(nova)


def listar_materias_service(db: Session):
    materia_repo = MateriaRepository(db)
    return materia_repo.get_all()


def listar_alunos_por_materia_service(id: int, db: Session):
    materia_repo = MateriaRepository(db)
    materia = materia_repo.get_by_id(id)
    if not materia:
        raise MateriaNotFoundException(f"Matéria com ID {id} não encontrada")
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
    turma_repo = TurmaRepository(db)
    materia_repo = MateriaRepository(db)

    turma = turma_repo.get_by_id(turma_id)
    if not turma:
        raise TurmaNotFoundException(f"Turma com ID {turma_id} não encontrada")

    alunos = turma.alunos
    if not alunos:
        raise AlunoNotFoundException(f"Nenhum aluno encontrado para a turma {turma_id}")

    materias = [materia_repo.get_by_id(mid) for mid in dados.materias_ids]
    materias = [m for m in materias if m is not None]

    if not materias:
        raise MateriaNotFoundException("Nenhuma matéria válida encontrada")

    for aluno in alunos:
        for materia in materias:
            if materia not in aluno.materias:
                aluno.materias.append(materia)

    db.commit()
    return {
        "mensagem": f"{len(materias)} matérias atribuídas a {len(alunos)} alunos da turma {turma_id}"
    }
