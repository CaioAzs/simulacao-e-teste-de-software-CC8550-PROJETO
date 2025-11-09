from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models import Aluno

class AlunoRepository(BaseRepository[Aluno]):
    """Repositório para operações de dados da entidade Aluno"""

    def create(self, entity: Aluno) -> Aluno:
        """Cria um novo aluno no banco de dados"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, id: int) -> Optional[Aluno]:
        """Busca um aluno por ID"""
        return self.db.query(Aluno).filter(Aluno.id == id).first()

    def get_all(self) -> List[Aluno]:
        """Retorna todos os alunos"""
        return self.db.query(Aluno).all()

    def update(self, id: int, **kwargs) -> Optional[Aluno]:
        """Atualiza um aluno existente"""
        aluno = self.get_by_id(id)
        if aluno:
            for campo, valor in kwargs.items():
                if hasattr(aluno, campo):
                    setattr(aluno, campo, valor)
            self.db.commit()
            self.db.refresh(aluno)
        return aluno

    def delete(self, id: int) -> bool:
        """Remove um aluno do banco de dados"""
        aluno = self.get_by_id(id)
        if aluno:
            self.db.delete(aluno)
            self.db.commit()
            return True
        return False

    def get_by_turma_id(self, turma_id: int) -> List[Aluno]:
        """Busca alunos por ID da turma"""
        return self.db.query(Aluno).filter(Aluno.turma_id == turma_id).all()
