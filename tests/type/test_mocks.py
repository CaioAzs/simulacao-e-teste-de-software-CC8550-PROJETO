"""
Testes com Mocks e Stubs
Objetivo: Isolar dependências externas e simular diferentes cenários de resposta
"""

import pytest
from unittest.mock import Mock, patch
from app.services.alunos_service import criar_aluno_service, obter_aluno_service
from app.models import Aluno, Turma
from app.exceptions.not_found import TurmaNotFoundException, AlunoNotFoundException


class TestMocksIsolation:
    """
    Teste 1: Isolar dependências de banco de dados usando Mocks
    Objetivo: Testar lógica de serviço sem acessar banco de dados real
    """

    def test_criar_aluno_with_mock_repository(self):
        # Mock do repositório e banco de dados
        mock_db = Mock()
        mock_turma_repo = Mock()
        mock_aluno_repo = Mock()

        # Simular turma existente
        turma_mock = Turma(id=1, nome="Turma Mock")
        mock_turma_repo.get_by_id.return_value = turma_mock

        # Simular criação de aluno
        aluno_criado = Aluno(id=10, nome="Aluno Mock", idade=16, turma_id=1, bolsista=False)
        mock_aluno_repo.create.return_value = aluno_criado

        # Mock do objeto de entrada
        aluno_input = Mock()
        aluno_input.nome = "Aluno Mock"
        aluno_input.idade = 16
        aluno_input.turma_id = 1
        aluno_input.bolsista = False
        aluno_input.dict.return_value = {
            "nome": "Aluno Mock",
            "idade": 16,
            "turma_id": 1,
            "bolsista": False
        }

        # Patch dos repositórios
        with patch('app.services.alunos_service.TurmaRepository', return_value=mock_turma_repo):
            with patch('app.services.alunos_service.AlunoRepository', return_value=mock_aluno_repo):
                resultado = criar_aluno_service(aluno_input, mock_db)

        # Verificações
        assert resultado.id == 10
        assert resultado.nome == "Aluno Mock"
        mock_turma_repo.get_by_id.assert_called_once_with(1)
        mock_aluno_repo.create.assert_called_once()


class TestMocksScenarios:
    """
    Teste 2: Simular diferentes cenários de resposta (sucesso e erro)
    Objetivo: Testar tratamento de exceções quando turma não existe
    """

    def test_criar_aluno_turma_inexistente_with_mock(self):
        # Mock do banco de dados e repositórios
        mock_db = Mock()
        mock_turma_repo = Mock()
        mock_aluno_repo = Mock()

        # Simular turma NÃO existente (retorna None)
        mock_turma_repo.get_by_id.return_value = None

        # Mock do objeto de entrada
        aluno_input = Mock()
        aluno_input.nome = "Aluno Teste"
        aluno_input.idade = 15
        aluno_input.turma_id = 999  # ID inexistente
        aluno_input.bolsista = False

        # Patch dos repositórios
        with patch('app.services.alunos_service.TurmaRepository', return_value=mock_turma_repo):
            with patch('app.services.alunos_service.AlunoRepository', return_value=mock_aluno_repo):
                # Verificar que exceção é lançada
                with pytest.raises(TurmaNotFoundException) as excinfo:
                    criar_aluno_service(aluno_input, mock_db)

        # Verificações
        assert "Turma com ID 999 não encontrada" in str(excinfo.value)
        mock_turma_repo.get_by_id.assert_called_once_with(999)
        mock_aluno_repo.create.assert_not_called()  # Não deve tentar criar aluno
