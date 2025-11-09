# Sistema de Gestão Escolar - Projeto de Testes

## Descrição do Projeto

Sistema de gestão escolar desenvolvido em Python com FastAPI para gerenciar alunos, turmas, matérias e tarefas. O projeto implementa uma API REST completa com operações CRUD e utiliza SQLite como banco de dados.

## Tecnologias Utilizadas

- **Python 3.13**
- **FastAPI** - Framework web para criação da API REST
- **SQLAlchemy** - ORM para manipulação do banco de dados
- **SQLite** - Banco de dados relacional
- **Pytest** - Framework de testes
- **Pydantic** - Validação de dados

## Arquitetura

O projeto segue uma arquitetura em camadas:
- **Routers** - Endpoints da API REST
- **Services** - Lógica de negócio
- **Repositories** - Acesso aos dados
- **Models** - Entidades do banco de dados
- **Exceptions** - Tratamento de erros customizados

## Funcionalidades

- Gerenciamento de Alunos (CRUD completo)
- Gerenciamento de Turmas
- Gerenciamento de Matérias
- Gerenciamento de Tarefas
- Criação em lote de alunos
- Consulta de alunos com mais tarefas pendentes

## Estrutura de Testes

O projeto implementa diferentes tipos de testes:

1. **Testes Unitários** (`tests/unit/`) - 31 testes unitários cobrindo repositórios e serviços
2. **Testes Funcionais** (`tests/functional/`) - 8 testes caixa-preta validando regras de negócio
3. **Testes Específicos** (`tests/type/`) - 2 testes de API REST e 2 testes com Mocks

## Cobertura de Testes

- **Total: 43 testes implementados**
  - 31 testes unitários
  - 8 testes funcionais (caixa-preta)
  - 2 testes de API REST
  - 2 testes com Mocks
