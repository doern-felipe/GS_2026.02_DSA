# O Tempo Vale — Protótipo Web (MVP)

Plataforma de colaboração comunitária onde **1 hora de contribuição = 1 crédito de tempo**.

## Como executar
**Opção 1 (recomendada):** Dê um duplo clique em `index.html` — a plataforma abre direto no navegador, sem instalar nada (o projeto usa `js/bundle.js`, script clássico compatível com arquivo local).
**Opção 2:** Sirva a pasta com um servidor estático (ex.: `python -m http.server 8080` nesta pasta) e acesse `http://localhost:8080/`.
3. Entre com a conta demo: **demo@tempovale.com** (qualquer senha), botão **Acessar demonstração** ou **Continuar como visitante**.

## Estrutura
```
index.html
css/styles.css        — Design system (paleta #F8F7F4 / #3D5145 / #CC5500, Manrope)
css/responsive.css    — 1024 / 768 / 420px (sidebar desktop, bottom nav mobile com 5 itens)
js/bundle.js         — Bundle clássico gerado (data + storage + módulos + app, sem imports)
js/data.js            — Seed: 8 usuários, 12 oportunidades, 4 projetos, 8 notificações, 10 lançamentos
js/storage.js         — Persistência localStorage + reset
js/app.js             — SPA (hash router, telas, ações) — versão modular para servidor HTTP
js/modules/
  utils.js            — formatadores, toast, modal
  credits.js          — saldo, histórico, transferência única após confirmação mútua
  opportunities.js    — busca, filtros, ordenação
  projects.js         — progresso e filtros de projetos
  notifications.js    — avisos e não-lidas
```

## Fluxo demonstrável
Explorar → abrir “Aula de inglês para iniciantes” → Tenho interesse → (Minhas atividades) Aceitar/Confirmar → Marcar como realizada → Confirmar horas (mútua) → carteira atualizada → Projetos → participar em “Nossa Praça, Nosso Espaço” → contador e progresso atualizados.

## Regras implementadas
- Créditos nunca movimentam só por interesse; exigem conclusão + confirmação dos dois lados (status `Aguardando confirmação` até lá) e movimentam **uma única vez** (`activity.credited`).
- Projetos: progresso = horas confirmadas / meta; responsável registra horas e atualizações.
- Perfil: nível por atividades/consistência/avaliações (não só saldo).
- Restaurar dados: **Configurações → Restaurar dados demonstrativos**.

## Nota de segurança
Autenticação e persistência são **apenas demonstrativas** (localStorage). Não use localStorage para dados sensíveis em produção; substitua por API/banco de dados na evolução para app.
