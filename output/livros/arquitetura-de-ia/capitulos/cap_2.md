## 2. Persistência e API: Memória do Assistente

### 2.1 Introdução

No capítulo anterior, construímos um chat funcional que mantém histórico em memória. O problema? Quando você fecha o terminal, todo o histórico se perde. Neste capítulo, vamos resolver dois problemas fundamentais:

1. **Persistência:** Salvar conversas em um banco de dados para que nunca se percam
2. **API REST:** Expor nosso chat como uma API que outros aplicativos podem usar

**O que você vai adicionar ao projeto:**
- FastAPI para criar endpoints REST
- PostgreSQL para persistir conversas
- ORM (SQLAlchemy) para interagir com o banco
- Migrações de banco de dados
- Testes automatizados

**Por que isso importa:**
Todo sistema de IA em produção precisa de persistência (para analytics, fallback, auditoria) e de uma API (para integração com frontends, mobile, outros serviços). Estes são os primeiros componentes de infraestrutura real do nosso assistente.

### 2.2 Explica

#### Arquitetura de APIs REST

REST (Representational State Transfer) é um padrão arquitetural para APIs web [1]. Em vez de criar endpoints customizados para cada operação, REST usa os verbos HTTP padrão:

| Verbo HTTP | Operação | Exemplo |
|------------|----------|---------|
| `GET` | Ler dados | `GET /conversas/123` — buscar conversa |
| `POST` | Criar dados | `POST /conversas` — criar nova conversa |
| `PUT` | Atualizar dados | `PUT /conversas/123` — atualizar conversa |
| `DELETE` | Deletar dados | `DELETE /conversas/123` — remover conversa |

**Por que REST e não GraphQL ou gRPC?**
- REST é o padrão maisado e bem documentado
- Maioria dos clientes (web, mobile) já sabe consumir REST
- Ferramentas como FastAPI geram documentação automática (Swagger)
- Para este estágio do projeto, REST é suficiente e simples

#### Modelagem de Dados para IA

Um sistema de IA conversacional precisa armazenar [2]:

1. **Conversas:** Uma sessão de chat (pode ter várias mensagens)
2. **Mensagens:** Cada interação (usuário ou assistente)
3. **Metadados:** Timestamps, tokens usados, modelo, latência

**Schema do banco de dados:**

```sql
-- Tabela de conversas
CREATE TABLE conversas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    titulo VARCHAR(255) NOT NULL,
    criado_em TIMESTAMP DEFAULT NOW(),
    atualizado_em TIMESTAMP DEFAULT NOW(),
    modelo VARCHAR(50) NOT NULL,
    metadata JSONB DEFAULT '{}'
);

-- Tabela de mensagens
CREATE TABLE mensagens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversa_id UUID REFERENCES conversas(id) ON DELETE CASCADE,
    papel VARCHAR(20) NOT NULL CHECK (papel IN ('user', 'assistant', 'system')),
    conteudo TEXT NOT NULL,
    tokens_entrada INTEGER,
    tokens_saida INTEGER,
    latencia_ms FLOAT,
    criado_em TIMESTAMP DEFAULT NOW()
);
```

**Por que UUID em vez de integer?**
- UUIDs são únicos globalmente (sem conflito entre bancos)
- Não expõem a contagem de registros (segurança)
- Funcionam bem em sistemas distribuídos (futuro)

#### ORM com SQLAlchemy

SQLAlchemy é o ORM (Object-Relational Mapping) mais usado no Python [3]. Ele permite interagir com o banco de dados usando objetos Python em vez de SQL raw:

```python
# Em vez de SQL raw:
# INSERT INTO mensagens (conversa_id, papel, conteudo) VALUES ('uuid', 'user', 'Olá')

# Com SQLAlchemy:
mensagem = Mensagem(conversa_id=uuid, papel="user", conteudo="Olá")
session.add(mensagem)
session.commit()
```

**Vantagens do ORM:**
- Proteção contra SQL injection
- Migrações automáticas (Alembic)
- Tipagem e autocompletar no editor
- Facilidade de testes (pode trocar o banco)

#### FastAPI: APIs Modernas no Python

FastAPI é um framework web moderno para Python que usa type hints para gerar documentação automática [4]. Ele é ideal para APIs de IA porque:

