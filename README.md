# deephack2019

Submissão para competição [DeepHack2019](https://deephack.xyz/2019), organizada pelo USPCodeLab.

## Objetivo

O objetivo do projeto apresentado aqui é, de maneira geral, a prototipação de um Dashboard para uso do TCE-SP e das prefeituras municipais, de modo a analisar os dados brutos de contas públicas, produzidos em massa, e torná-los um pouco mais palatáveis e compreensíveis, de forma que sejam realmente úteis e possam ajudar no cumprimento da responsabilidade fiscal e do ODS 11, foco do trabalho proposto pela competição. Essa abordagem "produtizada" torna mais concreta a ideia apresentada, fazendo com que elas tentem ser mais do que meras análises abstratas, e passem a ser uma ferramenta real e interativa, que seja instrumento de trabalho para as entidades públicas envolvidas.

Devido ao grande trabalho e à natureza rápida da competição, as possíveis telas e componentes do "produto final" ideal, que seria o Dashboard se apresentam de maneiras diferentes. Seja em telas prototipadas utilizando a ferramenta de automação de ML [Streamlit](https://streamlit.io/), que apresentam uma solução mais completa e interativa, ou em Jupyter Notebooks, que elucidam mais o conceito e a evolução futura das features propostas e que não puderam ser completamente desenvolvidas. Em todos os casos, se optou por consumir os dados na forma de arquivos .csv, e não por APIs, tanto para redução de complexidade, quanto para evitar atrasos causados por latência, quanto devido ao volume massivo de dados de despesas, que dependeriam, provavelmente, do uso de um banco de dados ou solução adicional para uma leitura em velocidade satisfatória. Mudanças, reestruturações e agregações foram feitas nos arquivos quando necessário.

## Componentes

O código apresentado aqui é composto, basicamente de 3 componentes:

* Jupyter Notebooks de exploração de dados, bem como agregação e transformação de arquivos para melhorar leitura dos mesmos: _notebooks/Clusterizando cidades.ipynb_, _notebooks/Explorando dados de receitas e despesas.ipynb_ e _notebooks/Analisando despesas.ipynb_.
* Jupyter Notebooks de propostas de novas features e análises para o Dashboard, originárias de análises anteriores ou não: _notebooks/IEG-M, o ODS 11 e norteamento de políticas públicas e desafios.ipynb_ (baseado na clusterização de cidades do item anterior) e _notebooks/Uma possibilidade de melhorar o modelo de análise de despesas.ipynb_ (baseado na análise de despesas do item anterior e na tela de análise de despesas em relação ao ODS 11 dos protótipos do Dashboard).
* Prototipação de 2 telas do Dashboard, *streamlit/renda_e_gastos.py* e *streamlit/despesas_com_ods_11*.

## Setup

Por conveniência, dados provenientes de fontes externas já foram incluídos. Em seguida, para conseguir rodar o projeto deve-se seguir os seguintes passos:

* Baixar e descompactar os [dados de receitas e despesas do TCE-SP](https://transparencia.tce.sp.gov.br/conjunto-de-dados), nos respectivos diretórios: _data/despesas/_ e _data/receitas/_
* Instalar as bibliotecas necessárias para o funcionamento dos notebooks e telas do dashboard: `pip install -r requirements.txt`
* Rodar os notebooks exploratórios, que se encarregarão de gerar os novos conjuntos de dados transformados em _data/_
* Rodar as telas do dashboard: `cd streamlit` e, em seguida `streamlit run renda_e_gastos.py --server.port 2222` e `streamlit run despesaas_com_ods_11.py --server.port 2223` (garantir que sejam portas diferentes)
* Rodar notebooks de novas features/melhoramento de modelos

Obrigado!