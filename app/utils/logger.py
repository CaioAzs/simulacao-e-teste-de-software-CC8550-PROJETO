"""
Sistema de logging configurável para a aplicação.

Este módulo fornece configuração centralizada de logging com suporte a:
- Múltiplos níveis (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Saída para arquivo e console
- Formatação padronizada
- Rotação de arquivos de log
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional


# Níveis de log disponíveis
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}


def setup_logger(
    name: str,
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_bytes: int = 10485760,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Configura e retorna um logger personalizado.

    Args:
        name: Nome do logger (geralmente __name__ do módulo)
        log_level: Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Caminho para arquivo de log (opcional)
        max_bytes: Tamanho máximo do arquivo antes de rotacionar
        backup_count: Número de arquivos de backup a manter

    Returns:
        logging.Logger: Logger configurado

    Example:
        >>> logger = setup_logger(__name__, "DEBUG", "logs/app.log")
        >>> logger.info("Aplicação iniciada")
    """
    logger = logging.getLogger(name)

    # Evita duplicação de handlers
    if logger.handlers:
        return logger

    # Define o nível de log
    level = LOG_LEVELS.get(log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Formato das mensagens de log
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para console (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo (se especificado)
    if log_file:
        # Cria diretório se não existir
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = RotatingFileHandler(
            filename=log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Retorna um logger existente ou cria um novo com configuração padrão.

    Args:
        name: Nome do logger

    Returns:
        logging.Logger: Logger configurado
    """
    return logging.getLogger(name)


# Logger padrão da aplicação
app_logger = setup_logger(
    name="app",
    log_level="INFO",
    log_file="logs/app.log"
)
