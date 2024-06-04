# Projeto de Gerenciamento de Produtos
## Descrição

Este projeto é um sistema de gerenciamento de produtos, onde é possível cadastrar patos e clientes, registrar vendas, e gerar relatórios. O objetivo é facilitar o rastreamento e a gestão dos produtos, bem como as transações de venda, oferecendo uma visão clara e organizada do estoque e das vendas realizadas.

## Objetivos

- Facilitar o cadastro e gerenciamento de patos.
- Permitir o registro e a administração de clientes.
- Registrar as vendas de produtos, aplicando descontos quando necessário.
- Listar patos vendidos e gerar relatórios de gerenciamento.

## Funcionalidades

1. **Cadastro de Patos:**
   - Cada pato pode ser cadastrado individualmente.
   - Durante o cadastro, é possível indicar a "mãe" de cada pato para melhor rastreamento.

2. **Cadastro de Clientes:**
   - Clientes podem ser cadastrados no sistema.
   - Cada cliente pode ser marcado como elegível para desconto ou não.

3. **Venda:**
   - É possível registrar a venda de um ou mais patos para um cliente cadastrado.
   - Se o cliente for elegível para desconto, aplica-se um desconto de 20% no valor total da venda.
   - A data da venda é registrada automaticamente.

4. **Listagem de Patos Vendidos:**
   - O sistema permite a listagem de todos os patos vendidos, incluindo a data da venda e o cliente.

5. **Geração de Relatórios:**
   - É possível gerar relatórios de gerenciamento de patos em dois formatos: Excel e PDF.
   - Os relatórios incluem informações detalhadas sobre os patos cadastrados, patos vendidos e as respectivas transações.

## Tecnologias Utilizadas

- **Flask**: Framework web utilizado para construir a API.
- **SQLAlchemy**: ORM utilizado para interagir com o banco de dados.
- **SQLite**: Banco de dados utilizado para armazenamento dos dados.
- **Pandas**: Biblioteca utilizada para manipulação e geração de relatórios em Excel.
- **Unittest**: Biblioteca de testes utilizada para garantir a funcionalidade do sistema.

---

# Product Management System
## Description
This project is a product management system where you can register ducks and clients, record sales, and generate reports. The objective is to facilitate the tracking and management of products, as well as sales transactions, offering a clear and organized view of inventory and completed sales.

## Objectives
Facilitate the registration and management of ducks.
Enable the registration and management of clients.
Record product sales, applying discounts when necessary.
List sold ducks and generate management reports.

## Features
1. Duck Registration:

    - Each duck can be registered individually.
    - During registration, it is possible to indicate the "mother" of each duck for better tracking.

2. Client Registration:

    - Clients can be registered in the system.
    - Each client can be marked as eligible for a discount or not.

3. Sales:

    - It is possible to record the sale of one or more ducks to a registered client.
    - If the client is eligible for a discount, a 20% discount is applied to the total sale value.
    - The sale date is recorded automatically.

4. List of Sold Ducks:

    - The system allows listing all sold ducks, including the sale date and the client.

5. Report Generation:

    - It is possible to generate duck management reports in two formats: Excel and PDF.
    - The reports include detailed information about registered ducks, sold ducks, and their respective transactions.

## Technologies Used
- **Flask:** Web framework used to build the API.
- **SQLAlchemy:** ORM used to interact with the database.
- **SQLite:** Database used for data storage.
- **Pandas:** Library used for data manipulation and generating Excel reports.
- **Unittest:** Testing framework used to ensure system functionality.
