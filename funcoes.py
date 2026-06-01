import csv
import re
from datetime import datetime

####### função 1: Limpeza de Texto 

def limpar_categoria(categoria):
    """
    Recebe o nome da categoria, converte para minúsculo, remove espaços extras e usa Regex para tirar caracteres especiais.
    """
    # Se a categoria for vazia, aplicamos a regra de negocio
    if not categoria or categoria.strip() == "":
        return "sem categoria"
    
    # .lower() deixa tudo minusculo. .strip() tira espaços do começo e fim
    categoria_limpa = categoria.lower().strip()

    # re.sub é o nosso "substituidor"
    # [^\w\s] significa: "tudo que NÃO (^) for letra/numero (\w) ou espaço (\s)"
    # ele pega esses caracteres estranhos e troca por nada ('')
    categoria_limpa = re.sub(r'[^\w\s]','',categoria_limpa)

    return categoria_limpa

####### função 2 : Processamento de produtos

def processar_produtos(caminho_arquivo):
    """
    Lê o arquivo de produtos, limpa as categorias e lida com dados ausentes
    """
    linhas_processadas = 0
    nulos_corrigidos = 0
    produtos_validos = []

    # 'with open' garante que o arquivo será fechado automaticamente depois de usa-lo.
    # 'utf-8' é o padrao de codificação de texto.
    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        # DictReader transforma cada linha num dicionario, onde a chave é o nome da coluna
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            linhas_processadas += 1

            # 1. tratamento da categoria
            categoria_original = linha['product_category_name']
            categoria_nova = limpar_categoria(categoria_original)
            
            if categoria_nova == "sem categoria":
                nulos_corrigidos += 1
            linha['product_category_name'] = categoria_nova

            # 2. Tratamento das dimensoes (regra de corte)
            # decisão tecnica : se o peso ou dimensões forem nulos/vazios, vamos descartar o registro.
            # justificativa: atribuir média exigiria ler o arquivo duas vezes (uma para calcular, outra para preencher).
            # Colocar "0" estragaria modelos de calculo de frete da Olist. Descartar é mais seguro aqui.
            if not linha['product_weight_g'] or not linha['product_length_cm']:
                continue # o 'continue' pula para a proxima linha do 'for', descartando esta.
            
            produtos_validos.append(linha)

    return linhas_processadas, nulos_corrigidos, produtos_validos
    
####### função 3: Formatação de Datas

def formatar_data(data_string):
    """
    Converte a data de 'YYYY-MM-DD HH:MM:SS' para 'DD/MM/YYYY'.
    """
    if not data_string or data_string.strip() == "":
       return ""
    
    try:
        # strptime: Transforma a String num objeto DATETIME(ele entende o que é ano,mes,dia)
        data_obj = datetime.strptime(data_string, "%Y-%m-%d %H:%M:%S")
        # strftime: transforma o DATETIME de volta em string, mas no formato brasileiro
        return data_obj.strftime("%d/%m/%Y")
    except ValueError:
        # se a data vier num formato inesperado, retornamos como estava
        return data_string
    
######## função 4: Processamento de Pedidos (regra de Negocio)

def processar_pedidos(caminho_arquivo):
    """
    Lê o arquivo de pedidos, formata datas e testa a hipotese da diretoria.
    """
    linhas_processadas = 0
    datas_entrega_vazias = 0
    vazias_e_canceladas = 0
    pedidos_cancelados_total = 0

    with open(caminho_arquivo, mode='r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            linhas_processadas += 1

            # formatando a data de aprovação
            linha['order_approved_at'] = formatar_data(linha['order_approved_at'])

            status = linha['order_status'].strip().lower()
            data_entrega = linha['order_delivered_customer_date'].strip()

            # contando cancelados no geral
            if status == "canceled":
                pedidos_cancelados_total += 1

            # testando a hipotese da diretoria (if/elif/else)
            if data_entrega == "":
                datas_entrega_vazias += 1
                if status == "canceled":
                    vazias_e_canceladas += 1
                elif status != "canceled":
                    # aqui percebemos se a hipotese da diretoria é funcional ou não
                    pass
                else:
                    pass

    # verifica a hipotese: a data nula ocorre OBRIGATORIAMENTE por causa de cancelamento?
    # Note que agora essas linhas tem 4 espaços antes delas!
    hipotese_comprovada = (datas_entrega_vazias == vazias_e_canceladas) and (datas_entrega_vazias > 0)

    return linhas_processadas, pedidos_cancelados_total, datas_entrega_vazias, vazias_e_canceladas, hipotese_comprovada