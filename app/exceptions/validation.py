"""
Exceções relacionadas a validação de dados.
"""

from .base import AppException


class ValidationException(AppException):
    """
    Exceção base para erros de validação de dados.

    Levantada quando dados fornecidos pelo usuário não atendem
    aos critérios de validação esperados.
    """
    pass


class IdadeInvalidaException(ValidationException):
    """
    Exceção para idade fora do intervalo permitido.

    Examples:
        >>> raise IdadeInvalidaException("Idade deve estar entre 10 e 100 anos")
    """

    def __init__(self, idade: int = None, min_idade: int = 0, max_idade: int = 150):
        message = f"Idade inválida"
        details = {}

        if idade is not None:
            message = f"Idade {idade} está fora do intervalo permitido"
            details = {
                "idade_fornecida": idade,
                "idade_minima": min_idade,
                "idade_maxima": max_idade
            }

        super().__init__(message, details)


class NomeInvalidoException(ValidationException):
    """
    Exceção para nome inválido ou vazio.

    Examples:
        >>> raise NomeInvalidoException("Nome não pode ser vazio")
    """

    def __init__(self, motivo: str = "Nome inválido"):
        super().__init__(motivo)


class EmailInvalidoException(ValidationException):
    """
    Exceção para email em formato inválido.

    Examples:
        >>> raise EmailInvalidoException("usuario@exemplo")
    """

    def __init__(self, email: str = None):
        message = "Email inválido"
        details = {}

        if email:
            message = f"Email '{email}' está em formato inválido"
            details = {"email_fornecido": email}

        super().__init__(message, details)
