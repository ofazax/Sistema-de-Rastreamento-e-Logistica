# 🚚 Sistema de Rastreamento e Logística (SRL)

![Banner do Projeto](https://github.com/ofazax/Sistema-de-Rastreamento-e-Logistica/blob/main/img/image.png?raw=true)

> **Descrição:** Um sistema completo de gerenciamento de logística e entregas, desenvolvido em Python e MSSQL. O projeto modela e implementa um banco de dados robusto para otimizar operações de entrega, desde o cadastro de entidades até o rastreamento de produtos em tempo real.

---

## 🎯 Sobre o Projeto

Este projeto foi desenvolvido como parte da disciplina de **Banco de Dados**. O objetivo era criar um sistema de software funcional sobre um modelo de dados relacional normalizado, capaz de gerenciar toda a operação de uma empresa de entregas domiciliares. A aplicação permite a interação com o banco de dados através de uma interface de terminal.

---

## ✨ Funcionalidades Principais

* **Controle de Acesso:** Sistema de login seguro com hashing de senhas e diferentes perfis de usuário (Admin, Cliente, Funcionário).
* **Gerenciamento Completo (CRUD):** Interface de administrador para gerenciar todas as entidades do sistema: Pessoas, Clientes, Funcionários, Veículos, Sedes e Produtos.
* **Normalização de Dados:** O modelo implementa uma estrutura de dados normalizada, separando `Pessoa` de `Cliente` e `Funcionário` para evitar redundância e garantir a integridade dos dados.
* **Self-Service para Clientes:** Novos clientes podem se cadastrar diretamente pela aplicação, que gerencia a criação de registros de Pessoa, Endereço, Cliente e Usuário de forma transacional.
* **Rastreamento de Pedidos:** Clientes podem rastrear seus pedidos utilizando um código único, com segurança para garantir que apenas partes autorizadas vejam os detalhes.
* **Gerenciamento de Carregamentos:** Lógica para associar múltiplos produtos a um veículo para uma entrega, respeitando a capacidade de carga.

---

## 🛠️ Modelo de Dados e Tecnologias

O projeto utiliza um banco de dados relacional hospedado no **Azure SQL**. O esquema foi cuidadosamente projetado, como detalhado no documento de análise (`/docs/Documentação_Sistema_Logística.pdf`), que inclui os modelos Entidade-Relacionamento e Relacional.

* **Linguagem:** **Python 3**
* **Banco de Dados:** **Microsoft SQL Server** (no Azure)
* **Bibliotecas Python:** `pyodbc` (conexão com BD), `python-dotenv` (segurança de credenciais), `hashlib`, `getpass`.
* **Script de Criação:** O banco de dados pode ser totalmente recriado usando o arquivo `sql/script.sql`.

---

## 🚀 Como Executar o Projeto

Para executar a aplicação localmente, siga os passos abaixo.

**Pré-requisitos:**
* Python 3.8+
* `pip` (gerenciador de pacotes do Python)
* Driver ODBC 18 para SQL Server instalado.

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/ofazax/Sistema-de-Rastreamento-e-Logistica.git
    cd Sistema-de-Rastreamento-e-Logistica
    ```

2.  **Instale as dependências:**
    ```bash
    pip install pyodbc python-dotenv
    ```

3.  **Configure as variáveis de ambiente:**
    * Renomeie o arquivo `config.example.env` para `config.env`.
    * Abra o arquivo `config.env` e preencha com as suas credenciais do banco de dados.

4.  **Execute a aplicação:**
    ```bash
    python app.py
    ```

---

## 👨‍💻 Autores

* Arthur Victor L. de M. Alves¹
* Brunno Enrico Machado Costa²
* Diogo Meireles Ribeiro³
* Vitória Rani Santos Menezes⁴
