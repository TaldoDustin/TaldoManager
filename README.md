# ⚽ Taldo Manager

Um Football Manager desenvolvido em Python com foco em aprendizado prático de programação.

O projeto está sendo construído do zero para estudar lógica de programação, orientação a objetos, arquitetura de software e desenvolvimento de sistemas.

---

# 🚀 Funcionalidades

## Jogadores

* ✅ Cadastro de jogadores
* ✅ Nome
* ✅ Idade
* ✅ Posição
* ✅ Overall
* ✅ Jogos
* ✅ Gols
* ✅ Assistências
* ✅ Média de nota
* ✅ Melhor nota
* ✅ Pior nota
* ✅ Melhor em campo
* ✅ Hat-tricks
* ✅ Pênaltis convertidos
* ✅ Pênaltis perdidos
* ✅ Clean Sheets
* ✅ Cartões amarelos
* ✅ Cartões vermelhos

---

## Clubes

* ✅ Cadastro de clubes
* ✅ País
* ✅ Dinheiro
* ✅ Elenco de jogadores
* ✅ Cálculo automático da força
* ✅ Forma recente
* ✅ Vantagem de mando de campo

---

## Partidas

* ✅ Simulação baseada na força dos clubes
* ✅ Geração de gols
* ✅ Distribuição de gols por posição
* ✅ Distribuição de assistências por posição
* ✅ Sistema de notas
* ✅ Melhor jogador da partida
* ✅ Clean Sheets
* ✅ Resultado automático
* ✅ Empates
* ✅ Placar completo
* ✅ Hat-tricks
* ✅ Pênaltis
* ✅ Pênaltis perdidos
* ✅ Cartões amarelos
* ✅ Cartões vermelhos
* ✅ Segundo amarelo
* ✅ Eventos cronológicos
* ✅ Ordenação por minuto

---

## Campeonato

* ✅ Cadastro de campeonatos
* ✅ Calendário turno e returno
* ✅ Sorteio automático de rodadas
* ✅ Histórico de partidas
* ✅ Classificação
* ✅ Critérios de desempate
* ✅ Artilharia
* ✅ Assistências
* ✅ Ranking de notas
* ✅ MVP do campeonato
* ✅ Ranking de Clean Sheets
* ✅ Ranking de Hat-tricks
* ✅ Recordes do campeonato

---

## Estrutura

* ✅ Separação dos dados (Seed)
* ✅ Arquivos JSON
* ✅ Carregamento automático dos dados
* ✅ Código refatorado em métodos menores
* ✅ Eventos estruturados em dicionários
* ✅ Processamento cronológico de eventos

---

# 📚 Tecnologias

* Python 3
* Programação Orientada a Objetos (POO)
* JSON
* Git
* GitHub

---

# 🎯 Objetivo

Este projeto tem como objetivo estudar:

* Lógica de programação
* Orientação a Objetos
* Arquitetura de Software
* Estruturação de projetos
* Simulação de sistemas
* Git e GitHub
* Banco de Dados
* Flask

---

# 🗺️ Roadmap

## ✅ Versão Atual (v0.5) — Concluída

### Base do jogo

* [x] Cadastro de jogadores
* [x] Cadastro de clubes
* [x] Contratação de jogadores
* [x] Seed em JSON
* [x] Loader automático

### Simulação

* [x] Cálculo de força dos clubes
* [x] Mando de campo
* [x] Forma recente
* [x] Simulação de partidas
* [x] Distribuição de gols
* [x] Distribuição de assistências
* [x] Sistema de notas
* [x] Melhor jogador da partida
* [x] Clean Sheets
* [x] Hat-tricks
* [x] Pênaltis
* [x] Pênaltis perdidos
* [x] Cartões amarelos
* [x] Cartões vermelhos
* [x] Segundo amarelo
* [x] Eventos cronológicos
* [x] Ordenação dos eventos

### Campeonato

