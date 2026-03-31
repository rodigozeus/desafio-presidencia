# Plataforma de Gestão de Pedidos — PMV

> Desafio prático — Presidência da República (Edital 173/2026)

## Visão Geral

Plataforma interna de gestão de pedidos para e-commerce, construída com arquitetura de **microsserviços** no backend e **microfrontends** no frontend.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         FRONTEND (porta 3000)                    │
│                      MFE Shell / Host (React)                    │
│                 Login │ Navegação │ AuthContext                  │
│                         ↕ Module Federation                      │
│              MFE Orders (porta 3001, remoteEntry.js)            │
│           OrdersList │ OrderCreate │ OrderDetail                 │
└──────────────────┬──────────────────┬───────────────────────────┘
                   │                  │
        ┌──────────▼──────┐  ┌────────▼────────┐
        │  Users Service  │  │  Orders Service  │
        │   (porta 8001)  │  │   (porta 8002)   │
        │    FastAPI      │  │    FastAPI       │
        │  JWT Issuer     │  │  JWT Validator   │
        │  POST /users    │  │  GET /orders     │
        │  POST /auth/    │  │  POST /orders    │
        │  GET /users     │  │  PATCH /{id}/    │
        └──────┬──────────┘  └────┬──────┬─────┘
               │                  │      │
        ┌──────▼──────┐   ┌───────▼─┐  ┌▼──────────┐
        │  PostgreSQL  │   │PostgreSQL│  │   Redis    │
        │  users_db    │   │orders_db │  │  (cache)   │
        └─────────────┘   └──────────┘  └────────────┘
```

**Fluxo de autenticação:**
1. Frontend faz login no Users Service → recebe JWT
2. JWT é armazenado no localStorage e enviado como `Authorization: Bearer`
3. Orders Service valida o JWT com a mesma chave secreta (shared secret)
4. Não há chamada inter-serviço para validar tokens — cada serviço valida localmente

## Tecnologias Escolhidas

### FastAPI (não Django REST Framework)
- Async-native, sem overhead de Django ORM para um PMV
- Geração automática de Swagger/OpenAPI (item bônus incluso gratuitamente)
- Pydantic para validação e serialização com type hints
- Menos boilerplate: um `main.py` vs configuração completa de settings/urls/apps

### Webpack Module Federation
- MFE de pedidos é um bundle **separado**, carregado em runtime pelo Shell
- Cada MFE pode ser deployado independentemente sem rebuild do Shell
- Compartilhamento de `react` e `react-router-dom` como singletons — sem conflitos
- Alternativa considerada (e rejeitada para este PMV): iframes — isolamento total mas UX ruim

### Redis como cache
- Cache de listagem de pedidos (TTL de 60s) — reduz load no banco em leituras repetidas
- Invalidado automaticamente ao criar/atualizar pedido
- Falha graciosamente: se Redis estiver down, a API continua funcionando sem cache

### JWT com shared secret
- Alternativa mais simples para PMV: um único `JWT_SECRET` compartilhado via env var
- Alternativa não tomada: JWKS endpoint no Users Service para verificação criptográfica — mais robusto mas adiciona latência e complexidade

### Integração com IA (Claude API — Bônus)
- Ao criar um pedido, o Orders Service chama `claude-haiku-4-5` para sugerir prioridade e gerar um resumo
- Funciona opcionalmente: se `ANTHROPIC_API_KEY` não estiver configurada, usa prioridade `medium` e sem resumo
- Modelo Haiku escolhido por latência e custo — adequado para classificação simples

## Como Executar

### Pré-requisitos
- Docker e Docker Compose instalados

### 1. Clone e configure
```bash
git clone <repo>
cd desafio_presidencia
cp .env.example .env
# Opcionalmente: adicione ANTHROPIC_API_KEY para habilitar IA
```

### 2. Suba a stack
```bash
docker-compose up --build
```

Aguarde todos os serviços iniciarem (~2 minutos no primeiro build).

### 3. Crie usuários e dados de demonstração
```bash
pip install httpx
python scripts/seed.py
```

### 4. Acesse a aplicação

| Serviço | URL |
|---------|-----|
| Frontend (Shell) | http://localhost:3000 |
| MFE Orders | http://localhost:3001 |
| Users Service API | http://localhost:8001/docs |
| Orders Service API | http://localhost:8002/docs |

**Login demo:** `admin@demo.com` / `admin123`

## Endpoints da API

### Users Service (porta 8001)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/auth/login` | Login — retorna JWT |
| POST | `/users/` | Criar usuário |
| GET | `/users/` | Listar usuários |
| GET | `/users/{id}` | Buscar usuário por ID |
| GET | `/health` | Health check |

### Orders Service (porta 8002)
| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/orders/` | Listar pedidos (filtro `?status=`) |
| POST | `/orders/` | Criar pedido (IA sugere prioridade) |
| GET | `/orders/{id}` | Buscar pedido por ID |
| PATCH | `/orders/{id}/status` | Atualizar status (JWT obrigatório) |
| GET | `/health` | Health check |

## Testes

```bash
# Users Service
cd services/users
pip install -r requirements.txt
pytest tests/ -v

