"""
Exceções relacionadas a regras de negócio.
"""

from .base import AppException


class BusinessRuleException(AppException):
    """
    Exceção para violações de regras de negócio.
    """
    pass
