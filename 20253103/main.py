import sys
from pydantic import ValidationError
from tabulate import tabulate
from contratos.contrato_repo import ContratoRepo
from contratos.contrato import Contrato
from datetime import date

def exibir_menu():
    print("\n--- Menu de Gerenciamento de Contratos ---")
    print("a) Cadastrar Contrato")
    print("b) Listar Contratos")
    print("c) Alterar Contrato")
    print("d) Excluir Contrato")
    print("e) Sair")
    print("-----------------------------------------")

def obter_entrada_usuario(mensagem, tipo=str):
    while True:
        entrada = input(mensagem)
        try:
            if tipo == float:
                return float(entrada)
            elif tipo == int:
                return int(entrada)
            elif tipo == date:
                return date.fromisoformat(entrada)
            else:
                return entrada.strip()
        except ValueError:
            print(f"Entrada inválida. Por favor, insira um valor do tipo '{tipo.__name__}'.")

def cadastrar_contrato(repo: ContratoRepo, valor, data_inicio, data_fim, requisitos):
    try:
        novo_contrato = Contrato(valor=valor, data_inicio=data_inicio, data_fim=data_fim, requisitos=requisitos)
        contrato_id = repo.adicionar(novo_contrato)

        if contrato_id:
            print(f"Contrato cadastrado com sucesso! ID: {contrato_id}")
        else:
            print("Falha ao cadastrar o contrato.")

    except ValidationError as e:
        print("\nErro de validação ao cadastrar contrato:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao cadastrar: {e}")

def listar_contratos(repo: ContratoRepo):
    contratos = repo.obter_todos()

    if contratos:
        tabela = [[c.id, c.valor, c.data_inicio, c.data_fim, c.requisitos] for c in contratos]
        cabecalhos = ["ID", "Valor", "Data de Início", "Data de Fim", "Requisitos"]
        print(tabulate(tabela, headers=cabecalhos, tablefmt="grid"))
    else:
        print("Nenhum contrato cadastrado.")

def alterar_contrato(repo: ContratoRepo, contrato_id, valor, data_inicio, data_fim, requisitos):
    try:
        contrato_existente = repo.obter(contrato_id)

        if contrato_existente:
            contrato_atualizado = Contrato(id=contrato_id, valor=valor, data_inicio=data_inicio, data_fim=data_fim, requisitos=requisitos)

            if repo.atualizar(contrato_atualizado):
                print(f"Contrato ID {contrato_id} atualizado com sucesso!")
            else:
                print(f"Falha ao atualizar o contrato ID {contrato_id}.")

        else:
            print(f"Contrato com ID {contrato_id} não encontrado.")

    except ValidationError as e:
        print("\nErro de validação ao alterar contrato:")
        for error in e.errors():
            print(f"- Campo '{error['loc'][0]}': {error['msg']}")
    except ValueError:
        print("Entrada inválida para ID, valor ou data. A alteração foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao alterar: {e}")

def excluir_contrato(repo: ContratoRepo, contrato_id):
    try:
        contrato = repo.obter(contrato_id)
        if not contrato:
             print(f"Contrato com ID {contrato_id} não encontrado.")
             return

        confirmacao = input(f"Tem certeza que deseja excluir o contrato (ID: {contrato_id})? (s/N): ").lower()

        if confirmacao == 's':
            if repo.excluir(contrato_id):
                print(f"Contrato ID {contrato_id} excluído com sucesso.")
            else:
                print(f"Falha ao excluir o contrato ID {contrato_id}. Pode já ter sido removido.")
        else:
            print("Exclusão cancelada.")

    except ValueError:
        print("ID inválido. A exclusão foi cancelada.")
    except Exception as e:
        print(f"\nOcorreu um erro inesperado ao excluir: {e}")

def main():
    repo = ContratoRepo()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").lower().strip()

        if opcao == 'a':
            valor = input("Valor: ")
            data_inicio = input("Data de Início (AAAA-MM-DD): ")
            data_fim = input("Data de Fim (AAAA-MM-DD): ")
            requisitos = input("Requisitos: ")
            cadastrar_contrato(repo, float(valor), date.fromisoformat(data_inicio), date.fromisoformat(data_fim), requisitos)
        elif opcao == 'b':
            listar_contratos(repo)
        elif opcao == 'c':
            try:
                contrato_id = input("ID do contrato a ser alterado: ")
                valor = input("Novo Valor: ")
                data_inicio = input("Nova Data de Início (AAAA-MM-DD): ")
                data_fim = input("Nova Data de Fim (AAAA-MM-DD): ")
                requisitos = input("Novos Requisitos: ")
                alterar_contrato(repo, int(contrato_id), float(valor), date.fromisoformat(data_inicio), date.fromisoformat(data_fim), requisitos)
            except ValueError:
                print("Formato de data inválido. Use AAAA-MM-DD.")
        elif opcao == 'd':
            contrato_id = input("ID do contrato a ser excluído: ")
            excluir_contrato(repo, int(contrato_id))
        elif opcao == 'e':
            print("Saindo do programa. Até logo!")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()