- **Alta performance:** Async/await nativo, tão rápido quanto Node.js
- **Documentação automática:** Swagger UI gerada a partir dos type hints
- **Validação automática:** Pydantic valida os dados de entrada
- **Fácil de aprender:** Sintaxe simples e intuitiva

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class MensagemRequest(BaseModel):
    conteudo: str

@app.post("/conversas/{conversa_id}/mensagens")
async def criar_mensagem(conversa_id: str, request: MensagemRequest):
    # FastAPI valida automaticamente que conteudo é string
    # e retorna 422 se faltar
    return {"mensagem": "Criada com sucesso"}
```

### 2.3 Ilustra

#### Atualização do requirements.txt

```txt
# requirements.txt (atualizado)
openai>=1.0.0
python-dotenv>=1.0.0
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
sqlalchemy>=2.0.0
alembic>=1.12.0
psycopg2-binary>=2.9.0
pydantic>=2.0.0
httpx>=0.25.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

#### Modelos de Banco de Dados

```python
# src/database/models.py
"""
Modelos de banco de dados para persistência de conversas.
"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class Conversa(Base):
    """Uma sessão de chat com uma ou mais mensagens."""
    __tablename__ = "conversas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    titulo = Column(String(255), nullable=False, default="Nova Conversa")
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    modelo = Column(String(50), nullable=False, default="deepseek-v4-flash")
    metadata_ = Column("metadata", JSON, default=dict)
    
    # Relacionamento
    mensagens = relationship("Mensagem", back_populates="conversa", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Conversa(id={self.id}, titulo='{self.titulo}')>"

class Mensagem(Base):
    """Uma mensagem individual em uma conversa."""
    __tablename__ = "mensagens"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversa_id = Column(UUID(as_uuid=True), ForeignKey("conversas.id"), nullable=False)
    papel = Column(String(20), nullable=False)  # 'user', 'assistant', 'system'
    conteudo = Column(Text, nullable=False)
    tokens_entrada = Column(Integer)
    tokens_saida = Column(Integer)
    latencia_ms = Column(Float)
    criado_em = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento
    conversa = relationship("Conversa", back_populates="mensagens")
    
    def __repr__(self):
        return f"<Mensagem(id={self.id}, papel='{self.papel}')>"
```

#### Conexão com o Banco

```python
# src/database/connection.py
"""
Gerenciamento de conexão com o banco de dados.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from src.database.models import Base
from config.settings import load_config

class Database:
    """Gerencia a conexão e sessões do banco de dados."""
    
    def __init__(self, database_url: str = None):
        config = load_config()
        self.database_url = database_url or config.database.url
        
        self.engine = create_engine(
            self.database_url,
            echo=config.debug,
            pool_pre_ping=True,  # Verifica conexões mortas
        )
        
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def criar_tabelas(self):
        """Cria todas as tabelas definidas nos modelos."""
        Base.metadata.create_all(self.engine)
    
    def get_session(self) -> Session:
        """Retorna uma nova sessão do banco."""
        return self.SessionLocal()
    
    def dependency(self):
        """Dependency para FastAPI (injeção de dependência)."""
        session = self.get_session()
        try:
            yield session
        finally:
            session.close()
```

#### Repositório de Dados

