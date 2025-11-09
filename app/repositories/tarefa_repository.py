from typing import List, Optional
from sqlalchemy.orm import Session
from app.repositories.base_repository import BaseRepository
from app.models import Tarefa

class TarefaRepository(BaseRepository[Tarefa]):
    """Repositório para operações de dados da entidade Tarefa"""

    def create(self, entity: Tarefa) -> Tarefa:
        """Cria uma nova tarefa no banco de dados"""
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def get_by_id(self, id: int) -> Optional[Tarefa]:
        """Busca uma tarefa por ID"""
        return self.db.query(Tarefa).filter(Tarefa.id == id).first()

    def get_all(self) -> List[Tarefa]:
        """Retorna todas as tarefas"""
        return self.db.query(Tarefa).all()

    def update(self, id: int, **kwargs) -> Optional[Tarefa]:
        """Atualiza uma tarefa existente"""
        tarefa = self.get_by_id(id)
        if tarefa:
            for campo, valor in kwargs.items():
                if hasattr(tarefa, campo):
                    setattr(tarefa, campo, valor)
            self.db.commit()
            self.db.refresh(tarefa)
        return tarefa

    def delete(self, id: int) -> bool:
        """Remove uma tarefa do banco de dados"""
        tarefa = self.get_by_id(id)
        if tarefa:
            self.db.delete(tarefa)
            self.db.commit()
            return True
        return False

    def get_by_aluno_id(self, aluno_id: int) -> List[Tarefa]:
        """Busca tarefas por ID do aluno"""
        return self.db.query(Tarefa).filter(Tarefa.aluno_id == aluno_id).all()

    def get_pendentes_by_aluno(self, aluno_id: int) -> List[Tarefa]:
        """Busca tarefas pendentes de um aluno"""
        return self.db.query(Tarefa).filter(
            Tarefa.aluno_id == aluno_id,
            Tarefa.concluido == False
        ).all()
