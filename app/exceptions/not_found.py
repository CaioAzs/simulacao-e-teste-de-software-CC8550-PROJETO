"""
Exceções para recursos não encontrados.
"""

from .base import AppException


class NotFoundException(AppException):
    """
    Exceção base para recursos não encontrados no banco de dados.
    """
    pass


class AlunoNotFoundException(NotFoundException):
    """Aluno não encontrado."""
    pass


class MateriaNotFoundException(NotFoundException):
    """Matéria não encontrada."""
    pass


class TarefaNotFoundException(NotFoundException):
    """Tarefa não encontrada."""
    pass


class TurmaNotFoundException(NotFoundException):
    """Turma não encontrada."""
    pass