```python
# src/database/repository.py
"""
Repositório para operações de CRUD no banco de dados.
Separa a lógica de negócio da lógica de acesso a dados.
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from src.database.models import Conversa, Mensagem

class ConversaRepository:
    """Operações CRUD para conversas."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def criar(self, titulo: str, modelo: str) -> Conversa:
        """Cria uma nova conversa."""
        conversa = Conversa(titulo=titulo, modelo=modelo)
        self.session.add(conversa)
        self.session.commit()
        self.session.refresh(conversa)
        return conversa
    
    def buscar_por_id(self, conversa_id: UUID) -> Optional[Conversa]:
        """Busca uma conversa por ID."""
        return self.session.query(Conversa).filter(Conversa.id == conversa_id).first()
    
    def listar(self, limite: int = 50) -> List[Conversa]:
        """Lista conversas ordenadas por data de criação."""
        return self.session.query(Conversa)\
            .order_by(Conversa.criado_em.desc())\
            .limit(limite)\
            .all()
    
    def atualizar(self, conversa_id: UUID, **kwargs) -> Optional[Conversa]:
        """Atualiza campos de uma conversa."""
        conversa = self.buscar_por_id(conversa_id)
        if conversa:
            for key, value in kwargs.items():
                setattr(conversa, key, value)
            self.session.commit()
            self.session.refresh(conversa)
        return conversa
    
    def deletar(self, conversa_id: UUID) -> bool:
        """Deleta uma conversa e todas as suas mensagens."""
        conversa = self.buscar_por_id(conversa_id)
        if conversa:
            self.session.delete(conversa)
            self.session.commit()
            return True
        return False

class MensagemRepository:
    """Operações CRUD para mensagens."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def criar(self, conversa_id: UUID, papel: str, conteudo: str,
              tokens_entrada: int = None, tokens_saida: int = None,
              latencia_ms: float = None) -> Mensagem:
        """Cria uma nova mensagem."""
        mensagem = Mensagem(
            conversa_id=conversa_id,
            papel=papel,
            conteudo=conteudo,
            tokens_entrada=tokens_entrada,
            tokens_saida=tokens_saida,
            latencia_ms=latencia_ms,
        )
        self.session.add(mensagem)
        self.session.commit()
        self.session.refresh(mensagem)
        return mensagem
    
    def listar_por_conversa(self, conversa_id: UUID) -> List[Mensagem]:
        """Lista todas as mensagens de uma conversa."""
        return self.session.query(Mensagem)\
            .filter(Mensagem.conversa_id == conversa_id)\
            .order_by(Mensagem.criado_em)\
            .all()
```

#### Client da API (Atualizado)

```python
# src/client.py (atualizado com métricas)
"""
Cliente da API de IA com métricas de performance.
"""
import os
import time
import logging
from typing import List, Dict, Optional, Tuple
from openai import OpenAI, RateLimitError, APIError

logger = logging.getLogger(__name__)

class IAClient:
    """Cliente para a API de IA com tratamento de erros e métricas."""
    
    def __init__(self, api_key: str, base_url: str, model: str,
                 temperature: float = 0.7, max_tokens: int = 1000):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
    
    def enviar(self, mensagens: List[Dict[str, str]], 
               temperature: Optional[float] = None,
               max_tokens: Optional[int] = None) -> Tuple[str, Dict]:
        """
        Envia mensagens e retorna resposta com métricas.
        
        Returns:
            Tupla (resposta_texto, metricas)
        """
        metricas = {}
        max_retries = 3
        retry_delay = 1.0
        
        for attempt in range(max_retries):
            try:
                start_time = time.time()
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=mensagens,
                    temperature=temperature or self.temperature,
                    max_tokens=max_tokens or self.max_tokens,
                )
                
                elapsed_ms = (time.time() - start_time) * 1000
                
                resposta = response.choices[0].message.content
                
                # Extrair métricas
                metricas = {
                    "tokens_entrada": response.usage.prompt_tokens if response.usage else 0,
                    "tokens_saida": response.usage.completion_tokens if response.usage else 0,
                    "latencia_ms": elapsed_ms,
                    "modelo": response.model,
                }
                
                logger.info(f"Resposta: {len(resposta)} chars, {elapsed_ms:.0f}ms")
                return resposta, metricas
                
            except RateLimitError as e:
                logger.warning(f"Rate limit (tentativa {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay * (2 ** attempt))
                else:
                    raise Exception(f"Rate limit após {max_retries} tentativas")
                    
            except APIError as e:
                logger.error(f"Erro na API: {e}")
                raise Exception(f"Erro na API: {e}")
```

#### API REST com FastAPI

