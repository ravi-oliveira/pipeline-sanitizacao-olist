 # Pipeline de Sanitização de Dados - Olist

## Descrição do Projeto
A equipe de Engenharia de Dados da Olist extraiu lotes de dados do banco oficial (`olist_products_dataset.csv` e `olist_orders_dataset.csv`), porém foram identificadas inconsistências, como valores nulos, categorias fora do padrão e hipóteses de negócio pendentes de validação. 

O objetivo deste projeto é construir um script em Python (utilizando apenas bibliotecas nativas) para realizar a limpeza (sanitização) desses dados. O pipeline corrige nomenclaturas, descarta registros incompletos e formata padrões de data, garantindo que as informações fiquem prontas e confiáveis para geração de relatórios automatizados.

## Guia de Execução
Para testar e rodar o código localmente, siga os passos:
1. Certifique-se de ter o **Python** instalado em sua máquina.
2. Coloque os dois arquivos de base de dados (`olist_products_dataset.csv` e `olist_orders_dataset.csv`) na mesma pasta onde estão os scripts.
3. Abra o seu terminal (ou prompt de comando) e navegue até a pasta do projeto.
4. Execute o arquivo principal com o comando:
   `python main.py`
5. O console exibirá o relatório estatístico da limpeza e a validação da hipótese de negócio da diretoria.

## Reflexão Teórica: Limpeza de Dados e Machine Learning
Aplicar uma lógica de programação estruturada para a limpeza correta dos dados é o primeiro e mais vital passo antes de treinar modelos de Inteligência Artificial. Se alimentarmos um modelo com dados sujos (como categorias vazias, caracteres especiais criando "categorias duplicadas" falsas, ou datas mal formatadas), a máquina aprenderá sobre um cenário irreal, fenômeno conhecido como *Garbage In, Garbage Out*. 

Garantir que os dados representem a realidade e estejam balanceados ajuda a evitar o **Viés** (onde o modelo discrimina ou favorece um padrão de forma incorreta por dados falhos) e o **Overfitting** (quando o modelo "decora" ruídos do dataset em vez de aprender as regras de negócio reais, perdendo a capacidade de prever novos dados corretamente). Um dado bem sanitizado é o pilar de uma IA generalizável e ética.