* [x] Campeonato
* [x] Calendário turno e returno
* [x] Histórico
* [x] Classificação
* [x] Critérios de desempate
* [x] Artilharia
* [x] Assistências
* [x] Ranking de notas
* [x] MVP do campeonato
* [x] Ranking de Hat-tricks
* [x] Recordes do campeonato

### Código

* [x] Refatoração da classe Partida
* [x] Refatoração da classe Campeonato
* [x] Métodos reutilizáveis
* [x] Organização do projeto
* [x] Sistema de eventos estruturados

---

# 🚧 Próxima Sprint (v0.6)

## Eventos Avançados

* [ ] Expulsão afetando força do time
* [ ] Suspensão automática por vermelho
* [ ] Suspensão por acúmulo de amarelos
* [ ] Lesões
* [ ] Pênaltis defendidos
* [ ] Defesas difíceis
* [ ] Acréscimos
* [ ] Substituições

## Estatísticas da Partida

* [ ] Posse de bola
* [ ] Finalizações
* [ ] Chutes no gol
* [ ] Escanteios
* [ ] Faltas

## Estatísticas Gerais

* [ ] Histórico individual dos jogadores
* [ ] Estatísticas por temporada
* [ ] Ranking de cartões
* [ ] Ranking de pênaltis
* [ ] Ranking de melhores em campo

---

# 💰 Mercado (v0.7)

* [ ] Valor de mercado
* [ ] Salários
* [ ] Sistema financeiro
* [ ] Compra de jogadores
* [ ] Venda de jogadores
* [ ] Negociações
* [ ] Renovação de contrato
* [ ] Evolução por idade
* [ ] Potencial dos jogadores

---

# 🏆 Modo Carreira (v0.8)

* [ ] Temporadas
* [ ] Histórico de campeões
* [ ] Envelhecimento
* [ ] Aposentadoria
* [ ] Geração de jovens
* [ ] Categorias de base
* [ ] Hall da Fama

---

# 💾 Persistência (v0.9)

* [ ] SQLite
* [ ] Sistema de Save
* [ ] Carregar Save
* [ ] Autosave

---

# 🌐 Web (v1.0)

* [ ] API Flask
* [ ] Interface Web
* [ ] Dashboard do campeonato
* [ ] Dashboard financeiro
* [ ] Painel de jogadores
* [ ] Mercado de transferências
* [ ] Estatísticas avançadas

---

# 📁 Estrutura

```text
TaldoManager/
│
├── data/
│   ├── jogadores.json
│   ├── clubes.json
│   └── loader.py
│
├── jogadores.py
├── clubes.py
├── partidas.py
├── campeonatos.py
├── main.py
│
└── README.md
```

---

# 🎯 Meta de Desenvolvimento

**Objetivo:** manter uma rotina consistente de **1 a 3 horas por dia**.

## Regras do Projeto

* ✅ Desenvolver pelo menos uma funcionalidade por semana
* ✅ Não iniciar um sistema novo antes de concluir o atual
* ✅ Testar todas as implementações
* ✅ Refatorar quando necessário
* ✅ Fazer commit ao final de cada sessão
* ✅ Executar `git push` após cada commit
* ✅ Atualizar o roadmap sempre que uma funcionalidade for concluída

---

# 🎯 Objetivo de Curto Prazo

Transformar o Taldo Manager em um simulador completo de campeonatos com:

* ✅ Estatísticas completas
* ⏳ Eventos avançados
* ⏳ Mercado de transferências
* ⏳ Evolução dos jogadores
* ⏳ Temporadas contínuas
* ⏳ Sistema de Save

---

# 🎯 Objetivo Final

Criar um Football Manager totalmente jogável contendo:

* Banco de Dados SQLite
* API Flask
* Interface Web
* Dashboard completo
* Mercado de transferências
* Sistema financeiro
* Modo carreira
* Temporadas infinitas
* Versão jogável pelo navegador

---

> 🚀 **Lembrete:** consistência vence intensidade. Desenvolver entre **1 e 3 horas por dia** representa aproximadamente **30 a 90 horas de evolução por mês**. Pequenos avanços diários constroem grandes projetos.
