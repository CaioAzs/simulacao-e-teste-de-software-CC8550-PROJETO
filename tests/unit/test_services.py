import pytest
from app.services import tarefas_service, materias_service, turmas_service
from app.exceptions import TarefaNotFoundException, MateriaNotFoundException, TurmaNotFoundException


class MockTarefaCreate:
    """Mock para dados de criação de tarefa"""
    def __init__(self, nome, materia_id, aluno_id=None):
        self.nome = nome
        self.materia_id = materia_id
        self.aluno_id = aluno_id

    def dict(self):
        return {
            "nome": self.nome,
            "materia_id": self.materia_id,
            "aluno_id": self.aluno_id,
            "concluido": False
        }


class MockMateriaCreate:
    """Mock para dados de criação de matéria"""
    def __init__(self, nome):
        self.nome = nome

    def dict(self):
        return {"nome": self.nome}


class MockTurmaCreate:
    """Mock para dados de criação de turma"""
    def __init__(self, nome):
        self.nome = nome

    def dict(self):
        return {"nome": self.nome}


class TestTarefasService:
    """Testes unitários para tarefas_service (3 testes)"""

    def test_criar_tarefa_sucesso(self, db_session, aluno_sample, materia_sample):
        """Teste de criação de tarefa com sucesso"""
        dados = MockTarefaCreate("Prova 1", materia_sample.id, aluno_sample.id)
        resultado = tarefas_service.criar_tarefa_service(dados, db_session)
        assert resultado.nome == "Prova 1"
        assert resultado.concluido is False

    def test_concluir_tarefa(self, db_session, tarefa_sample):
        """Teste de marcar tarefa como concluída"""
        resultado = tarefas_service.concluir_tarefa_service(tarefa_sample.id, db_session)
        assert "mensagem" in resultado

    def test_concluir_tarefa_inexistente(self, db_session):
        """Teste de concluir tarefa inexistente"""
        with pytest.raises(TarefaNotFoundException):
            tarefas_service.concluir_tarefa_service(9999, db_session)


class TestMateriasService:
    """Testes unitários para materias_service (2 testes)"""

    def test_criar_materia_sucesso(self, db_session):
        """Teste de criação de matéria com sucesso"""
        dados = MockMateriaCreate("Química")
        resultado = materias_service.criar_materia_service(dados, db_session)
        assert resultado.nome == "Química"

    def test_listar_materias(self, db_session, materia_sample):
        """Teste de listagem de matérias"""
        resultado = materias_service.listar_materias_service(db_session)
        assert len(resultado) >= 1


class TestTurmasService:
    """Testes unitários para turmas_service (2 testes)"""

    def test_criar_turma_sucesso(self, db_session):
        """Teste de criação de turma com sucesso"""
        dados = MockTurmaCreate("Turma Z")
        resultado = turmas_service.criar_turma_service(dados, db_session)
        assert resultado.nome == "Turma Z"

    def test_listar_turmas(self, db_session, turma_sample):
        """Teste de listagem de turmas"""
        resultado = turmas_service.listar_turmas_service(db_session)
        assert len(resultado) >= 1
