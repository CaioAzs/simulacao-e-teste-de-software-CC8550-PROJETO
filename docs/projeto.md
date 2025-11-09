# Sistema de Gest�o Escolar - Projeto de Testes

## Descri��o do Projeto

Sistema de gest�o escolar desenvolvido em Python com FastAPI para gerenciar alunos, turmas, mat�rias e tarefas. O projeto implementa uma API REST completa com opera��es CRUD e utiliza SQLite como banco de dados.

## Tecnologias Utilizadas

- **Python 3.13**
- **FastAPI** - Framework web para cria��o da API REST
- **SQLAlchemy** - ORM para manipula��o do banco de dados
- **SQLite** - Banco de dados relacional
- **Pytest** - Framework de testes
- **Pydantic** - Valida��o de dados

## Arquitetura

O projeto segue uma arquitetura em camadas:
- **Routers** - Endpoints da API REST
- **Services** - L�gica de neg�cio
- **Repositories** - Acesso aos dados
- **Models** - Entidades do banco de dados
- **Exceptions** - Tratamento de erros customizados

## Funcionalidades

- Gerenciamento de Alunos (CRUD completo)
- Gerenciamento de Turmas
- Gerenciamento de Mat�rias
- Gerenciamento de Tarefas
- Cria��o em lote de alunos
- Consulta de alunos com mais tarefas pendentes

## Estrutura de Testes

O projeto implementa diferentes tipos de testes:

1. **Testes Unit�rios** (`tests/unit/`) - 31 testes unit�rios cobrindo reposit�rios e servi�os
2. **Testes Funcionais** (`tests/functional/`) - 8 testes caixa-preta validando regras de neg�cio
3. **Testes Espec�ficos** (`tests/type/`) - 2 testes de API REST e 2 testes com Mocks

## Cobertura de Testes

- **Total: 59 testes implementados**
- **Testes Unitários**: 30 testes
  - Repositories: 18 testes
  - Services: 12 testes
- **Testes de Integração**: 11 testes
- **Testes Funcionais**: 10 testes (casos de teste documentados)
- **Testes Estruturais**: 4 testes (cobertura de branches)
- **Testes com Mocks**: 2 testes
- **Testes de API REST**: 2 testes