# Orders Service
cd services/orders
pip install -r requirements.txt
pytest tests/ -v
```

## CI Pipeline

GitHub Actions configurado em `.github/workflows/`:
- `ci-users.yml` — roda testes do Users Service a cada push em `services/users/`
- `ci-orders.yml` — roda testes do Orders Service a cada push em `services/orders/`
- `ci-frontend.yml` — valida build dos MFEs a cada push em `frontend/`

## Demonstração de Resiliência

Para demonstrar que os serviços são independentes:

```bash
# Derrube o Users Service — Orders ainda funciona para leitura
docker-compose stop users-service

# Pedidos continuam sendo listados (e criados sem autenticação)
# Apenas PATCH /status ficará retornando 401 (sem JWT válido)

# Suba novamente
docker-compose start users-service
```

## O Que Ficaria Diferente com Mais Tempo

### Prioridade Alta
1. **API Gateway** (Nginx ou Kong): roteamento centralizado, rate limiting, SSL termination — atualmente o frontend faz chamadas diretas para cada serviço
2. **Refresh token**: o JWT atual expira em 24h mas não há mecanismo de refresh sem re-login
3. **RBAC real**: atualmente qualquer usuário autenticado pode fazer PATCH no status; faltam regras de papéis
4. **Testes de integração**: os testes atuais usam SQLite em memória; idealmente subiriam um PostgreSQL de teste via `pytest-docker`

### Prioridade Média
5. **Comunicação assíncrona**: ao criar um pedido, publicar evento em Redis Pub/Sub ou RabbitMQ — permitiria notificações, auditoria e integração com outros serviços sem acoplamento
6. **MFE Catálogo**: terceiro microfrontend para gerenciar o catálogo de produtos, que hoje são strings livres no formulário
7. **Paginação no frontend**: a listagem não tem paginação — em produção com milhares de pedidos isso seria crítico
8. **Observabilidade real**: estrutura de logs está pronta, mas falta integração com Prometheus/Grafana ou Datadog

### Decisões Não Tomadas (e Por Quê)
- **MongoDB**: optei por Redis como complemento ao PostgreSQL — mais simples de justificar operacionalmente para um PMV, e já resolve o caso de cache. MongoDB faria sentido se os pedidos tivessem schema muito variável, o que não é o caso aqui.
- **JWKS / validação remota de token**: mais seguro (permite revogação imediata de tokens), mas adiciona latência na validação de cada request. Para o PMV, shared secret é suficiente.
- **Autenticação no MFE**: o token é gerenciado pelo Shell e não é diretamente acessível pelo MFE via Module Federation — é lido do localStorage. Melhor abordagem seria um AuthContext compartilhado via Module Federation ou um BFF.
- **SSR / Next.js**: considerado para o Shell, rejeitado — Module Federation com SSR adiciona complexidade significativa e não é necessário para uma ferramenta interna.

## Estrutura do Projeto

```
desafio_presidencia/
├── services/
│   ├── users/                  # Microsserviço de usuários + JWT
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py       # SQLAlchemy User model
│   │   │   ├── schemas.py      # Pydantic schemas
│   │   │   ├── auth.py         # bcrypt + JWT issuer
│   │   │   ├── config.py       # Settings via pydantic-settings
│   │   │   ├── database.py     # SQLAlchemy engine
│   │   │   └── routes/
│   │   │       ├── auth.py     # POST /auth/login
│   │   │       └── users.py    # CRUD /users
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── orders/                 # Microsserviço de pedidos
│       ├── app/
│       │   ├── main.py
│       │   ├── models.py       # SQLAlchemy Order model
│       │   ├── schemas.py
│       │   ├── auth.py         # JWT validator (shared secret)
│       │   ├── ai_service.py   # Claude API integration
│       │   ├── redis_client.py # Cache layer
│       │   ├── config.py
│       │   ├── database.py
│       │   └── routes/
│       │       └── orders.py   # CRUD + status update
│       ├── tests/
│       ├── Dockerfile
│       └── requirements.txt
├── frontend/
│   ├── shell/                  # MFE Host (Webpack Module Federation)
│   │   ├── src/
│   │   │   ├── App.jsx         # Routing + lazy MFE loading
│   │   │   ├── context/        # AuthContext (JWT state)
│   │   │   └── components/     # Navigation, Login
│   │   ├── webpack.config.js   # Module Federation host config
│   │   └── Dockerfile
│   └── mfe-orders/             # MFE Remote (expõe OrdersApp)
│       ├── src/
│       │   ├── OrdersApp.jsx   # Routes: list, create, detail
│       │   ├── api.js          # Fetch wrapper com auth headers
│       │   └── components/     # OrdersList, OrderCreate, OrderDetail
│       ├── webpack.config.js   # Module Federation remote config
│       └── Dockerfile
├── scripts/
│   └── seed.py                 # Cria usuários demo + pedidos de exemplo
├── .github/
│   └── workflows/              # CI para cada serviço
├── docker-compose.yml
├── .env.example
└── README.md
```
