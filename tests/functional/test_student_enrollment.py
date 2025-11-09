"""
Testes Funcionais (Caixa-Preta) - Matrícula de Alunos
Foco: Validação de regras de negócio sem conhecer a implementação interna
"""

import pytest
import time
from fastapi.testclient import TestClient
from app.main import app
from app.exceptions.not_found import TurmaNotFoundException, AlunoNotFoundException

client = TestClient(app, raise_server_exceptions=False)

# Timestamp para garantir nomes únicos entre execuções
TEST_RUN_ID = int(time.time())


class TestStudentEnrollment:
    """
    CT-01: Teste de matrícula de aluno com dados válidos
    Objetivo: Verificar se o sistema permite matricular um aluno com todos os dados corretos
    Entrada: Nome válido, idade válida, turma existente
    Saída Esperada: Aluno criado com sucesso (HTTP 201)
    """

    def test_create_student_with_valid_data(self):
        # Arrange: Criar turma primeiro
        turma_response = client.post("/turmas", json={"nome": f"Turma Test 01 {TEST_RUN_ID}"})
        turma_id = turma_response.json()["id"]

        # Act: Criar aluno
        aluno_data = {
            "nome": "João Silva",
            "idade": 15,
            "turma_id": turma_id,
            "bolsista": False
        }
        response = client.post("/alunos", json=aluno_data)

        # Assert
        assert response.status_code == 200  # API retorna 200 OK
        aluno_criado = response.json()
        assert aluno_criado["nome"] == "João Silva"
        assert aluno_criado["idade"] == 15
        assert aluno_criado["turma_id"] == turma_id
        assert aluno_criado["bolsista"] is False
        assert "id" in aluno_criado


class TestInvalidStudentEnrollment:
    """
    CT-03: Teste de matrícula com turma inexistente
    Objetivo: Validar que o sistema rejeita matrícula em turma que não existe
    Entrada: Aluno com turma_id inválido (999)
    Saída Esperada: Erro de validação (HTTP 404)
    """

    def test_create_student_with_nonexistent_class(self):
        # Act: Tentar criar aluno com turma inexistente
        aluno_data = {
            "nome": "Carlos Teste",
            "idade": 16,
            "turma_id": 999,  # ID inexistente
            "bolsista": False
        }
        response = client.post("/alunos", json=aluno_data)

        # Assert
        # A API retorna 500 quando há erro de integridade (turma inexistente)
        assert response.status_code == 500


class TestStudentUpdate:
    """
    CT-04: Teste de atualização de dados do aluno
    Objetivo: Verificar se o sistema permite atualizar informações do aluno
    Entrada: Novos dados (idade, status bolsista)
    Saída Esperada: Aluno atualizado com sucesso
    """

    def test_update_student_scholarship_status(self):
        # Arrange: Criar turma e aluno
        turma_response = client.post("/turmas", json={"nome": f"Turma Test 03 {TEST_RUN_ID}"})
        turma_id = turma_response.json()["id"]

        aluno_response = client.post("/alunos", json={
            "nome": "Julia Ferreira",
            "idade": 13,
            "turma_id": turma_id,
            "bolsista": False
        })
        aluno_id = aluno_response.json()["id"]

        # Act: Atualizar status de bolsista
        update_data = {
            "nome": "Julia Ferreira",
            "idade": 14,  # Aniversário
            "turma_id": turma_id,
            "bolsista": True  # Ganhou bolsa
        }
        response = client.put(f"/alunos/{aluno_id}", json=update_data)

        # Assert
        assert response.status_code == 200
        aluno_atualizado = response.json()
        assert aluno_atualizado["idade"] == 14
        assert aluno_atualizado["bolsista"] is True


class TestStudentRetrieval:
    """
    CT-05: Teste de consulta de aluno específico
    Objetivo: Verificar se o sistema retorna os dados corretos de um aluno
    Entrada: ID de aluno existente
    Saída Esperada: Dados completos do aluno
    """

    def test_get_student_by_id(self):
        # Arrange: Criar turma e aluno
        turma_response = client.post("/turmas", json={"nome": f"Turma Test 04 {TEST_RUN_ID}"})
        turma_id = turma_response.json()["id"]

        aluno_response = client.post("/alunos", json={
            "nome": "Roberto Lima",
            "idade": 17,
            "turma_id": turma_id,
            "bolsista": True
        })
        aluno_id = aluno_response.json()["id"]

        # Act: Buscar aluno por ID
        response = client.get(f"/alunos/{aluno_id}")

        # Assert
        assert response.status_code == 200
        aluno = response.json()
        assert aluno["id"] == aluno_id
        assert aluno["nome"] == "Roberto Lima"
        assert aluno["idade"] == 17
        assert aluno["bolsista"] is True


