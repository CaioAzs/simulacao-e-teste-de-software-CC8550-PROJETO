"""
Exceção base para toda a aplicação.
"""


class AppException(Exception):
    """
    Classe base para todas as exceções customizadas da aplicação.

    Todas as exceções específicas do projeto devem herdar desta classe,
    permitindo captura centralizada e tratamento consistente de erros.

    Attributes:
        message (str): Mensagem de erro descritiva
        details (dict): Detalhes adicionais sobre o erro (opcional)
    """

    def __init__(self, message: str, details: dict = None):
        """
        Inicializa a exceção base.

        Args:
            message: Mensagem descritiva do erro
            details: Dicionário com informações adicionais sobre o erro
        """
        self.message = message
        self.details = details or {}
        super().__init__(self.message)

    def __str__(self) -> str:
        """Retorna representação em string da exceção."""
        if self.details:
            return f"{self.message} - Detalhes: {self.details}"
        return self.message

    def to_dict(self) -> dict:
        """
        Converte a exceção para dicionário (útil para APIs REST).

        Returns:
            dict: Dicionário com informações da exceção
        """
        return {
            "error": self.__class__.__name__,
            "message": self.message,
            "details": self.details
        }
