"""
Exceções relacionadas ao banco de dados.
"""

from .base import AppException


class DatabaseException(AppException):
    """
    Exceção base para erros relacionados ao banco de dados.
    """
    pass


class ConexaoBancoException(DatabaseException):
    """Erro ao conectar com o banco de dados."""
    pass


class IntegridadeDadosException(DatabaseException):
    """Violação de integridade de dados (chave estrangeira, unique, etc)."""
    pass
