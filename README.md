# 🎓 API SOAP de Notas

API SOAP em Python para gerenciamento acadêmico de alunos e notas

## Arquitetura

```
Client (Zeep / Postman)
        │
        ▼ SOAP Request
┌─────────────────────────────────┐
│  Spyne Application (WSGI)       │
│  ┌───────────────────────────┐  │
│  │  method_call event        │  │
│  │  ├── Rate Limit           │  │
│  │  ├── Auth (WS-Security)   │  │
│  │  └── RBAC                 │  │
│  └───────────────────────────┘  │
│  ┌───────────────────────────┐  │
│  │  AlunoService (6 ops)     │  │
│  │  └── AlunoRepository      │  │
│  │      └── Business Logic   │  │
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

## Estrutura de Diretórios

```
API-SOAP-de-Notas/
├── main.py                 # Ponto de entrada (python main.py)
├── server.py               # Configuração da app Spyne + segurança + seed
├── client.py               # Cliente CLI demonstrativo
├── compat.py               # Patches de compatibilidade Spyne ↔ Python 3.13
├── requirements.txt        # Dependências do projeto
│
├── models/
│   └── aluno.py            # AlunoModel (Spyne ComplexModel)
│
├── services/
│   ├── aluno_service.py    # AlunoRepository + AlunoService (6 operações)
│   └── business_logic.py   # Cálculo de média, situação e validação
│
├── security/
│   ├── auth.py             # WS-Security UsernameToken + hash SHA-256
│   ├── roles.py            # RBAC (ADM / USER)
│   └── rate_limit.py       # Rate limit por IP (100 req/min)
│
└── tests/
    ├── conftest.py          # Fixtures (servidor dinâmico + cleanup)
    ├── test_unit.py         # Testes unitários de business_logic
    ├── test_integration.py  # CRUD completo + auth + RBAC via Zeep
    ├── test_contract.py     # Validação do WSDL (operações + tipos)
    └── test_e2e.py          # Fluxo acadêmico completo + rate limit
```

## Tecnologias

| Tecnologia | Finalidade |
|---|---|
| **Python 3.9+** | Linguagem |
| **[Spyne](http://spyne.io/)** | Framework SOAP/WSDL |
| **[Zeep](https://docs.python-zeep.org/)** | Cliente SOAP (testes e CLI) |
| **pytest + pytest-cov** | Testes e cobertura de código |
| **wsgiref** | Servidor WSGI embutido |

## Instalação

```bash
git clone https://github.com/ean22/API-SOAP-de-Notas.git
cd API-SOAP-de-Notas

python -m .venv venv
.venv\Scripts\activate      # Windows (PowerShell)
# source venv/bin/activate   # Linux/Mac

pip install -r requirements.txt
```

## Como Usar

### Servidor

```bash
python main.py
```

O servidor inicia na porta 8000:
- **WSDL:** http://127.0.0.1:8000/?wsdl

### Cliente CLI

Com o servidor rodando, em outro terminal:

```bash
python client.py
```

O cliente demonstra todas as operações: listar, cadastrar (ADM), consultar, atualizar (ADM), remover (ADM), média da turma, e cenários de erro (RBAC, sem autenticação).

## Segurança

A API usa **WS-Security (UsernameToken)** para autenticação e **RBAC** para controle de acesso.

| Usuário | Senha | Papel | Permissões |
|---|---|---|---|
| `admin` | `admin123` | ADM | Acesso total (CRUD) |
| `user` | `user123` | USER | Somente leitura |

Senhas armazenadas com hash SHA-256. Rate limiting simples de 100 req/min por IP.

## Operações SOAP

| Operação | Acesso | Descrição |
|---|---|---|
| `consultar_aluno(ra)` | Público | Retorna dados de um aluno |
| `listar_alunos()` | Público | Lista todos os alunos |
| `cadastrar_aluno(nome, nota1, nota2)` | ADM | Cadastra novo aluno |
| `atualizar_notas(ra, nota1, nota2)` | ADM | Atualiza notas |
| `remover_aluno(ra)` | ADM | Remove aluno |
| `calcular_media_turma()` | Público | Média geral da turma |

**Regras de negócio:**
- Média ponderada: `nota1 × 0.4 + nota2 × 0.6`
- Aprovado: média ≥ 7.0 | Recuperação: média ≥ 5.0 | Reprovado: média < 5.0
- Notas válidas: 0.0 a 10.0

## Testes

```bash
# Todos os testes
pytest tests -v

# Com cobertura de código
pytest tests -v --cov=services --cov=security --cov=models --cov-report=term-missing
```

Cobertura atual: **100%** (23 testes: unitários, integração, contrato WSDL, e2e e validações de borda).