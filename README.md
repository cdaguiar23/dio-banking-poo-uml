# Sistema Bancário Simples em Python

Este projeto é uma simulação de um sistema bancário básico desenvolvido em Python, utilizando conceitos de Programação Orientada a Objetos (POO). Ele permite gerenciar clientes e suas contas correntes através de um menu interativo no terminal.

## Funcionalidades

-   **Gestão de Clientes:**
    -   Criação de novos clientes (Pessoa Física) com nome, CPF, data de nascimento e endereço.
-   **Gestão de Contas Correntes:**
    -   Criação de contas vinculadas a um cliente.
    -   Definição de um **limite de crédito (cheque especial)** para cada conta.
    -   Definição de um **limite de saques** para cada conta.
-   **Operações Bancárias:**
    -   **Depósito:** Adicionar fundos a uma conta.
    -   **Saque:** Retirar fundos de uma conta, respeitando o saldo, o limite de crédito e o número máximo de saques.
    -   **Transferência:** Mover fundos entre duas contas.
-   **Consultas:**
    -   **Resumo da Conta:** Visualização rápida do saldo, limite de crédito e contagem de saques.
    -   **Extrato:** Exibição detalhada de todas as transações realizadas na conta.

## Como Executar

Para rodar o sistema, você precisa ter o Python 3 instalado.

1.  Salve o código em um arquivo chamado `desafio.py`.
2.  Abra um terminal ou prompt de comando.
3.  Navegue até o diretório onde você salvou o arquivo.
4.  Execute o seguinte comando:

    ```bash
    python desafio.py
    ```

5.  O menu interativo será exibido, e você poderá escolher as opções digitando o número correspondente.

## Estrutura do Código

O código está organizado utilizando os seguintes princípios de POO:

-   **`Cliente` / `PessoaFisica`**: Classes responsáveis por modelar os clientes do banco.
-   **`Conta` / `ContaCorrente`**: Classes que representam as contas bancárias. A `ContaCorrente` herda de `Conta` e adiciona funcionalidades específicas, como limite de crédito e de saques.
-   **`Historico`**: Classe que armazena a lista de transações de uma conta.
-   **`Transacao` (Abstrata)**: Classe base para todas as operações financeiras.
-   **`Deposito`, `Saque`, `Transferencia`**: Classes que herdam de `Transacao` e implementam a lógica específica para cada tipo de operação, demonstrando o uso de polimorfismo.
-   **`menu()`**: Função principal que controla o fluxo do programa e a interação com o usuário.