```python
# src/api/routes.py
"""
Endpoints REST da API do assistente de IA.
"""
from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from src.database.connection import Database
from src.database.repository import ConversaRepository, MensagemRepository
from src.client import IAClient
from config.settings import load_config

router = APIRouter()
config = load_config()

# Schemas Pydantic (validação automática)
class ConversaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=255)

class MensagemCreate(BaseModel):
    conteudo: str = Field(..., min_length=1, max_length=10000)

class MensagemResponse(BaseModel):
    id: UUID
    papel: str
    conteudo: str
    tokens_entrada: Optional[int]
    tokens_saida: Optional[int]
    latencia_ms: Optional[float]
    criado_em: str

class ConversaResponse(BaseModel):
    id: UUID
    titulo: str
    modelo: str
    criado_em: str
    atualizado_em: str
    total_mensagens: int

class ChatResponse(BaseModel):
    resposta: str
    metricas: dict

# Database dependency
db = Database()

def get_session():
    return db.dependency()

# Endpoints
@router.post("/conversas", response_model=ConversaResponse)
def criar_conversa(request: ConversaCreate, session: Session = Depends(get_session)):
    """Cria uma nova conversa."""
    repo = ConversaRepository(session)
    conversa = repo.criar(titulo=request.titulo, modelo=config.ia.model)
    return ConversaResponse(
        id=conversa.id,
        titulo=conversa.titulo,
        modelo=conversa.modelo,
        criado_em=str(conversa.criado_em),
        atualizado_em=str(conversa.atualizado_em),
        total_mensagens=0,
    )

@router.get("/conversas", response_model=List[ConversaResponse])
def listar_conversas(limite: int = 50, session: Session = Depends(get_session)):
    """Lista todas as conversas."""
    repo = ConversaRepository(session)
    conversas = repo.listar(limite=limite)
    return [
        ConversaResponse(
            id=c.id, titulo=c.titulo, modelo=c.modelo,
            criado_em=str(c.criado_em), atualizado_em=str(c.atualizado_em),
            total_mensagens=len(c.mensagens),
        )
        for c in conversas
    ]

@router.get("/conversas/{conversa_id}", response_model=ConversaResponse)
def buscar_conversa(conversa_id: UUID, session: Session = Depends(get_session)):
    """Busca uma conversa por ID."""
    repo = ConversaRepository(session)
    conversa = repo.buscar_por_id(conversa_id)
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return ConversaResponse(
        id=conversa.id, titulo=conversa.titulo, modelo=conversa.modelo,
        criado_em=str(conversa.criado_em), atualizado_em=str(conversa.atualizado_em),
        total_mensagens=len(conversa.mensagens),
    )

@router.post("/conversas/{conversa_id}/chat", response_model=ChatResponse)
def enviar_mensagem(conversa_id: UUID, request: MensagemCreate, 
                    session: Session = Depends(get_session)):
    """Envia uma mensagem e retorna a resposta do assistente."""
    # Buscar conversa
    conv_repo = ConversaRepository(session)
    conversa = conv_repo.buscar_por_id(conversa_id)
    if not conversa:
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    
    # Salvar mensagem do usuário
    msg_repo = MensagemRepository(session)
    msg_repo.criar(
        conversa_id=conversa_id,
        papel="user",
        conteudo=request.conteudo,
    )
    
    # Buscar histórico
    historico = msg_repo.listar_por_conversa(conversa_id)
    mensagens_api = [{"role": m.papel, "content": m.conteudo} for m in historico]
    
    # Chamar IA
    client = IAClient(
        api_key=config.ia.api_key,
        base_url=config.ia.base_url,
        model=config.ia.model,
    )
    resposta, metricas = client.enviar(mensagens_api)
    
    # Salvar resposta do assistente
    msg_repo.criar(
        conversa_id=conversa_id,
        papel="assistant",
        conteudo=resposta,
        tokens_entrada=metricas.get("tokens_entrada"),
        tokens_saida=metricas.get("tokens_saida"),
        latencia_ms=metricas.get("latencia_ms"),
    )
    
    # Atualizar timestamp da conversa
    conv_repo.atualizar(conversa_id, titulo=conversa.titulo)
    
    return ChatResponse(resposta=resposta, metricas=metricas)

@router.delete("/conversas/{conversa_id}")
def deletar_conversa(conversa_id: UUID, session: Session = Depends(get_session)):
    """Deleta uma conversa."""
    repo = ConversaRepository(session)
    if not repo.deletar(conversa_id):
        raise HTTPException(status_code=404, detail="Conversa não encontrada")
    return {"mensagem": "Conversa deletada com sucesso"}
```

#### Ponto de Entrada da API

```python
# api/main.py
"""
Ponto de entrada da API FastAPI.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.database.connection import Database

app = FastAPI(
    title="Assistente de IA API",
    description="API REST para o assistente de IA com persistência",
    version="0.2.0",
)

# CORS para permitir acesso de outros apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir rotas
app.include_router(router, prefix="/api")

# Criar tabelas na inicialização
@app.on_event("startup")
def startup():
    db = Database()
    db.criar_tabelas()

@app.get("/")
def root():
    return {"mensagem": "Assistente de IA API", "versao": "0.2.0"}
```

