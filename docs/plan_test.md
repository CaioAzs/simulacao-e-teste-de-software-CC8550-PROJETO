# PLANO DE TESTES - Sistema de Gerenciamento Acadêmico

## 1. INTRODUÇÃO

### 1.1 Objetivo
Este documento descreve a estratégia de testes aplicada ao sistema de gerenciamento acadêmico, que permite o controle de alunos, turmas, matérias e tarefas.

### 1.2 Escopo
O plano de testes cobre todas as camadas da aplicação: repositories, services, API REST e funcionalidades de negócio, utilizando diferentes técnicas e abordagens de teste.

### 1.3 Framework e Ferramentas
- **Framework de Testes**: pytest 8.4.2
- **Cobertura de Código**: pytest-cov (configurado para app/services)
- **Testes de Mutação**: mutmut (configurado para serviços críticos)
- **Cliente de Testes API**: FastAPI TestClient
- **Mocking**: unittest.mock
- **Banco de Dados**: SQLite em memória (testes isolados)

---

## 2. ESTRATÉGIA DE TESTES

### 2.1 Níveis de Teste Implementados

#### 2.1.1 Testes Unitários (Unit Tests)
**Localização**: `tests/unit/`

**Componentes Testados**:
- **Repositories** (`test_repositories.py`): 18 testes
  - AlunoRepository: 8 testes (CRUD completo + testes parametrizados)
  - TurmaRepository: 3 testes
  - MateriaRepository: 3 testes
  - TarefaRepository: 4 testes

- **Services** (`test_services.py`): 7 testes
  - TarefasService: 3 testes (criar, concluir, exceções)
  - MateriasService: 2 testes
  - TurmasService: 2 testes

- **AlunosService** (`test_alunos_service.py`): 5 testes
  - Criação com sucesso
  - Validação de turma inexistente
  - Busca por ID
  - Tratamento de exceções
  - Exclusão

**Técnicas Aplicadas**:
- Isolamento de componentes com fixtures
- Testes parametrizados para múltiplos cenários
- Validação de exceções customizadas
- Uso de mocks para objetos DTO

#### 2.1.2 Testes de Integração (Integration Tests)
**Localização**: `tests/integration/test_api.py`

**Cobertura**: 11 testes end-to-end

**Fluxos Testados**:
1. Criação e listagem de turmas
2. Fluxo completo de criação de aluno
3. Obtenção de aluno específico
4. Atualização de aluno
5. Exclusão de aluno
6. Criação de matéria
7. Atribuição de matéria para turma
8. Criação e conclusão de tarefa
9. Atribuição de tarefa para aluno
10. Atribuição de tarefa para turma inteira
11. Ranking de alunos com tarefas pendentes

**Características**:
- Testes de integração completa entre API, services e banco de dados
- Validação de relacionamentos entre entidades
- Testes de endpoints complexos (rankings, atribuições em lote)

#### 2.1.3 Testes Funcionais / Caixa-Preta (Functional Tests)
**Localização**: `tests/functional/test_student_enrollment.py`

**Casos de Teste**: 10 cenários de matrícula de alunos

**CT-01**: Matrícula com dados válidos (cenário de sucesso)
**CT-03**: Matrícula com turma inexistente (validação de erro)
**CT-04**: Atualização de dados do aluno (mudança de bolsista/idade)
**CT-05**: Consulta de aluno específico por ID
**CT-06**: Exclusão de aluno
**CT-07**: Listagem de todos os alunos
**CT-09**: Criação sem nome - DEFEITO IDENTIFICADO (aceita nome vazio)
**CT-10**: Busca de aluno inexistente

**Abordagem**:
- Testes sem conhecimento da implementação interna
- Foco em requisitos de negócio
- Validação de regras de validação
- Identificação de defeitos reais no sistema

#### 2.1.4 Testes Estruturais / Caixa-Branca (Structural Tests)
**Localização**: `tests/structural/test_services_structural.py`

**Objetivo**: Cobertura completa de branches e caminhos

**Testes Implementados**:
1. **test_crud_aluno_branches**: Cobertura de todos os caminhos do CRUD de alunos
   - Criação, listagem, obtenção, atualização, exclusão
   - Cenários de exceção (aluno não encontrado, turma inexistente)

2. **test_alunos_cenarios_coletivos**: Operações em lote e rankings
   - Criação em lote
   - Ranking de tarefas pendentes
   - Cenários com listas vazias

