import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models.models import Turma, Aluno, Materia, Tarefa
from app.repositories import (
    TurmaRepository,
    AlunoRepository,
    MateriaRepository,
    TarefaRepository,
)
from app.services.alunos_service import (
    criar_aluno_service,
    listar_alunos_service,
    obter_aluno_service,
    atualizar_aluno_service,
    deletar_aluno_service,
    alunos_com_mais_tarefas_pendentes_service,
    criar_alunos_em_lote_service,
)
from app.services.turmas_service import (
    criar_turma_service,
    listar_turmas_service,
    listar_alunos_da_turma_service,
    turmas_com_mais_bolsistas_service,
)
from app.services.tarefas_service import (
    criar_tarefa_service,
    concluir_tarefa_service,
    atribuir_tarefa_para_turma_service,
    listar_tarefas_do_aluno_service,
    atribuir_tarefa_para_aluno_service,
)
from app.exceptions import (
    AlunoNotFoundException,
    TurmaNotFoundException,
    MateriaNotFoundException,
    TarefaNotFoundException,
)


class DummyAlunoDTO:
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
            "turma_id": self.turma_id,
        }


class DummyTarefaDTO:
    def __init__(self, nome, materia_id, aluno_id=None):
        self.nome = nome
        self.materia_id = materia_id
        self.aluno_id = aluno_id

    def dict(self):
        return {
            "nome": self.nome,
            "materia_id": self.materia_id,
            "aluno_id": self.aluno_id,
        }


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def setup_dados(db_session):
    turma_repo = TurmaRepository(db_session)
    aluno_repo = AlunoRepository(db_session)
    materia_repo = MateriaRepository(db_session)
    tarefa_repo = TarefaRepository(db_session)

    turma = turma_repo.create(Turma(nome="Turma Estrutural"))
    outra_turma = turma_repo.create(Turma(nome="Turma Vazios"))
    materia = materia_repo.create(Materia(nome="Matemtica Estrutural"))

    aluno1 = aluno_repo.create(Aluno(nome="Aluno Alpha", idade=18, bolsista=True, turma_id=turma.id))
    aluno2 = aluno_repo.create(Aluno(nome="Aluno Beta", idade=19, bolsista=False, turma_id=turma.id))
    aluno_repo.create(Aluno(nome="Aluno Gamma", idade=20, bolsista=True, turma_id=outra_turma.id))
    tarefa_repo.create(Tarefa(nome="Tarefa Antiga", materia_id=materia.id, aluno_id=aluno1.id, concluido=False))
    tarefa_repo.create(Tarefa(nome="Tarefa Conclu da", materia_id=materia.id, aluno_id=aluno2.id, concluido=True))

    return {
        "turma": turma,
        "outra_turma": outra_turma,
        "materia": materia,
        "aluno1": aluno1,
        "aluno2": aluno2,
        "turma_repo": turma_repo,
        "aluno_repo": aluno_repo,
        "materia_repo": materia_repo,
        "tarefa_repo": tarefa_repo,
    }


def test_crud_aluno_branches(db_session, setup_dados):
    turma = setup_dados["turma"]

    novo_dto = DummyAlunoDTO("Aluno Novo", 21, False, turma.id)
    criado = criar_aluno_service(novo_dto, db_session)
    assert criado.id is not None

    alunos = listar_alunos_service(db_session)
    assert any(a.id == criado.id for a in alunos)

    obtido = obter_aluno_service(criado.id, db_session)
    assert obtido.nome == "Aluno Novo"

    atualizado_dto = DummyAlunoDTO("Aluno Atualizado", 22, True, turma.id)
    atualizado = atualizar_aluno_service(criado.id, atualizado_dto, db_session)
    assert atualizado.nome == "Aluno Atualizado"
    assert atualizar_aluno_service(criado.id, atualizado_dto, db_session).bolsista is True

    resposta = deletar_aluno_service(criado.id, db_session)
    assert resposta["mensagem"].startswith("Aluno removido")

    with pytest.raises(AlunoNotFoundException):
        obter_aluno_service(criado.id, db_session)

    with pytest.raises(AlunoNotFoundException):
        atualizar_aluno_service(9999, atualizado_dto, db_session)

    with pytest.raises(AlunoNotFoundException):
        deletar_aluno_service(9999, db_session)

    with pytest.raises(TurmaNotFoundException):
        criar_aluno_service(DummyAlunoDTO("Aluno Sem Turma", 18, False, 9999), db_session)

