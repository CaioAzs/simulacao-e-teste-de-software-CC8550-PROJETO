"""
Testes de API REST - Métodos HTTP e Status Codes
Objetivo: Validar endpoints com diferentes métodos HTTP e respostas JSON
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app, raise_server_exceptions=False)


class TestHTTPMethods:
    """
    Teste 1: Validar diferentes métodos HTTP (GET, POST, PUT, DELETE)
    Objetivo: Verificar que a API responde corretamente aos métodos HTTP
    """

    def test_http_methods_on_alunos_endpoint(self):
        # POST - Criar turma e aluno
        turma_response = client.post("/turmas", json={"nome": "Turma API Test"})
        assert turma_response.status_code == 200
        turma_id = turma_response.json()["id"]

        # POST - Criar aluno
        post_response = client.post("/alunos", json={
            "nome": "Teste HTTP",
            "idade": 16,
            "turma_id": turma_id,
            "bolsista": False
        })
        assert post_response.status_code == 200
        aluno_id = post_response.json()["id"]

        # GET - Buscar aluno
        get_response = client.get(f"/alunos/{aluno_id}")
        assert get_response.status_code == 200

        # PUT - Atualizar aluno
        put_response = client.put(f"/alunos/{aluno_id}", json={
            "nome": "Teste HTTP Atualizado",
            "idade": 17,
            "turma_id": turma_id,
            "bolsista": True
        })
        assert put_response.status_code == 200

        # DELETE - Remover aluno
        delete_response = client.delete(f"/alunos/{aluno_id}")
        assert delete_response.status_code == 200


class TestStatusCodesAndJSON:
    """
    Teste 2: Validar status codes e estrutura de respostas JSON
    Objetivo: Verificar que a API retorna status codes corretos e JSON válido
    """

    def test_status_codes_and_json_structure(self):
        # POST - Criar turma (200 OK com JSON)
        turma_response = client.post("/turmas", json={"nome": "Turma JSON Test"})
        assert turma_response.status_code == 200
        turma_json = turma_response.json()
        assert "id" in turma_json
        assert "nome" in turma_json
        assert turma_json["nome"] == "Turma JSON Test"

        # GET - Listar alunos (200 OK com lista JSON)
        list_response = client.get("/alunos")
        assert list_response.status_code == 200
        alunos_list = list_response.json()
        assert isinstance(alunos_list, list)

        # GET - Buscar aluno inexistente (500 - erro não tratado)
        not_found_response = client.get("/alunos/99999")
        assert not_found_response.status_code == 500
