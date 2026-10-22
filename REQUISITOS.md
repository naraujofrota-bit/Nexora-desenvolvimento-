# Nexora — requisitos específicos do sistema

Extraído do **Roteiro de Desenvolvimento — Sistema de Gestão de Demandas e Desenvolvimento, Web + PWA, versão 2.0** (17 páginas) e adaptado ao nome e à identidade visual Nexora apresentados pela usuária. No roteiro, “TaskHub” é explicitamente um nome provisório; neste projeto, o nome de produto é **Nexora**. Os nomes e números de exemplo das telas de referência não são dados reais do negócio.

## 1. Objetivo e limites

Nexora deve organizar correções, manutenção e evolução de sistemas de produção administrados por uma gestora, com equipe inicial de uma gestora e dois programadores. A primeira configuração prevê dois sistemas em produção, cada um de uma empresa diferente, mas a estrutura deve aceitar mais empresas, sistemas e pessoas.

O fluxo principal vai do registro e priorização da demanda à atribuição, desenvolvimento, teste/homologação, eventual registro de publicação e encerramento com histórico. A interface deve servir tanto à visão gerencial quanto à execução diária da equipe.

Fora da primeira versão: integração funcional com GitHub, assistente de IA, chat independente, aplicativos nativos Android/iOS e gerenciamento complexo de sprints. O registro da publicação é manual.

## 2. Estrutura do produto

Seis páginas principais no menu:

1. **Dashboard** — indicadores reais e atalhos para prazos, tarefas e atividades.
2. **Demandas** — cadastro, busca, filtros, lista, detalhes e comunicação por demanda.
3. **Kanban** — fluxo compartilhado com a lista de demandas.
4. **Projetos** — no domínio do roteiro, cada projeto representa um sistema vinculado a uma empresa.
5. **Planejamento** — backlog e demandas previstas por semana ou mês.
6. **Configurações** — perfil, pessoas, empresas, permissões e preferências.

Elementos auxiliares: login, painel lateral de detalhes/cadastro e central de notificações. No desktop: navegação lateral, cabeçalho, seletor de empresa/sistema, notificações e perfil. Em celular/PWA: navegação compacta ou inferior, áreas tocáveis, formulários responsivos, cartões e acesso simples às tarefas atribuídas.

## 3. Requisitos funcionais

### 3.1 Login, contas e permissões

- Login individual, com nome, e-mail e senha; recuperação/alteração de senha.
- Perfis iniciais: **Gestora/Administradora** e **Programador**.
- A gestora administra empresas, sistemas, módulos, usuários e permissões; cria/edita demandas; prioriza e atribui; aprova ou reprova homologações; registra publicações e consulta indicadores dos projetos que administra.
- O programador consulta apenas projetos autorizados, vê suas demandas, atualiza situação, comenta, anexa evidências, registra bloqueios, envia itens para teste e consulta histórico.
- Programadores não administram permissões. O servidor e o banco precisam aplicar a autorização; ocultar um botão na interface não é controle de acesso.
- Usuários podem ser convidados/cadastrados, editados, ativados ou desativados; projeto deve listar os responsáveis autorizados.

### 3.2 Empresas, sistemas e módulos

- CRUD de empresas.
- CRUD de sistemas/projetos, sempre vinculados a uma única empresa; situação: ativo, pausado ou encerrado.
- Sistema contém nome, descrição, empresa, módulos e usuários autorizados.
- Detalhe do sistema exibe contagem de demandas abertas/concluídas, demandas relacionadas e histórico de publicações.
- Registro manual de publicação: versão, data, responsável, demandas incluídas, observações e resultado.
- Não integrar a publicação com GitHub nesta versão.

### 3.3 Demandas

Campos obrigatórios: título, empresa e sistema (sistema determina a empresa), tipo, descrição e prioridade.

Campos opcionais: módulo, responsável principal, prazo, imagens/anexos, resultado esperado, passos para reproduzir, critérios de aceite e observações.

Tipos: bug/erro, correção, melhoria, nova funcionalidade, tarefa técnica e ajuste visual. Prioridades: crítica, alta, média e baixa.

Capacidades: código único; criar e editar; lista/tabela; pesquisar por título/código; filtrar por empresa, sistema, responsável, prioridade e situação; ordenar por criação, prazo e prioridade; abrir detalhe com todos os campos, comentários, anexos, checklist/subtarefas, histórico e resultado de homologação. Demandas concluídas continuam consultáveis e incluídas nos relatórios.