def test_alunos_cenarios_coletivos(db_session, setup_dados):
    turma = setup_dados["turma"]
    outra_turma = setup_dados["outra_turma"]

    lote = [
        DummyAlunoDTO(f"Aluno Lote {i}", 18 + i, i % 2 == 0, turma.id) for i in range(3)
    ]
    criados = criar_alunos_em_lote_service(lote, db_session)
    assert len(criados) == 3

    pendentes = alunos_com_mais_tarefas_pendentes_service(db_session)
    ids = {item["id"]: item["pendentes"] for item in pendentes}
    assert ids[setup_dados["aluno1"].id] >= 1

    lote_invalido = [
        DummyAlunoDTO("Aluno Falho", 19, False, outra_turma.id),
        DummyAlunoDTO("Aluno Sem Turma", 19, False, 9999),
    ]
    with pytest.raises(TurmaNotFoundException):
        criar_alunos_em_lote_service(lote_invalido, db_session)
    db_session.query(Tarefa).filter(Tarefa.aluno_id == setup_dados["aluno1"].id).update({"concluido": True})
    db_session.commit()

    pendentes_vazio = alunos_com_mais_tarefas_pendentes_service(db_session)
    if pendentes_vazio:
        ids_final = {item["id"]: item["pendentes"] for item in pendentes_vazio}
        assert ids_final.get(setup_dados["aluno1"].id, 0) == 0
        assert any(item["pendentes"] == 0 for item in pendentes_vazio)
    else:
        assert pendentes_vazio == []


def test_turmas_branches(db_session, setup_dados):
    turma = setup_dados["turma"]
    outra_turma = setup_dados["outra_turma"]

    nova = criar_turma_service(type("TurmaDTO", (), {"nome": "Turma Estrutural Nova"}), db_session)
    assert nova.nome == "Turma Estrutural Nova"

    turmas = listar_turmas_service(db_session)
    assert any(t["id"] == turma.id and len(t["alunos"]) >= 2 for t in turmas)

    alunos_turma = listar_alunos_da_turma_service(turma.id, db_session)
    assert len(alunos_turma) >= 2

    with pytest.raises(TurmaNotFoundException):
        listar_alunos_da_turma_service(9999, db_session)

    alunos_outra = listar_alunos_da_turma_service(outra_turma.id, db_session)
    assert len(alunos_outra) >= 1

    bolsistas = turmas_com_mais_bolsistas_service(db_session)
    assert any(item["total_bolsistas"] >= 1 for item in bolsistas)


def test_tarefas_branches(db_session, setup_dados):
    turma = setup_dados["turma"]
    materia = setup_dados["materia"]
    aluno1 = setup_dados["aluno1"]
    aluno2 = setup_dados["aluno2"]

    tarefa_dto = DummyTarefaDTO("Tarefa Estrutural", materia.id, aluno1.id)
    tarefa = criar_tarefa_service(tarefa_dto, db_session)
    assert tarefa.concluido is False

    tarefas_aluno = listar_tarefas_do_aluno_service(aluno1.id, db_session)
    assert any(item["id"] == tarefa.id for item in tarefas_aluno)

    resposta = concluir_tarefa_service(tarefa.id, db_session)
    assert resposta["mensagem"].startswith("Tarefa concluída")

    with pytest.raises(TarefaNotFoundException):
        concluir_tarefa_service(9999, db_session)

    turma_vazia = setup_dados["outra_turma"]
    for aluno in list(turma_vazia.alunos):
        setup_dados["aluno_repo"].delete(aluno.id)
    db_session.commit()

    turma_vazia_db = setup_dados["turma_repo"].get_by_id(turma_vazia.id)
    assert len(turma_vazia_db.alunos) == 0

    with pytest.raises(AlunoNotFoundException):
        atribuir_tarefa_para_turma_service(turma_vazia.id, type("TarefaTurmaDTO", (), {"nome": "Tarefa Turma", "materia_id": materia.id}), db_session)

    with pytest.raises(MateriaNotFoundException):
        atribuir_tarefa_para_aluno_service(aluno2.id, type("TarefaAlunoDTO", (), {"nome": "Tarefa", "materia_id": 9999}), db_session)

    with pytest.raises(AlunoNotFoundException):
        atribuir_tarefa_para_aluno_service(9999, type("TarefaAlunoDTO", (), {"nome": "Tarefa", "materia_id": materia.id}), db_session)

    turma_tarefas = atribuir_tarefa_para_turma_service(turma.id, type("TarefaTurmaDTO", (), {"nome": "Tarefa Turma", "materia_id": materia.id}), db_session)
    assert len(turma_tarefas["tarefas"]) >= 2

    tarefas_aluno2 = listar_tarefas_do_aluno_service(aluno2.id, db_session)
    assert any(item["nome"] == "Tarefa Turma" for item in tarefas_aluno2)

    with pytest.raises(MateriaNotFoundException):
        atribuir_tarefa_para_turma_service(turma.id, type("TarefaTurmaDTO", (), {"nome": "Sem Matria", "materia_id": 9999}), db_session)

    with pytest.raises(TurmaNotFoundException):
        atribuir_tarefa_para_turma_service(9999, type("TarefaTurmaDTO", (), {"nome": "Sem Turma", "materia_id": materia.id}), db_session)

    with pytest.raises(AlunoNotFoundException):
        listar_tarefas_do_aluno_service(9999, db_session)