### 2.4 Técnica

#### Migrações com Alembic

Alembic é a ferramenta de migração do SQLAlchemy [5]. Ele permite versionar o schema do banco e aplicar mudanças incrementalmente:

```bash
# Inicializar Alembic
alembic init alembic

# Criar migração automaticamente
alembic revision --autogenerate -m "Adicionar tabelas de conversas"

# Aplicar migração
alembic upgrade head

# Reverter última migração
alembic downgrade -1
```

**Arquivo de migração (gerado automaticamente):**

```python
# alembic/versions/xxxx_adicionar_tabelas.py
"""Adicionar tabelas de conversas

Revision ID: xxxx
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade():
    op.create_table(
        'conversas',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('titulo', sa.String(255), nullable=False),
        sa.Column('criado_em', sa.DateTime, server_default=sa.func.now()),
        sa.Column('atualizado_em', sa.DateTime, server_default=sa.func.now()),
        sa.Column('modelo', sa.String(50), nullable=False),
        sa.Column('metadata', sa.JSON, default={}),
    )
    
    op.create_table(
        'mensagens',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('conversa_id', UUID(as_uuid=True), 
                  sa.ForeignKey('conversas.id'), nullable=False),
        sa.Column('papel', sa.String(20), nullable=False),
        sa.Column('conteudo', sa.Text, nullable=False),
        sa.Column('tokens_entrada', sa.Integer),
        sa.Column('tokens_saida', sa.Integer),
        sa.Column('latencia_ms', sa.Float),
        sa.Column('criado_em', sa.DateTime, server_default=sa.func.now()),
    )

def downgrade():
    op.drop_table('mensagens')
    op.drop_table('conversas')
```

#### Testes Unitários

```python
# tests/test_chat.py
"""
Testes para o módulo de chat.
"""
import pytest
from unittest.mock import Mock, patch
from src.chat import Chat
from src.client import IAClient

@pytest.fixture
def mock_client():
    """Cria um mock do cliente de IA."""
    client = Mock(spec=IAClient)
    client.enviar.return_value = ("Resposta mock", {"tokens_entrada": 10, "tokens_saida": 20})
    return client

@pytest.fixture
def chat(mock_client):
    """Cria uma instância de chat com mock."""
    return Chat(mock_client, system_prompt="Você é um assistente de teste")

def test_enviar_mensagem(chat, mock_client):
    """Testa envio de mensagem."""
    resposta = chat.enviar("Olá")
    
    assert resposta == "Resposta mock"
    mock_client.enviar.assert_called_once()
    
    # Verificar que a mensagem foi adicionada ao histórico
    assert len(chat.mensagens) == 2  # system + user + assistant
    assert chat.mensagens[1]["role"] == "user"
    assert chat.mensagens[1]["content"] == "Olá"
    assert chat.mensagens[2]["role"] == "assistant"
    assert chat.mensagens[2]["content"] == "Resposta mock"

def test_limpar_historico(chat):
    """Testa limpeza do histórico."""
    chat.enviar("Primeira mensagem")
    chat.enviar("Segunda mensagem")
    
    chat.limpar()
    
    # Deve manter apenas o system prompt
    assert len(chat.mensagens) == 1
    assert chat.mensagens[0]["role"] == "system"

def test_exportar_historico(chat):
    """Testa exportação do histórico."""
    chat.enviar("Pergunta")
    
    historico = chat.exportar()
    
    assert isinstance(historico, list)
    assert len(historico) == 3  # system + user + assistant
```

#### docker-compose.yml

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ia_user
      POSTGRES_PASSWORD: ia_password
      POSTGRES_DB: ia_database
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ia_user"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://ia_user:ia_password@db:5432/ia_database
      DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY}
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app

volumes:
  postgres_data:
