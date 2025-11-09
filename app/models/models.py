from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

# Tabela associativa aluno-materia
aluno_materia = Table(
    "aluno_materia",
    Base.metadata,
    Column("aluno_id", Integer, ForeignKey("alunos.id")),
    Column("materia_id", Integer, ForeignKey("materias.id"))
)

class Turma(Base):
    __tablename__ = "turmas"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    alunos = relationship("Aluno", back_populates="turma")

class Materia(Base):
    __tablename__ = "materias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    alunos = relationship("Aluno", secondary=aluno_materia, back_populates="materias")

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    idade = Column(Integer)
    bolsista = Column(Boolean, default=False)  # Novo atributo
    turma_id = Column(Integer, ForeignKey("turmas.id"))
    turma = relationship("Turma", back_populates="alunos")
    materias = relationship("Materia", secondary=aluno_materia, back_populates="alunos")



class Tarefa(Base):
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    concluido = Column(Boolean, default=False)
    materia_id = Column(Integer, ForeignKey("materias.id"))
    aluno_id = Column(Integer, ForeignKey("alunos.id"))

    materia = relationship("Materia")
    aluno = relationship("Aluno", back_populates="tarefas")

Aluno.tarefas = relationship("Tarefa", back_populates="aluno")
