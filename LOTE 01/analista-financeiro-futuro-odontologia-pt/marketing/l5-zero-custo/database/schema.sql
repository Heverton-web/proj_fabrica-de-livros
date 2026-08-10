-- Máquina de Vendas — Schema SQLite

CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    telefone TEXT DEFAULT '',
    empresa TEXT DEFAULT '',
    cargo TEXT DEFAULT '',
    fonte TEXT DEFAULT '',
    etapa_funil TEXT DEFAULT 'novo' CHECK (etapa_funil IN ('novo', 'qualificado', 'proposta', 'negociacao', 'ganho', 'perdido')),
    score INTEGER DEFAULT 0 CHECK (score >= 0 AND score <= 100),
    tags TEXT DEFAULT '',
    notas TEXT DEFAULT '',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    tipo TEXT NOT NULL,
    descricao TEXT DEFAULT '',
    metadata TEXT DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS vendas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    valor REAL DEFAULT 0,
    moeda TEXT DEFAULT 'BRL',
    status TEXT DEFAULT 'proposta' CHECK (status IN ('proposta', 'aceita', 'recusada', 'cancelada')),
    produto TEXT DEFAULT '',
    notas TEXT DEFAULT '',
    closed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS campanhas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT DEFAULT '',
    tipo TEXT DEFAULT 'email' CHECK (tipo IN ('email', 'sms', 'whatsapp')),
    status TEXT DEFAULT 'rascunho' CHECK (status IN ('rascunho', 'ativa', 'pausada', 'finalizada')),
    template_assunto TEXT DEFAULT '',
    template_corpo TEXT DEFAULT '',
    segmento_tags TEXT DEFAULT '',
    agendada_para TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS emails_enviados (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER NOT NULL,
    campanha_id INTEGER,
    assunto TEXT DEFAULT '',
    corpo TEXT DEFAULT '',
    status TEXT DEFAULT 'enviado' CHECK (status IN ('enviado', 'erro', 'aberto', 'clicado')),
    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id) ON DELETE CASCADE,
    FOREIGN KEY (campanha_id) REFERENCES campanhas(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS metricas_diarias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT NOT NULL UNIQUE,
    total_leads INTEGER DEFAULT 0,
    leads_novos INTEGER DEFAULT 0,
    leads_qualificados INTEGER DEFAULT 0,
    leads_ganhos INTEGER DEFAULT 0,
    receita_dia REAL DEFAULT 0
);

-- Índices para performance
CREATE INDEX IF NOT EXISTS idx_leads_score ON leads(score DESC);
CREATE INDEX IF NOT EXISTS idx_leads_etapa ON leads(etapa_funil);
CREATE INDEX IF NOT EXISTS idx_leads_email ON leads(email);
CREATE INDEX IF NOT EXISTS idx_interacoes_lead ON interacoes(lead_id);
CREATE INDEX IF NOT EXISTS idx_interacoes_tipo ON interacoes(tipo);
CREATE INDEX IF NOT EXISTS idx_vendas_lead ON vendas(lead_id);
CREATE INDEX IF NOT EXISTS idx_vendas_status ON vendas(status);
CREATE INDEX IF NOT EXISTS idx_emails_lead ON emails_enviados(lead_id);
CREATE INDEX IF NOT EXISTS idx_emails_campanha ON emails_enviados(campanha_id);
CREATE INDEX IF NOT EXISTS idx_metricas_data ON metricas_diarias(data);