```

### 2.5 Aplica

#### Exercício Prático: Setup do Banco

1. **Inicie o PostgreSQL com Docker:**
```bash
docker-compose up -d db
```

2. **Execute as migrações:**
```bash
alembic upgrade head
```

3. **Inicie a API:**
```bash
uvicorn api.main:app --reload --port 8000
```

4. **Teste os endpoints (Documentação automática):**
- Acesse http://localhost:8000/docs (Swagger UI)
- Crie uma conversa: `POST /api/conversas`
- Envie uma mensagem: `POST /api/conversas/{id}/chat`
- Liste conversas: `GET /api/conversas`

5. **Teste com curl:**
```bash
# Criar conversa
curl -X POST http://localhost:8000/api/conversas \
  -H "Content-Type: application/json" \
  -d '{"titulo": "Minha primeira conversa"}'

# Enviar mensagem (substitua {id} pelo UUID retornado)
curl -X POST http://localhost:8000/api/conversas/{id}/chat \
  -H "Content-Type: application/json" \
  -d '{"conteudo": "O que é FastAPI?"}'
```

6. **Execute os testes:**
```bash
pytest tests/ -v
```

#### Checklist de Validação

- [ ] PostgreSQL rodando (Docker ou local)
- [ ] Migrações aplicadas com sucesso
- [ ] API inicia sem erros
- [ ] Documentação Swagger acessível em /docs
- [ ] Criar conversa funciona
- [ ] Enviar mensagem retorna resposta da IA
- [ ] Histórico é preservado no banco
- [ ] Testes passam (pytest)
- [ ] Métricas (tokens, latência) são registradas

### 2.6 Conclusão

Neste capítulo, transformamos nosso chat simples em uma API profissional com persistência. O projeto agora tem:

- **FastAPI** com endpoints REST documentados
- **PostgreSQL** persistindo conversas e mensagens
- **SQLAlchemy ORM** com modelos tipados
- **Alembic** para migrações versionadas
- **Métricas** de tokens e latência em cada resposta
- **Testes** automatizados

No próximo capítulo, vamos adicionar **RAG (Retrieval-Augmented Generation)** — a capacidade de o assistente buscar informações em documentos específicos antes de responder. Isso transformará nosso chat genérico em um assistente especializado no conteúdo que você escolher.

### 2.7 Referências

[1] Fielding, R.T. "Architectural Styles and the Design of Network-based Software Architectures." Doctoral dissertation, University of California, Irvine, 2000.

[2] Microsoft. "Design a RAG Solution." Azure Architecture Center, 2024. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/

[3] SQLAlchemy. "SQLAlchemy 2.0 Documentation." SQLAlchemy Project, 2024. Disponível em: https://docs.sqlalchemy.org/

[4] FastAPI. "FastAPI — Modern Python Web Framework." FastAPI Documentation, 2024. Disponível em: https://fastapi.tiangolo.com/

[5] Alembic. "Alembic — Database Migration Tool." Alembic Documentation, 2024. Disponível em: https://alembic.sqlalchemy.org/

[6] PostgreSQL. "PostgreSQL 15 Documentation." PostgreSQL Global Development Group, 2024. Disponível em: https://www.postgresql.org/docs/

[7] Docker. "Docker Compose Overview." Docker Documentation, 2024. Disponível em: https://docs.docker.com/compose/

[8] Pydantic. "Pydantic — Data Validation." Pydantic Documentation, 2024. Disponível em: https://docs.pydantic.dev/

[9] Uvicorn. "Uvicorn — ASGI Web Server." Uvicorn Documentation, 2024. Disponível em: https://www.uvicorn.org/

[10] Microsoft Azure Architecture Center. "Get Started with AI Architecture Design." Microsoft Learn, 2024. Disponível em: https://learn.microsoft.com/en-us/azure/architecture/ai-ml/ai-get-started

[11] AWS. "Machine Learning Lens — Well-Architected Framework." Amazon Web Services, 2024. Disponível em: https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/

[12] Google Cloud. "ML System Design Patterns." Google Cloud Architecture Center, 2023. Disponível em: https://cloud.google.com/architecture/ml-design-patterns

[13] Huyen, Chip. "Designing Machine Learning Systems." O'Reilly Media, 2022. ISBN: 978-1098107963.

[14] DeepSeek. "API Documentation." DeepSeek API Docs, 2024. Disponível em: https://api-docs.deepseek.com/

[15] OpenAI. "API Reference." OpenAI Platform Documentation, 2024. Disponível em: https://platform.openai.com/docs/api-reference

[16] Pinecone. "What is RAG?" Pinecone Learning Center, 2024. Disponível em: https://www.pinecone.io/learn/retrieval-augmented-generation/

[17] LangChain. "RAG from Scratch." LangChain Documentation, 2024. Disponível em: https://python.langchain.com/docs/tutorials/rag/

[18] OWASP. "Top 10 for Large Language Model Applications." OWASP Foundation, 2024. Disponível em: https://owasp.org/www-project-top-10-for-large-language-model-applications/

[19] NIST. "Artificial Intelligence Risk Management Framework." National Institute of Standards and Technology, 2024. Disponível em: https://www.nist.gov/artificial-intelligence/risk-management-framework

[20] Hugging Face. "PEFT Library." Hugging Face Documentation, 2024. Disponível em: https://huggingface.co/docs/peft

#### Versionamento de Dados e Schemas

Quando você muda o schema do banco, precisa de migrações seguras [6]:

**Regras de ouro para migrações:**

1. **Nunca delete dados** em migrações — apenas adicione colunas
2. **Mantenha compatibilidade** com versões anteriores
3. **Teste migrações** antes de aplicar em produção
4. **Tenha um rollback** para cada migração

**Exemplo de migração segura:**

```python
# Alembic: Adicionar coluna sem quebrar código existente
def upgrade():
    # 1. Adicionar coluna com valor padrão
    op.add_column('mensagens', 
        sa.Column('tokens_entrada', sa.Integer, nullable=True))
    
    # 2. Preencher dados existentes (opcional)
    op.execute("""
        UPDATE mensagens 
        SET tokens_entrada = 0 
        WHERE tokens_entrada IS NULL
    """)
    
    # 3. Tornar NOT NULL apenas depois de preencher
    op.alter_column('mensagens', 'tokens_entrada', nullable=False)

