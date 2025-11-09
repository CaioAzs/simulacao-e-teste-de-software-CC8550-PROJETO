from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models import Turma

class TurmaRepository(BaseRepository[Turma]):
    """Repositório para operações de dados da entidade Turma"""

    def create(self, entity: Turma) -> Turma:
        """Cria uma nova turma no banco de dados"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, id: int) -> Optional[Turma]:
        """Busca uma turma por ID"""
        return self.db.query(Turma).filter(Turma.id == id).first()

    def get_all(self) -> List[Turma]:
        """Retorna todas as turmas"""
        return self.db.query(Turma).all()

    def update(self, id: int, **kwargs) -> Optional[Turma]:
        """Atualiza uma turma existente"""
        turma = self.get_by_id(id)
        if turma:
            for campo, valor in kwargs.items():
                if hasattr(turma, campo):
                    setattr(turma, campo, valor)
            self.db.commit()
            self.db.refresh(turma)
        return turma

    def delete(self, id: int) -> bool:
        """Remove uma turma do banco de dados"""
        turma = self.get_by_id(id)
        if turma:
            self.db.delete(turma)
            self.db.commit()
            return True
        return False

    def get_by_nome(self, nome: str) -> Optional[Turma]:
        """Busca uma turma por nome"""
        return self.db.query(Turma).filter(Turma.nome == nome).first()
