#importamos as funções que criamos no nosso outro arquivo
from funcoes import processar_produtos, processar_pedidos

def main():
    print("Iniciando o pipeline da sanitização da Olist...\n")

    # nomes dos arquivos
    arq_produtos = 'olist_products_dataset.csv'
    arq_pedidos = 'olist_orders_dataset.csv'

    # 1. processando produtos
    print("processando tabela de produtos...")
    linhas_prod, nulos_corrigidos, produtos_limpos = processar_produtos(arq_produtos)

    #2 processando pedidos
    print("processando tabela de pedidos...")
    linhas_ped, cancelados_total, entregas_vazias, vazias_e_canceladas, hipotese = processar_pedidos(arq_pedidos)

    # 3. sumario estatistico manual (relatorio)
    print("\n" + "="*40)
    print("Relatorio de Status de sanitização")
    print("="*40)
    print(f"-> Total de linhas lidas (produtos): {linhas_prod}")
    print(f"->Nulos corrigidos (categorias sem nome): {nulos_corrigidos}")
    print("-" *40)
    print(f"-> Total de linhas lidas (Pedidos): {linhas_ped}")
    print(f"-> Total de pedidos com status 'Canceled': {cancelados_total}")
    print("\n ANÁLISE DA HIPÓTESE DA DIRETORIA:")
    print("A diretoria achou que datas de entrega vazias eram obrigatoriamente de pedidos cancelados.")
    print(f"Total de datas de entrega vazias encontradas: {entregas_vazias}")
    print(f"Desses, quantos realmente estavam cancelados?: {vazias_e_canceladas}")

    if hipotese:
         print(">> Conclusão: hipotese confirmada. Todas as datas vazias são de pedidos cancelados ")
    else:
         print(">> Conclusção: Hipotese refutada. Existem pedidos com datas de entraga vazia que Não estão cancelados (ex: status 'invoiced' ou 'shipped').")

# Isso garante que o script só rode se for chamado diretamente
if __name__ == "__main__":
    main()