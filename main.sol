// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract FilaChamados {
    struct Chamado {
        uint codigo;
        string solicitante;
        string descricao;
        uint prioridade;
        uint proximo; // Atua como ponteiro. 0 indica NULL/None.
        bool existe;
    }

    mapping(uint => Chamado) public chamados;
    uint public inicio;
    uint public fim;
    uint public quantidade;

    // 1. Registrar um chamado no final da lista
    function registrar(uint _codigo, string memory _solicitante, string memory _descricao, uint _prioridade) public {
        require(!chamados[_codigo].existe, "Codigo ja existe");
        require(_codigo > 0, "Codigo deve ser maior que zero (0 eh NULL)");

        // Cria o nó de forma equivalente à alocação dinâmica
        chamados[_codigo] = Chamado(_codigo, _solicitante, _descricao, _prioridade, 0, true);

        if (inicio == 0) {
            inicio = _codigo;
            fim = _codigo;
        } else {
            chamados[fim].proximo = _codigo;
            fim = _codigo;
        }
        quantidade++;
    }

    // 3. Buscar um chamado pelo código
    function buscar(uint _codigo) public view returns (uint, string memory, string memory, uint, uint) {
        require(chamados[_codigo].existe, "Chamado nao encontrado");
        Chamado memory c = chamados[_codigo];
        return (c.codigo, c.solicitante, c.descricao, c.prioridade, c.proximo);
    }

    // 5. Remover o primeiro chamado
    function removerPrimeiro() public {
        require(inicio != 0, "Lista vazia"); // Testa lista vazia
        uint codigoRemovido = inicio;

        // Atualiza o início para o próximo elemento
        inicio = chamados[inicio].proximo;
        
        // Libera a "memória" do nó removido
        delete chamados[codigoRemovido];
        quantidade--;

        // Trata a remoção do único elemento existente
        if (inicio == 0) {
            fim = 0;
        }
    }

    // Função auxiliar para percorrer a lista
    function listarOrdem() public view returns (uint[] memory) {
        uint[] memory ordem = new uint[](quantidade);
        uint atual = inicio;
        uint i = 0;
        
        // Percorre a lista até encontrar 0 (NULL)
        while (atual != 0) {
            ordem[i] = atual;
            atual = chamados[atual].proximo;
            i++;
        }
        return ordem;
    }
}
