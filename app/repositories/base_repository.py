from abc import ABC, abstractmethod
from typing import Generic, TypeVar, List, Optional
from sqlalchemy.orm import Session

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """
    Interface abstrata para repositórios de dados.
    Define operações CRUD básicas que devem ser implementadas.
    """

    def __init__(self, db: Session):
        self.db = db

    @abstractmethod
    def create(self, entity: T) -> T:
        """Cria uma nova entidade no banco de dados"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[T]:
        """Busca uma entidade por ID"""
        pass

    @abstractmethod
    def get_all(self) -> List[T]:
        """Retorna todas as entidades"""
        pass

    @abstractmethod
    def update(self, id: int, **kwargs) -> Optional[T]:
        """Atualiza uma entidade existente"""
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        """Remove uma entidade do banco de dados"""
        pass