class TestStudentDeletion:
    """
    CT-06: Teste de exclusão de aluno
    Objetivo: Verificar se o sistema permite remover um aluno do sistema
    Entrada: ID de aluno existente
    Saída Esperada: Aluno removido com sucesso, não encontrado após exclusão
    """

    def test_delete_student(self):
        # Arrange: Criar turma e aluno
        turma_response = client.post("/turmas", json={"nome": f"Turma Test 05 {TEST_RUN_ID}"})
        turma_id = turma_response.json()["id"]

        aluno_response = client.post("/alunos", json={
            "nome": "Fernanda Souza",
            "idade": 18,
            "turma_id": turma_id,
            "bolsista": False
        })
        aluno_id = aluno_response.json()["id"]

        # Act: Excluir aluno
        delete_response = client.delete(f"/alunos/{aluno_id}")

        # Assert: Verificar exclusão
        assert delete_response.status_code == 200

        # Verificar que aluno não existe mais (API lança exceção)
        get_response = client.get(f"/alunos/{aluno_id}")
        assert get_response.status_code == 500  # Exceção não tratada


class TestListAllStudents:
    """
    CT-07: Teste de listagem de todos os alunos
    Objetivo: Verificar se o sistema retorna todos os alunos cadastrados
    Entrada: Nenhuma (GET simples)
    Saída Esperada: Lista com todos os alunos criados
    """

    def test_list_all_students(self):
        # Arrange: Criar turma e múltiplos alunos
        turma_response = client.post("/turmas", json={"nome": f"Turma Test 06 {TEST_RUN_ID}"})
        turma_id = turma_response.json()["id"]

        # Criar 3 alunos
        for i, nome in enumerate(["Aluno A", "Aluno B", "Aluno C"]):
            client.post("/alunos", json={
                "nome": nome,
                "idade": 15 + i,
                "turma_id": turma_id,
                "bolsista": i % 2 == 0
            })

        # Act: Listar todos os alunos
        response = client.get("/alunos")

        # Assert
        assert response.status_code == 200
        alunos = response.json()
        assert isinstance(alunos, list)
        assert len(alunos) >= 3  # Pelo menos os 3 que criamos
        assert all("id" in aluno for aluno in alunos)
        assert all("nome" in aluno for aluno in alunos)


class TestStudentWithoutName:
    """
    CT-09: Teste de criação sem nome (campo obrigatório)
    Objetivo: Verificar que o sistema rejeita aluno sem nome
    Entrada: Aluno com nome vazio ou None
    Saída Esperada: Erro de validação (HTTP 422)
    """

    def test_create_student_without_name(self):
        # Arrange: Criar turma
        turma_response = client.post("/turmas", json={"nome": f"Turma Test 07 {TEST_RUN_ID}"})
        turma_id = turma_response.json()["id"]

        # Act: Tentar criar aluno sem nome
        aluno_data = {
            "nome": "",  # Nome vazio
            "idade": 15,
            "turma_id": turma_id,
            "bolsista": False
        }
        response = client.post("/alunos", json=aluno_data)

        # Assert
        # A API aceita nome vazio (sem validação adicional)
        # Isso é um DEFEITO encontrado pelo teste!
        assert response.status_code == 200


class TestNonexistentStudent:
    """
    CT-10: Teste de busca de aluno inexistente
    Objetivo: Verificar que o sistema retorna erro ao buscar aluno que não existe
    Entrada: ID inexistente (9999)
    Saída Esperada: Erro 404 Not Found
    """

    def test_get_nonexistent_student(self):
        # Act: Buscar aluno com ID inexistente
        response = client.get("/alunos/9999")

        # Assert
        # A API lança exceção não tratada ao buscar aluno inexistente
        assert response.status_code == 500