def downgrade():
    op.drop_column('mensagens', 'tokens_entrada')
```

**Versionamento de dados para IA:**

```python
# src/database/versioning.py
"""
Versionamento de dados para sistemas de IA.
"""
from datetime import datetime
from typing import Dict, Any

class DataVersioner:
    """Gerencia versões de dados em sistemas de IA."""
    
    def __init__(self):
        self.versions: Dict[str, Dict] = {}
    
    def criar_versao(self, dados: Dict, metadado: str = "") -> str:
        """Cria uma nova versão dos dados."""
        import hashlib
        import json
        
        # Gerar hash dos dados
        dados_str = json.dumps(dados, sort_keys=True)
        version_id = hashlib.md5(dados_str.encode()).hexdigest()[:8]
        
        self.versions[version_id] = {
            "dados": dados,
            "metadado": metadado,
            "criado_em": datetime.now().isoformat(),
        }
        
        return version_id
    
    def comparar_versoes(self, v1: str, v2: str) -> Dict:
        """Compara duas versões de dados."""
        dados1 = self.versions.get(v1, {}).get("dados", {})
        dados2 = self.versions.get(v2, {}).get("dados", {})
        
        # Encontrar diferenças
        diferencas = {}
        all_keys = set(list(dados1.keys()) + list(dados2.keys()))
        
        for key in all_keys:
            val1 = dados1.get(key)
            val2 = dados2.get(key)
            
            if val1 != val2:
                diferencas[key] = {"antes": val1, "depois": val2}
        
        return {
            "versao1": v1,
            "versao2": v2,
            "diferencas": diferencas,
            "total_diferencas": len(diferencas),
        }
```

**Backup automático:**
```python
# scripts/backup_dados.py
"""
Backup automático do banco de dados.
"""
import subprocess
from datetime import datetime
from pathlib import Path

def backup_postgres():
    """Cria backup do PostgreSQL."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)
    
    backup_file = backup_dir / f"ia_database_{timestamp}.sql"
    
    subprocess.run([
        "pg_dump",
        "-h", "localhost",
        "-U", "ia_user",
        "-d", "ia_database",
        "-f", str(backup_file),
    ], check=True)
    
    print(f"Backup criado: {backup_file}")
    return backup_file

if __name__ == "__main__":
    backup_postgres()
```

**Agendamento de backups:**
```bash
# Adicionar ao crontab (Linux/Mac)
# Backup diário às 2:00 AM
0 2 * * * cd /app && python scripts/backup_dados.py >> logs/backup.log 2>&1
```

