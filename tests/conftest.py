"""
Arquivo conftest.py raiz com todas as fixtures centralizadas.
"""
import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.models import Aluno, Turma, Materia, Tarefa
from app.main import app

# Adiciona o diretório raiz ao path para imports funcionarem corretamente
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))


@pytest.fixture
def db_session():
    """Fixture que cria uma sessão de banco de dados em memória para testes"""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


@pytest.fixture
def turma_sample(db_session):
    """Fixture que cria uma turma de exemplo"""
    turma = Turma(nome="Turma A")
    db_session.add(turma)
    db_session.commit()
    db_session.refresh(turma)
    return turma


@pytest.fixture
def aluno_sample(db_session, turma_sample):
    """Fixture que cria um aluno de exemplo"""
    aluno = Aluno(
        nome="João Silva",
        idade=20,
        bolsista=True,
        turma_id=turma_sample.id
    )
    db_session.add(aluno)
    db_session.commit()
    db_session.refresh(aluno)
    return aluno


@pytest.fixture
def materia_sample(db_session):
    """Fixture que cria uma matéria de exemplo"""
    materia = Materia(nome="Matemática")
    db_session.add(materia)
    db_session.commit()
    db_session.refresh(materia)
    return materia


@pytest.fixture
def tarefa_sample(db_session, aluno_sample, materia_sample):
    """Fixture que cria uma tarefa de exemplo"""
    tarefa = Tarefa(
        nome="Exercício 1",
        materia_id=materia_sample.id,
        aluno_id=aluno_sample.id,
        concluido=False
    )
    db_session.add(tarefa)
    db_session.commit()
    db_session.refresh(tarefa)
    return tarefa


@pytest.fixture
def client():
    """Fixture que cria um cliente de teste com banco de dados em memória"""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    app.state._session_factory = TestingSessionLocal
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.pop(get_db, None)
        app.state.__dict__.pop("_session_factory", None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture
def client_session(client):
    """Fixture que cria uma sessão de banco de dados do cliente de teste"""
    Session = client.app.state._session_factory
    session = Session()
    try:
        yield session
    finally:
        session.close()
