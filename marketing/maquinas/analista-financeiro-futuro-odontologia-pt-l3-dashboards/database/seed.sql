-- Máquina de Vendas — Dados de exemplo

INSERT INTO leads (nome, email, telefone, empresa, cargo, fonte, etapa_funil, score, tags, notas)
VALUES
    ('Ana Souza', 'ana.souza@editoranova.com.br', '(11) 99876-5432', 'Editora Nova', 'Diretora de Publicações', 'organico', 'qualificado', 65, 'livro,publishing', 'Interessada em publicação de livros técnicos'),
    ('Carlos Oliveira', 'carlos@techbooks.com', '(21) 98765-4321', 'TechBooks', 'CEO', 'paid', 'proposta', 78, 'ebook,tech', 'Pediu proposta para série de e-books'),
    ('Maria Fernanda', 'maria.f@grupoleitura.com', '(31) 97654-3210', 'Grupo Leitura', 'Gerente de Marketing', 'referral', 'novo', 25, 'marketing,indicacao', 'Indicada por Ana Souza'),
    ('Pedro Santos', 'pedro.santos@editoraalfa.com', '(41) 96543-2109', 'Editora Alfa', 'Editor-Chefe', 'evento', 'negociacao', 82, 'livro,premium', 'Reunião agendada para sexta'),
    ('Juliana Lima', 'juliana@livrosdigitais.com.br', '(51) 95432-1098', 'Livros Digitais', 'Head de Conteúdo', 'organico', 'qualificado', 55, 'ebook,digital', 'Baixou nosso e-book gratuito'),
    ('Rafael Costa', 'rafael@publishtech.io', '(11) 94321-0987', 'PublishTech', 'CTO', 'paid', 'ganho', 95, 'tech,enterprise', 'Fechou contrato de 12 meses'),
    ('Fernanda Alves', 'fernanda@editoramax.com', '(21) 93210-9876', 'Editora Max', 'Diretora Comercial', 'webhook', 'novo', 10, 'comercial', 'Lead via formulário do site'),
    ('Lucas Mendes', 'lucas.m@bookfactory.com', '(31) 92109-8765', 'BookFactory', 'Product Manager', 'referral', 'proposta', 70, 'tech,produto', 'Aguardando retorno da proposta'),
    ('Camila Rodrigues', 'camila@leituracriativa.com', '(41) 91098-7654', 'Leitura Criativa', 'Fundadora', 'organico', 'novo', 20, 'infantil,criativo', 'Visitou a landing page 3 vezes'),
    ('Bruno Carvalho', 'bruno@edicoespremium.com', '(51) 90987-6543', 'Edições Premium', 'VP de Vendas', 'evento', 'qualificado', 60, 'premium,evento', 'Conheceu na FLIP 2025');

INSERT INTO interacoes (lead_id, tipo, descricao)
VALUES
    (1, 'email_aberto', 'Abriu email de boas-vindas'),
    (1, 'email_clicado', 'Clicou no link do catálogo'),
    (1, 'visita_site', 'Visitou página de preços'),
    (2, 'email_aberto', 'Abriu sequência de nurturing #1'),
    (2, 'email_clicado', 'Clicou em "ver proposta"'),
    (2, 'download', 'Baixou PDF de cases de sucesso'),
    (3, 'email_aberto', 'Abriu email de boas-vindas'),
    (4, 'email_aberto', 'Abriu 5 emails'),
    (4, 'email_clicado', 'Clicou em 3 links diferentes'),
    (4, 'resposta', 'Respondeu pedindo reunião'),
    (4, 'visita_site', 'Visitou página de pricing 2x'),
    (5, 'email_aberto', 'Abriu email de boas-vindas'),
    (5, 'download', 'Baixou e-book gratuito'),
    (6, 'email_aberto', 'Abriu todos os emails da campanha'),
    (6, 'email_clicado', 'Clicou em links de demonstração'),
    (6, 'resposta', 'Respondeu com interesse'),
    (6, 'visita_site', 'Visitou site 10 vezes'),
    (6, 'download', 'Baixou whitepaper técnico');

INSERT INTO vendas (lead_id, valor, moeda, status, produto, notas)
VALUES
    (6, 12000.00, 'BRL', 'aceita', 'Plano Enterprise Anual', 'Contrato de 12 meses com suporte prioritário'),
    (2, 4500.00, 'BRL', 'proposta', 'Pacote E-book Premium', 'Proposta enviada, aguardando aprovação'),
    (4, 8000.00, 'BRL', 'proposta', 'Plano Profissional Semestral', 'Reunião agendada para fechar');

INSERT INTO campanhas (nome, descricao, tipo, status, template_assunto, template_corpo, segmento_tags)
VALUES
    ('Boas-vindas', 'Sequência de boas-vindas para novos leads', 'email', 'ativa',
     'Bem-vindo(a), {{nome}}!',
     '<h1>Olá, {{nome}}!</h1><p>Obrigado por se cadastrar. Somos a Fábrica de Livros e ajudamos autores a publicar.</p><p>Em breve entraremos em contato.</p>',
     'novo'),
    ('Reengajamento', 'Reativar leads frios', 'email', 'rascunho',
     'Sentimos sua falta, {{nome}}',
     '<h1>Olá, {{nome}}</h1><p>Faz tempo que não nos vemos. Que tal conferir as novidades?</p>',
     'frio'),
    ('Pós-reunião', 'Follow-up após reunião comercial', 'email', 'ativa',
     'Próximos passos - {{empresa}}',
     '<h1>Olá, {{nome}}</h1><p>Foi ótimo conversar com você. Seguem os próximos passos discutidos.</p>',
     'reuniao');

INSERT INTO metricas_diarias (data, total_leads, leads_novos, leads_qualificados, leads_ganhos, receita_dia)
VALUES
    ('2025-01-06', 7, 2, 2, 1, 12000.00),
    ('2025-01-07', 8, 1, 2, 1, 0.00),
    ('2025-01-08', 9, 1, 3, 1, 0.00),
    ('2025-01-09', 10, 1, 3, 1, 4500.00),
    ('2025-01-10', 10, 0, 3, 1, 0.00);
