import pytest
from app.repositories import AlunoRepository, TurmaRepository, MateriaRepository, TarefaRepository
from app.models import Aluno, Turma, Materia, Tarefa


class TestAlunoRepository:
    """Testes unitários para AlunoRepository (8 testes)"""

    def test_create_aluno(self, db_session, turma_sample):
        """Teste de criação de aluno"""
        repo = AlunoRepository(db_session)
        aluno = Aluno(nome="Maria", idade=22, bolsista=False, turma_id=turma_sample.id)
        resultado = repo.create(aluno)
        assert resultado.id is not None
        assert resultado.nome == "Maria"

    def test_get_by_id_aluno(self, db_session, aluno_sample):
        """Teste de busca de aluno por ID"""
        repo = AlunoRepository(db_session)
        resultado = repo.get_by_id(aluno_sample.id)
        assert resultado is not None
        assert resultado.id == aluno_sample.id

    def test_get_by_id_aluno_nao_existe(self, db_session):
        """Teste de busca de aluno inexistente"""
        repo = AlunoRepository(db_session)
        resultado = repo.get_by_id(9999)
        assert resultado is None

    def test_get_all_alunos(self, db_session, aluno_sample):
        """Teste de listagem de todos os alunos"""
        repo = AlunoRepository(db_session)
        resultado = repo.get_all()
        assert len(resultado) >= 1

    def test_update_aluno(self, db_session, aluno_sample):
        """Teste de atualização de aluno"""
        repo = AlunoRepository(db_session)
        repo.update(aluno_sample.id, nome="João Updated")
        resultado = repo.get_by_id(aluno_sample.id)
        assert resultado.nome == "João Updated"

    def test_delete_aluno(self, db_session, aluno_sample):
        """Teste de exclusão de aluno"""
        repo = AlunoRepository(db_session)
        repo.delete(aluno_sample.id)
        resultado = repo.get_by_id(aluno_sample.id)
        assert resultado is None

    @pytest.mark.parametrize("nome,idade", [("Ana", 20), ("Carlos", 25), ("Beatriz", 22)])
    def test_create_aluno_parametrizado(self, db_session, turma_sample, nome, idade):
        """Teste parametrizado de criação de múltiplos alunos"""
        repo = AlunoRepository(db_session)
        aluno = Aluno(nome=nome, idade=idade, bolsista=True, turma_id=turma_sample.id)
        resultado = repo.create(aluno)
        assert resultado.nome == nome
        assert resultado.idade == idade


class TestTurmaRepository:
    """Testes unitários para TurmaRepository (3 testes)"""

    def test_create_turma(self, db_session):
        """Teste de criação de turma"""
        repo = TurmaRepository(db_session)
        turma = Turma(nome="Turma B")
        resultado = repo.create(turma)
        assert resultado.id is not None

    def test_get_by_id_turma(self, db_session, turma_sample):
        """Teste de busca de turma por ID"""
        repo = TurmaRepository(db_session)
        resultado = repo.get_by_id(turma_sample.id)
        assert resultado is not None

    def test_get_all_turmas(self, db_session, turma_sample):
        """Teste de listagem de todas as turmas"""
        repo = TurmaRepository(db_session)
        resultado = repo.get_all()
        assert len(resultado) >= 1


class TestMateriaRepository:
    """Testes unitários para MateriaRepository (3 testes)"""

    def test_create_materia(self, db_session):
        """Teste de criação de matéria"""
        repo = MateriaRepository(db_session)
        materia = Materia(nome="Física")
        resultado = repo.create(materia)
        assert resultado.id is not None

    def test_get_by_id_materia(self, db_session, materia_sample):
        """Teste de busca de matéria por ID"""
        repo = MateriaRepository(db_session)
        resultado = repo.get_by_id(materia_sample.id)
        assert resultado is not None

    def test_get_all_materias(self, db_session, materia_sample):
        """Teste de listagem de todas as matérias"""
        repo = MateriaRepository(db_session)
        resultado = repo.get_all()
        assert len(resultado) >= 1


class TestTarefaRepository:
    """Testes unitários para TarefaRepository (4 testes)"""

    def test_create_tarefa(self, db_session, aluno_sample, materia_sample):
        """Teste de criação de tarefa"""
        repo = TarefaRepository(db_session)
        tarefa = Tarefa(nome="Trabalho 1", materia_id=materia_sample.id, aluno_id=aluno_sample.id, concluido=False)
        resultado = repo.create(tarefa)
        assert resultado.id is not None
        assert resultado.concluido is False

    def test_get_by_id_tarefa(self, db_session, tarefa_sample):
        """Teste de busca de tarefa por ID"""
        repo = TarefaRepository(db_session)
        resultado = repo.get_by_id(tarefa_sample.id)
        assert resultado is not None

    def test_update_tarefa_concluido(self, db_session, tarefa_sample):
        """Teste de atualização de tarefa para concluído"""
        repo = TarefaRepository(db_session)
        repo.update(tarefa_sample.id, concluido=True)
        resultado = repo.get_by_id(tarefa_sample.id)
        assert resultado.concluido is True

    def test_delete_tarefa(self, db_session, tarefa_sample):
        """Teste de exclusão de tarefa"""
        repo = TarefaRepository(db_session)
        repo.delete(tarefa_sample.id)
        resultado = repo.get_by_id(tarefa_sample.id)
        assert resultado is None
