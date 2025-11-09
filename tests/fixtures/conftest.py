import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.models import Aluno, Turma, Materia, Tarefa


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
