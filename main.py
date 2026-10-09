from web3 import Web3

# Conexão com o nó RPC do Ganache local
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.eth.default_account = w3.eth.accounts[0]

CONTRACT_ADDRESS = '0xd9145CCE52D386f254917e481eB44e9943F39138'
ABI = [
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_codigo",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "_solicitante",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "_descricao",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "_prioridade",
				"type": "uint256"
			}
		],
		"name": "registrar",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "removerPrimeiro",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_codigo",
				"type": "uint256"
			}
		],
		"name": "buscar",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "chamados",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "codigo",
				"type": "uint256"
			},
			{
				"internalType": "string",
				"name": "solicitante",
				"type": "string"
			},
			{
				"internalType": "string",
				"name": "descricao",
				"type": "string"
			},
			{
				"internalType": "uint256",
				"name": "prioridade",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "proximo",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "existe",
				"type": "bool"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "fim",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "inicio",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "listarOrdem",
		"outputs": [
			{
				"internalType": "uint256[]",
				"name": "",
				"type": "uint256[]"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "quantidade",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
] #ABI gerada na compilação do Smart Contract

contrato = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

def inserir():
    cod = int(input("Código: "))
    solicitante = input("Solicitante: ")
    desc = input("Descrição: ")
    prio = int(input("Prioridade: "))
    try:
        tx_hash = contrato.functions.registrar(cod, solicitante, desc, prio).transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Chamado registrado no final da lista com sucesso.")
    except Exception as e:
        print(f"Erro ao inserir: {e}")

def listar():
    codigos = contrato.functions.listarOrdem().call()
    if not codigos:
        print("A lista de chamados está vazia.")
        return
    
    print("\n--- Fila de Chamados ---")
    for cod in codigos:
        dados = contrato.functions.buscar(cod).call()
        print(f"[{dados[0]}] {dados[1]} | {dados[2]} | Prioridade: {dados[3]} -> Próx: {dados[4]}")

def buscar():
    cod = int(input("Código para busca: "))
    try:
        dados = contrato.functions.buscar(cod).call()
        print(f"Resultado: [{dados[0]}] {dados[1]} - {dados[2]} (Prioridade {dados[3]})")
    except:
        print("Chamado não encontrado.")

def exibir_quantidade():
    qtd = contrato.functions.quantidade().call()
    print(f"Total de chamados registrados: {qtd}")

def remover():
    try:
        tx_hash = contrato.functions.removerPrimeiro().transact()
        w3.eth.wait_for_transaction_receipt(tx_hash)
        print("Primeiro chamado removido da fila e memória liberada.")
    except Exception as e:
        print(f"Erro ao remover (a lista pode estar vazia): {e}")

def main():

    print("Chain ID da rede:", w3.eth.chain_id)
    print("Bytecode no endereço:", w3.eth.get_code(CONTRACT_ADDRESS))
    while True:
        print("\n1. Registrar chamado")
        print("2. Listar chamados")
        print("3. Buscar chamado")
        print("4. Exibir quantidade")
        print("5. Remover primeiro chamado")
        print("6. Sair")
        
        opcao = input("Opção: ")
        
        if opcao == '1':
            inserir()
        elif opcao == '2':
            listar()
        elif opcao == '3':
            buscar()
        elif opcao == '4':
            exibir_quantidade()
        elif opcao == '5':
            remover()
        elif opcao == '6':
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()