3. **test_turmas_branches**: Cobertura de operações de turmas
   - CRUD de turmas
   - Listagem de alunos da turma
   - Ranking de turmas com bolsistas
   - Cenários de turma vazia

4. **test_tarefas_branches**: Cobertura completa de tarefas
   - Criação, conclusão, atribuições
   - Exceções (tarefa/matéria/aluno não encontrado)
   - Atribuição para turma vazia

**Características**:
- Testes baseados em conhecimento do código
- Cobertura de todos os branches condicionais
- Validação de tratamento de exceções
- Testes de edge cases (listas vazias, IDs inexistentes)

#### 2.1.5 Testes com Mocks e Stubs
**Localização**: `tests/type/test_mocks.py`

**Testes Implementados**:
1. **test_criar_aluno_with_mock_repository**: Isolamento completo de dependências
   - Mock de TurmaRepository e AlunoRepository
   - Validação de chamadas aos métodos mockados
   - Testes sem acesso ao banco de dados

2. **test_criar_aluno_turma_inexistente_with_mock**: Simulação de cenários de erro
   - Mock retornando None (turma inexistente)
   - Validação de exceções lançadas
   - Verificação de que operações não executaram


#### 2.1.6 Testes de API REST
**Localização**: `tests/type/test_api_rest.py`

**Testes Implementados**:
1. **test_http_methods_on_alunos_endpoint**: Validação de métodos HTTP
   - POST (criação)
   - GET (consulta)
   - PUT (atualização)
   - DELETE (exclusão)

2. **test_status_codes_and_json_structure**: Validação de respostas
   - Status codes corretos (200, 500)
   - Estrutura JSON válida
   - Validação de campos obrigatórios no response

**Características**:
- Testes de conformidade com padrões REST
- Validação de contratos de API
- Testes de serialização/deserialização JSON

---

## 3. FIXTURES E CONFIGURAÇÃO

### 3.1 Fixtures Centralizadas (`tests/conftest.py`)

**Fixtures de Banco de Dados**:
- `db_session`: Sessão SQLite em memória isolada
- `client`: TestClient com banco de dados de teste
- `client_session`: Sessão vinculada ao cliente de teste

**Fixtures de Dados**:
- `turma_sample`: Turma pré-criada para testes
- `aluno_sample`: Aluno pré-criado vinculado a turma
- `materia_sample`: Matéria pré-criada
- `tarefa_sample`: Tarefa pré-criada vinculada a aluno e matéria

---

## 4. CONFIGURAÇÃO DE EXECUÇÃO

### 4.1 Pytest (`setup.cfg`)
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### 4.2 Cobertura de Código (`setup.cfg`)
```ini
[coverage:run]
source = app/services
omit = */tests/*, */test_*
```

### 4.3 Testes de Mutação (`setup.cfg`)
```ini
[mutmut]
paths_to_mutate = app/services/alunos_service.py,
                  app/services/turmas_service.py,
                  app/services/tarefas_service.py
runner = pytest
tests_dir = tests
```

---

## 5. MÉTRICAS E COBERTURA

### 5.1 Quantidade de Testes por Categoria
- **Testes Unitários**: 30 testes
  - Repositories: 18 testes
  - Services: 12 testes
- **Testes de Integração**: 11 testes
- **Testes Funcionais**: 10 testes (casos de teste documentados)
- **Testes Estruturais**: 4 testes (cobertura de branches)
- **Testes com Mocks**: 2 testes
- **Testes de API REST**: 2 testes

**Total**: ~59 testes automatizados

### 5.2 Áreas Cobertas
- ✅ Camada de Repositórios (CRUD completo)
- ✅ Camada de Serviços (lógica de negócio)
- ✅ Camada de API REST (endpoints)
- ✅ Tratamento de Exceções customizadas
- ✅ Validações de regras de negócio
- ✅ Relacionamentos entre entidades
- ✅ Operações em lote

---

## 7. ESTRATÉGIA DE EXECUÇÃO

### 7.1 Execução Local
```bash
# Todos os testes
pytest

# Com cobertura
pytest --cov=app/services --cov-report=html

# Categoria específica
pytest tests/unit/
pytest tests/integration/
pytest tests/functional/

# Testes de mutação
mutmut run
```

### 7.2 Critérios de Aceitação
- ✅ Todos os testes devem passar (0 falhas)
- ✅ Cobertura de código dos services: mínimo 80%
- ✅ Testes de mutação: mínimo 70% de mutantes mortos
- ✅ Sem regressões em testes existentes