Comunicação por demanda: comentários com autor e data/hora, menções a integrantes, anexos/evidências, esclarecimentos e decisões anteriores. Alterações importantes no registro devem criar histórico auditável. Demanda cancelada exige motivo.

### 3.4 Fluxo e homologação

O Kanban tem exatamente quatro colunas: **A fazer → Em andamento → Em teste → Concluído**. “Bloqueada” é uma marcação, não uma quinta coluna.

- Arrastar cartão ou mudar situação por seletor (o seletor é essencial em celular).
- Cartão mostra prioridade, prazo, responsável e indicador de bloqueio; abre os detalhes.
- Ao entrar em “Em teste”, registrar encaminhamento para homologação.
- Só a gestora aprova ou reprova homologação. Aprovação encerra o fluxo de desenvolvimento; reprovação exige justificativa e retorna a demanda a “Em andamento”.
- Registrar autor e data das mudanças de estado, bloqueios, encaminhamentos, decisão de homologação e cancelamentos.
- Lista, Kanban, dashboard e planejamento devem refletir os mesmos registros persistidos.

### 3.5 Dashboard

Mostrar total de demandas abertas, em andamento, aguardando teste, concluídas, atrasadas e críticas. Filtrar por empresa e sistema. Incluir distribuição por situação, atividades recentes, prazos próximos, tarefas atribuídas ao usuário e abertura direta de uma demanda.

Indicadores são agregações dos registros reais, nunca números fixos. Gestora vê os projetos a que tem acesso; programador recebe destaque para suas próprias atribuições. Definições para implementar de forma consistente: “aberta” = situação diferente de Concluído e não cancelada; “atrasada” = prazo anterior à data atual e ainda não concluída/cancelada; “crítica” = prioridade Crítica e ainda não concluída/cancelada.

### 3.6 Planejamento

- Backlog: demanda ainda sem período planejado.
- Planejamento: demanda associada a semana ou mês, com prioridade, prazo e responsável.
- Visualizar entregas previstas e reorganizar prioridades.
- Não exigir Scrum nem sprints.

### 3.7 Notificações

Central interna acessível pelo sino, com autor/contexto e data. Gerar pelo menos notificações de atribuição, menção em comentário, devolução para correção e solicitação de homologação. Push com app fechado fica fora do primeiro release.

### 3.8 PWA e conexão

- Implementar depois de estabilizar os fluxos web essenciais.
- Manifesto com nome Nexora, nome curto, ícones 192×192 e 512×512, cores e modo standalone; tela inicial do sistema operacional quando suportada.
- Service worker, experiência móvel revista e deploy seguro por HTTPS.
- Offline limitado à abertura da interface já armazenada em cache e aviso de falta de conexão. Login validado no servidor, CRUD, comentários, upload, mudanças de estado e sincronização exigem internet. Não implementar fila de mutações offline.
- Atualizações do service worker precisam conduzir corretamente à versão compatível mais recente.
- Tratar carregamento, erro e perda de conexão. Validar instalação em Android e em navegador desktop compatível.

## 4. Modelo de dados recomendado

- **User**: id, nome, e-mail, perfil, estado da conta, avatar opcional, preferências.
- **Company**: id, nome, descrição, estado.
- **Project/System**: id, company_id, nome, descrição, estado.
- **Module**: id, project_id, nome, descrição.
- **ProjectMember**: user_id, project_id, permissões concedidas.
- **Demand**: id/código público único, project_id, module_id opcional, título, descrição, tipo, prioridade, situação, bloqueada, owner_id, criador_id, prazo, resultado esperado, passos, critérios de aceite, observações, período de planejamento, cancelamento e timestamps.
- **Comment** e **Mention**: demanda, autor, texto, data/hora e destinatários mencionados.
- **Attachment**: demanda/comentário, caminho privado no Storage, nome, tipo, tamanho, autor e data.
- **ChecklistItem**: demanda, texto, estado, ordem, responsável opcional.
- **DemandEvent**: demanda, ator, tipo de alteração, valor anterior/novo, justificativa e data/hora.
- **Release** e **ReleaseDemand**: sistema, versão, data, responsável, resultado/observações e demandas incluídas.
- **Notification**: destinatário, tipo, entidade relacionada, leitura e data/hora.

Exigir chaves estrangeiras e índices para empresa/sistema/situação, responsável, prioridade, prazo e código. Arquivos ficam em armazenamento privado; metadados no banco. Nunca depender de dados do navegador como fonte de verdade.

## 5. Arquitetura e qualidade

