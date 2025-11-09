from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models import Materia

class MateriaRepository(BaseRepository[Materia]):
    """Repositório para operações de dados da entidade Materia"""

    def create(self, entity: Materia) -> Materia:
        """Cria uma nova matéria no banco de dados"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, id: int) -> Optional[Materia]:
        """Busca uma matéria por ID"""
        return self.db.query(Materia).filter(Materia.id == id).first()

    def get_all(self) -> List[Materia]:
        """Retorna todas as matérias"""
        return self.db.query(Materia).all()

    def update(self, id: int, **kwargs) -> Optional[Materia]:
        """Atualiza uma matéria existente"""
        materia = self.get_by_id(id)
        if materia:
            for campo, valor in kwargs.items():
                if hasattr(materia, campo):
                    setattr(materia, campo, valor)
            self.db.commit()
            self.db.refresh(materia)
        return materia

    def delete(self, id: int) -> bool:
        """Remove uma matéria do banco de dados"""
        materia = self.get_by_id(id)
        if materia:
            self.db.delete(materia)
            self.db.commit()
            return True
        return False

    def get_by_nome(self, nome: str) -> Optional[Materia]:
        """Busca uma matéria por nome"""
        return self.db.query(Materia).filter(Materia.nome == nome).first()
