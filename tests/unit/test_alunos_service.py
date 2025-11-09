import pytest
from app.services import alunos_service
from app.exceptions import AlunoNotFoundException, TurmaNotFoundException


class MockAlunoCreate:
    """Mock para dados de criação de aluno"""
    def __init__(self, nome, idade, bolsista, turma_id):
        self.nome = nome
        self.idade = idade
        self.bolsista = bolsista
        self.turma_id = turma_id

    def dict(self):
        return {
            "nome": self.nome,
            "idade": self.idade,
            "bolsista": self.bolsista,
            "turma_id": self.turma_id
        }


class TestAlunosService:
    """Testes unitários para alunos_service (5 testes)"""

    def test_criar_aluno_sucesso(self, db_session, turma_sample):
        """Teste de criação de aluno com sucesso"""
        dados = MockAlunoCreate("Carlos", 23, True, turma_sample.id)
        resultado = alunos_service.criar_aluno_service(dados, db_session)
        assert resultado.nome == "Carlos"
        assert resultado.idade == 23

    def test_criar_aluno_turma_inexistente(self, db_session):
        """Teste de criação de aluno com turma inexistente"""
        dados = MockAlunoCreate("Carlos", 23, True, 9999)
        with pytest.raises(TurmaNotFoundException):
            alunos_service.criar_aluno_service(dados, db_session)

    def test_buscar_aluno_por_id(self, db_session, aluno_sample):
        """Teste de busca de aluno por ID"""
        resultado = alunos_service.obter_aluno_service(aluno_sample.id, db_session)
        assert resultado.id == aluno_sample.id

    def test_buscar_aluno_por_id_nao_existe(self, db_session):
        """Teste de busca de aluno inexistente"""
        with pytest.raises(AlunoNotFoundException):
            alunos_service.obter_aluno_service(9999, db_session)

    def test_deletar_aluno(self, db_session, turma_sample):
        """Teste de exclusão de aluno"""
        dados = MockAlunoCreate("Temp", 20, False, turma_sample.id)
        aluno = alunos_service.criar_aluno_service(dados, db_session)
        resultado = alunos_service.deletar_aluno_service(aluno.id, db_session)
        assert "mensagem" in resultado