Stack proposta pelo roteiro: Next.js + React + TypeScript, Tailwind CSS e shadcn/ui; API Next.js; PostgreSQL; Supabase Auth e Storage; manifesto e service worker. Usar migrações versionadas, validação client/server, segredos fora do código, autorização aplicada no servidor/banco, erros tratados e componentes reaproveitáveis. O projeto precisa documentar configuração, migrações, execução e uso. O uso interno de Git para versionar o código não equivale à integração com GitHub, que permanece fora do produto.

## 6. Etapas de entrega e aceite

1. **Planejamento e protótipo:** estrutura, mapa das seis páginas, navegação desktop/celular, componentes e proposta de banco. Aceite: a gestora consegue entender o percurso de criar, acompanhar e concluir uma demanda.
2. **Base:** app executável, responsivo, login, menu, cadastros de empresas/sistemas e usuários, permissões e banco. Aceite: cada pessoa só acessa projetos autorizados.
3. **Demandas:** CRUD, lista, busca/filtros, detalhes, atribuição, comentários, anexos e histórico. Aceite: dados persistem após recarregar e autenticar novamente.
4. **Kanban:** quatro colunas, movimentação, filtros, responsáveis, bloqueio, envio para teste, aprovação/reprovação. Aceite: estado salvo aparece igual em todas as telas.
5. **Dashboard e planejamento:** indicadores reais, backlog, planejamento por semana/mês, prazos, prioridades, notificações internas e publicações. Aceite: filtros e agregações correspondem aos dados cadastrados.
6. **PWA:** manifesto, ícones, service worker, instalação, layout móvel, aviso offline e HTTPS. Aceite: instalação e funcionalidades online verificadas em Android e browser desktop suportado.
7. **Testes e entrega:** corrigir defeitos, validar permissões, formulários, homologação, responsividade e PWA; documentação de instalação e manual. Aceite: pessoa usuária completa o fluxo principal seguindo o manual sem assistência.

## 7. O que existe agora e o que precisa ser corrigido

A base visual existente em `index.html` cobre parcialmente o dashboard e um formulário simples salvo em `localStorage`. Ela **não satisfaz ainda** os requisitos do roteiro: não tem autenticação nem banco compartilhado; empresas/sistemas e permissões; campos obrigatórios/ opcionais especificados; anexos, comentários, checklist ou auditoria; Kanban e homologação; planejamento; notificações reais; ícones PWA próprios nem gestão de atualização. A navegação para páginas futuras ainda é demonstrativa. Dados de exemplo da referência não devem ser tratados como registros reais.

Portanto, tratar o painel atual como protótipo da **etapa 1**, não como sistema pronto para uso multiusuário. Antes da etapa 2, organizar o projeto e confirmar estrutura/decisões técnicas; avançar por etapa com critérios de aceite claros.

## 8. Configuração inicial confirmada e dados pendentes

- **Cris** — Gestora/Administradora.
- **Naiana** — Programadora.
- **Bioflex** e **Pontual Gráfica** — empresas acompanhadas inicialmente.

O roteiro prevê sistemas vinculados às empresas, mas os nomes dos sistemas ainda não foram informados. “Módulo” é uma divisão funcional *dentro de um sistema*, não outra empresa ou outro sistema. Por exemplo, um sistema de gestão poderia ter módulos Financeiro, Estoque e Relatórios; esses exemplos não são dados confirmados de Bioflex nem Pontual Gráfica. O módulo é opcional no cadastro da demanda e só deve ser cadastrado se cada sistema realmente tiver divisões desse tipo. Até confirmar, deixar módulo sem preenchimento.

Também faltam os nomes dos sistemas de cada empresa, e-mails/contas dos usuários, política inicial de acesso a cada sistema e ambiente/conta Supabase de destino. Definir domínio para deploy HTTPS quando chegar a etapa PWA. Os nomes “Maria”, “João” e outros da referência são exemplos visuais; não os tratar como integrantes reais.

## 9. Identidade de marca

Usar o nome **Nexora** e a assinatura **“Demandas que viram progresso”** da referência. Paleta: azul principal `#2563EB`, azul escuro `#0F172A`, verde-água `#14B8A6`, verde `#22C55E`, âmbar `#F59E0B`, vermelho `#EF4444`, cinza claro `#E5E7EB`, cinza escuro `#64748B`. Tipografia Inter. A referência recebida fica preservada sem edição em `assets/referencia-idv.jpeg`; não redesenhar, recolorir ou substituir a logo.
