def create_turma(client, nome):
    r = client.post("/turmas", json={"nome": nome})
    assert r.status_code == 200
    return r.json()


def create_aluno(client, turma_id, nome, idade=18, bolsista=False):
    r = client.post("/alunos", json={"nome": nome, "idade": idade, "bolsista": bolsista, "turma_id": turma_id})
    assert r.status_code == 200
    return r.json()


def create_materia(client, nome):
    r = client.post("/materias", json={"nome": nome})
    assert r.status_code == 200
    return r.json()


def create_tarefa(client, nome, materia_id, aluno_id):
    r = client.post("/tarefas", json={"nome": nome, "materia_id": materia_id, "aluno_id": aluno_id})
    assert r.status_code == 200
    return r.json()


def test_cria_e_lista_turma(client):
    turma = create_turma(client, "Turma 1")
    resp = client.get("/turmas")
    assert resp.status_code == 200
    assert any(item["id"] == turma["id"] for item in resp.json())


def test_cria_aluno_fluxo_completo(client):
    turma = create_turma(client, "Turma 2")
    aluno = create_aluno(client, turma["id"], "Aluno 2", bolsista=True)
    resp = client.get("/alunos")
    assert resp.status_code == 200
    assert any(item["id"] == aluno["id"] for item in resp.json())
    bolsistas = client.get("/turmas/mais-bolsistas")
    assert bolsistas.status_code == 200
    assert any(item["id"] == turma["id"] for item in bolsistas.json())


def test_obter_aluno(client):
    turma = create_turma(client, "Turma 3")
    aluno = create_aluno(client, turma["id"], "Aluno 3")
    resp = client.get(f"/alunos/{aluno['id']}")
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Aluno 3"


def test_atualiza_aluno(client):
    turma = create_turma(client, "Turma 4")
    aluno = create_aluno(client, turma["id"], "Aluno 4")
    resp = client.put(f"/alunos/{aluno['id']}", json={"nome": "Aluno 4 Atualizado", "idade": 25, "bolsista": True, "turma_id": turma["id"]})
    assert resp.status_code == 200
    assert resp.json()["nome"] == "Aluno 4 Atualizado"


def test_deleta_aluno(client):
    turma = create_turma(client, "Turma 5")
    aluno = create_aluno(client, turma["id"], "Aluno 5")
    resp = client.delete(f"/alunos/{aluno['id']}")
    assert resp.status_code == 200
    lista = client.get("/alunos").json()
    assert all(item["id"] != aluno["id"] for item in lista)


def test_cria_materia_fluxo(client):
    materia = create_materia(client, "Materia 6")
    resp = client.get("/materias")
    assert resp.status_code == 200
    assert any(item["id"] == materia["id"] for item in resp.json())


def test_atribui_materia_para_turma(client):
    turma = create_turma(client, "Turma 7")
    aluno = create_aluno(client, turma["id"], "Aluno 7")
    materia = create_materia(client, "Materia 7")
    resp = client.post(f"/materias/turma/{turma['id']}", json={"materias_ids": [materia["id"]]})
    assert resp.status_code == 200
    alunos = client.get(f"/materias/{materia['id']}/alunos")
    assert alunos.status_code == 200
    assert any(item["id"] == aluno["id"] for item in alunos.json())
    populares = client.get("/materias/mais-alunos")
    assert populares.status_code == 200
    assert any(item["id"] == materia["id"] for item in populares.json())


def test_cria_e_conclui_tarefa(client):
    turma = create_turma(client, "Turma 8")
    aluno = create_aluno(client, turma["id"], "Aluno 8")
    materia = create_materia(client, "Materia 8")
    tarefa = create_tarefa(client, "Tarefa 8", materia["id"], aluno["id"])
    assert tarefa["concluido"] is False
    lista = client.get(f"/tarefas/aluno/{aluno['id']}").json()
    assert any(item["id"] == tarefa["id"] for item in lista)
    resp = client.put(f"/tarefas/{tarefa['id']}/concluir")
    assert resp.status_code == 200
    ver = client.get(f"/tarefas/aluno/{aluno['id']}").json()
    assert any(item["concluido"] is True for item in ver)


def test_atribui_tarefa_para_aluno(client):
    turma = create_turma(client, "Turma 9")
    aluno = create_aluno(client, turma["id"], "Aluno 9")
    materia = create_materia(client, "Materia 9")
    resp = client.post(f"/tarefas/aluno/{aluno['id']}", json={"nome": "Tarefa Unica", "materia_id": materia["id"]})
    assert resp.status_code == 200
    tarefa = resp.json()["tarefa"]
    lista = client.get(f"/tarefas/aluno/{aluno['id']}").json()
    assert any(item["id"] == tarefa["id"] for item in lista)


def test_atribui_tarefa_para_turma(client):
    turma = create_turma(client, "Turma 10")
    aluno1 = create_aluno(client, turma["id"], "Aluno 10A")
    aluno2 = create_aluno(client, turma["id"], "Aluno 10B")
    materia = create_materia(client, "Materia 10")
    resp = client.post(f"/tarefas/turma/{turma['id']}", json={"nome": "Tarefa Turma", "materia_id": materia["id"]})
    assert resp.status_code == 200
    assert len(resp.json()["tarefas"]) == 2
    ranking_resp = client.get("/alunos/mais-pendentes")
    assert ranking_resp.status_code == 200
    ranking = ranking_resp.json()
    assert len(ranking) >= 2
    ids = {item["id"]: item.get("pendentes", 0) for item in ranking}
    assert ids.get(aluno1["id"]) == 1 and ids.get(aluno2["id"]) == 1
