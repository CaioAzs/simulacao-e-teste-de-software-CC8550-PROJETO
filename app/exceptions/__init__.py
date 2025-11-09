"""
Módulo de exceções personalizadas da aplicação.

Este módulo centraliza todas as exceções customizadas do sistema,
organizadas por categoria para facilitar o tratamento de erros.
"""

from .base import AppException
from .validation import (
    ValidationException,
    IdadeInvalidaException,
    NomeInvalidoException,
    EmailInvalidoException,
)
from .business import BusinessRuleException
from .not_found import (
    NotFoundException,
    AlunoNotFoundException,
    MateriaNotFoundException,
    TarefaNotFoundException,
    TurmaNotFoundException,
)
from .database import (
    DatabaseException,
    ConexaoBancoException,
    IntegridadeDadosException,
)

__all__ = [
    # Base
    "AppException",
    # Validation
    "ValidationException",
    "IdadeInvalidaException",
    "NomeInvalidoException",
    "EmailInvalidoException",
    # Business
    "BusinessRuleException",
    # Not Found
    "NotFoundException",
    "AlunoNotFoundException",
    "MateriaNotFoundException",
    "TarefaNotFoundException",
    "TurmaNotFoundException",
    # Database
    "DatabaseException",
    "ConexaoBancoException",
    "IntegridadeDadosException",
]
