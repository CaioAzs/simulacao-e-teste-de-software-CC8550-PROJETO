from app.repositories.base_repository import BaseRepository
from app.repositories.aluno_repository import AlunoRepository
from app.repositories.turma_repository import TurmaRepository
from app.repositories.materia_repository import MateriaRepository
from app.repositories.tarefa_repository import TarefaRepository

__all__ = [
    "BaseRepository",
    "AlunoRepository",
    "TurmaRepository",
    "MateriaRepository",
    "TarefaRepository",
]
