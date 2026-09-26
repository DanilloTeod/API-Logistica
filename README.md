# 📦 Sistema de Logística API

Este é um projeto de portfólio focado no desenvolvimento de um sistema back-end robusto para gestão de entregas e logística, simulando regras de negócio reais do mercado corporativo. 

## Intuito do Projeto
O objetivo principal desta API é gerenciar o fluxo completo de uma transportadora, desde o cadastro de frotas e motoristas até o rastreamento de pacotes em tempo real. O sistema atua como o "motor" central, capaz de receber requisições de aplicativos mobile (usados pelos motoristas) e de plataformas web (usadas por clientes e painel administrativo).

Do ponto de vista técnico, o projeto foi desenhado para demonstrar domínio completo sobre a stack **Python + Django**, evoluindo desde a modelagem relacional de dados até a construção de endpoints RESTful seguros, execução de tarefas em segundo plano e conteinerização da infraestrutura.

---

## Status Atual: Fase de Modelagem e Backoffice
Atualmente, o projeto concluiu a estruturação da base de dados relacional e a interface administrativa inicial.

**O que já está implementado:**
* **Modelagem de Dados (ORM):** Criação das entidades principais (`Caminhao`, `Motorista`, `Pacote`).
* **Relacionamentos Complexos:** Implementação de regras de negócio rigorosas utilizando Chaves Estrangeiras (`ForeignKey`) com proteção de integridade referencial (`models.PROTECT`), e relações de Muitos-para-Muitos (`ManyToManyField`).
* **Painel Administrativo Customizado:** Configuração do Django Admin atuando como um sistema de backoffice totalmente funcional para cadastro, filtro e gestão manual da frota e das entregas.
* **Manipulação via Shell:** Criação e consulta de registros utilizando o ORM diretamente via linha de comando.

---

## Roadmap
O sistema está sendo construído em fases incrementais. Os próximos passos transformarão o painel atual em uma API completa e escalável.

* [x] **Fase 1: Base de Dados e Backoffice** (Atual)
* [x] **Fase 2: API RESTful (Django Rest Framework)**
  * Criação de Serializers para conversão de dados em JSON.
  * Desenvolvimento de endpoints (GET, POST, PATCH, DELETE) para comunicação com aplicações front-end/mobile.
  * Autenticação e permissões de usuários (JWT/Token).
* [ ] **Fase 3: Consultas Avançadas em SQL**
  * Criação de rotas gerenciais baseadas em instruções SQL brutas (PostgreSQL) para relatórios complexos de performance de motoristas e frotas.
* [ ] **Fase 4: Tarefas Assíncronas (Celery + Redis)**
  * Implementação de filas de processamento.
  * Integração com bot do Telegram: disparo de notificações automáticas e assíncronas para o cliente sempre que o status de um pacote mudar para "Entregue".
* [ ] **Fase 5: Infraestrutura e Deploy**
  * Migração do banco local (SQLite) para o definitivo corporativo (PostgreSQL).
  * Empacotamento de toda a aplicação (Django, BD, Redis e Celery) utilizando **Docker** e `docker-compose`.

---

## Stack Tecnológica (Prevista)
* **Linguagem:** Python 3
* **Framework Web:** Django
* **API Framework:** Django Rest Framework (DRF)
* **Banco de Dados:** SQLite (Desenvolvimento) ➡️ PostgreSQL (Produção)
* **Tarefas Assíncronas:** Celery + Redis
* **Infraestrutura:** Docker

---
