import re
from datetime import datetime
from unicodedata import normalize

import matplotlib.pyplot as plt
import nltk
import streamlit as st
import pandas as pd
from wordcloud import WordCloud

ods_11_1 = ['habitação', 'habitacao', 'habitacional', 'favelas',
            'urbano', 'urbanização', 'urbanismo', 'urbanizacao', 'favela', 'básicos']
ods_11_2 = ['transporte', 'metrô', 'metro', 'onibus', 'ônibus', 'trem',
            'vlt', 'monotrilho', 'bonde', 'frota', 'trens', 'transportes']
ods_11_3 = ['sustentável', 'sustentavel', 'sustentabilidade', 'participativo', 'participativa',
            'assentamentos']
ods_11_4 = ['partimônio', 'cultura', 'restauração', 'patrimonio', 'restauracao', 'reserva',
            'natural', 'natureza', 'cultural', 'patrimonial', 'meio-ambiente']
ods_11_5 = ['mortalidade', 'catástrofe', 'catastrofe', 'catástrofes', 'catastrofes', 'acidente',
            'acidentes', 'enchentes', 'enchente', 'deslizamento', 'desastre', 'desastres', 'chuva',
            'chuvas', 'barragem', 'contaminação', 'despoluição', 'contaminacao', 'despoulicao',
            'contaminado', 'contaminada']
ods_11_6 = ['ar', 'poluição', 'resíduos', 'poluicao', 'residuos', 'esgoto', 'esgotos', 'saneamento',
            'coleta', 'lixo', 'lixão', 'lixao', 'lixoes', 'lixões', 'aterro', 'aterros', 'reciclagem',
            'reciclado', 'recicla', 'descarte']
ods_11_7 = ['espaço', 'espaco', 'acessível', 'acessibilidade', 'convivência', 'convivencia', 'conviver',
            'acessivel', 'cadeirante', 'cego', 'deficiente', 'deficientes', 'deficiencia', 'deficiência',
            'idoso', 'idosos', 'idosa', 'mulher', 'mulheres', 'verde', 'verdes']
ods_11_a = ['rural', 'campo', 'periurbana']
ods_11_b = ['eficiência', 'eficiencia', 'clima', 'climático', 'climatico', 'aquecimento', 'sendai']
ods_11_c = []

ods_11_1_text = "**11.1** Até 2030, garantir o acesso de todos a habitação segura, adequada e a preço acessível, e aos serviços básicos e urbanizar as favelas"
ods_11_2_text = "**11.2** Até 2030, proporcionar o acesso a sistemas de transporte seguros, acessíveis, sustentáveis e a preço acessível para todos, melhorando a segurança rodoviária por meio da expansão dos transportes públicos, com especial atenção para as necessidades das pessoas em situação de vulnerabilidade, mulheres, crianças, pessoas com deficiência e idosos"
ods_11_3_text = "**11.3** Até 2030, aumentar a urbanização inclusiva e sustentável, e a capacidade para o planejamento e a gestão participativa, integrada e sustentável dos assentamentos humanos, em todos os países"
ods_11_4_text = "**11.4** Fortalecer esforços para proteger e salvaguardar o patrimônio cultural e natural do mundo"
ods_11_5_text = "**11.5** Até 2030, reduzir significativamente o número de mortes e o número de pessoas afetadas por catástrofes e diminuir substancialmente as perdas econômicas diretas causadas por elas em relação ao produto interno bruto global, incluindo os desastres relacionados à água, com o foco em proteger os pobres e as pessoas em situação de vulnerabilidade"
ods_11_6_text = "**11.6** Até 2030, reduzir o impacto ambiental negativo per capita das cidades, inclusive prestando especial atenção à qualidade do ar, gestão de resíduos municipais e outros"
ods_11_7_text = "**11.7** Até 2030, proporcionar o acesso universal a espaços públicos seguros, inclusivos, acessíveis e verdes, em particular para as mulheres e crianças, pessoas idosas e pessoas com deficiência"
ods_11_a_text = "**11.a** Apoiar relações econômicas, sociais e ambientais positivas entre áreas urbanas, periurbanas e rurais, reforçando o planejamento nacional e regional de desenvolvimento"
ods_11_b_text = "**11.b** Até 2020, aumentar substancialmente o número de cidades e assentamentos humanos adotando e implementando políticas e planos integrados para a inclusão, a eficiência dos recursos, mitigação e adaptação à mudança do clima, a resiliência a desastres; e desenvolver e implementar, de acordo com o Marco de Sendai para a Redução do Risco de Desastres 2015-2030, o gerenciamento holístico do risco de desastres em todos os níveis"
ods_11_c_text = "**11.c** Apoiar os países menos desenvolvidos, inclusive por meio de assistência técnica e financeira, para construções sustentáveis e robustas, utilizando materiais locais"

ods_11 = ods_11_1 + ods_11_2 + ods_11_3 + ods_11_4 + ods_11_5 + ods_11_6 + ods_11_7 + ods_11_a + ods_11_b + ods_11_c


def is_ods(txt, ods_list):
    is_ods = False
    for ods in ods_list:
        if ods in txt:
            is_ods = True
    return is_ods


# de https://wiki.python.org.br/RemovedorDeAcentos
def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def clean_city_name(txt):
    sem_acento = remover_acentos(txt)
    clean = re.sub(r'\W+', '', sem_acento)
    return clean.lower()


today_dt = datetime.today()
today_month = today_dt.month
today_year = today_dt.year

st.sidebar.title("Suas despesas e o ODS 11")

# Utilizamos o DataFrame de receitas apenas para carregar as cidades (é o mais leve, nesse caso)
receitas_df = pd.read_csv("../data/generated/receitas-timeseries.csv", encoding="iso-8859-9")
cities_list = list(pd.unique(receitas_df['ds_municipio']))
cities_list = [city.encode('iso-8859-9').decode() for city in cities_list]

city = st.sidebar.selectbox('Escolha a sua cidade:', cities_list)
top_N = st.sidebar.slider("Selecionar os principais N tópicos a avaliar", 1, 500, 200)
button_run = st.sidebar.button("Continuar")

if button_run:
    file_name = f"../data/despesas/by_city/despesas-2019-{clean_city_name(city)}.csv"
    df_csv = pd.read_csv(file_name, sep=',')
    df_csv['vl_despesa'] = df_csv['vl_despesa'].apply(lambda x: float(x.replace(",", "."))).astype(float)

    st.write(f"Vamos ver qual é a maior recorrência de gastos na sua cidade? O gráfico a seguir apresenta os {top_N}"
             f" tópicos mais presentes nas descrições das suas despesas:")

    df = df_csv.copy()
    df['historico_despesa'] = df['historico_despesa'].apply(lambda x: re.sub(r'\W+', ' ', x))
    df['historico_despesa'] = df['historico_despesa'].apply(lambda x: re.sub(r'^[a-zA-Z]+$', ' ', x))
    txt = df.historico_despesa.str.lower().str.cat(sep=' ')

    words = nltk.tokenize.word_tokenize(txt)
    word_dist = nltk.FreqDist(words)
    stopwords = nltk.corpus.stopwords.words('portuguese')
    words_except_stop_dist = nltk.FreqDist(w for w in words if w not in stopwords)
    rslt = pd.DataFrame(words_except_stop_dist.most_common(top_N),
                        columns=['Word', 'Frequency'])
    rslt = rslt[rslt.Word.str.isalpha()]

    # Liberando memória
    del txt

    cloud_dict = dict()
    for row in rslt.iterrows():
        cloud_dict[row[1]['Word']] = int(row[1]['Frequency'])
    cloud = WordCloud(background_color="white", max_font_size=40, relative_scaling=.5).fit_words(cloud_dict)
    plt.imshow(cloud)
    plt.axis("off")
    st.pyplot(plt)

    st.write("Vamos analisar como a utilização dos recursos da cidade está avançando o progresso em direção ao ODS 11.")

    rslt['ods'] = rslt['Word'].apply(lambda x: x in ods_11)
    ods_rslt = rslt[rslt.ods]
    ods_word_list = list(ods_rslt['Word'])

    st.write("Os seguintes sub-objetivos do ODS 11 foram identificados nos seus gastos:")

    ods_lists = [ods_11_1, ods_11_2, ods_11_3, ods_11_4, ods_11_5, ods_11_6, ods_11_7, ods_11_a, ods_11_b, ods_11_c]
    ods_texts = [ods_11_1_text, ods_11_2_text, ods_11_3_text, ods_11_4_text, ods_11_5_text, ods_11_6_text,
                 ods_11_7_text,
                 ods_11_a_text, ods_11_b_text, ods_11_c_text]

    idx_list = [idx for idx, ods_list in enumerate(ods_lists) for word in ods_word_list if word in ods_list]

    for idx in set(idx_list):
        st.markdown(ods_texts[idx])

    df_csv['is_ods'] = df_csv['historico_despesa'].apply(lambda x: is_ods(x, ods_word_list))
    df_ods = df_csv[df_csv.is_ods]

    ods_sum = sum(df_ods['vl_despesa'])
    total_sum = sum(df_csv['vl_despesa'])

    st.write("O gasto empenhado para o cumprimento do ODS 11 foi de:")
    st.markdown(f"# R${round(ods_sum / 1000000, 3)} milhões")

    st.write("Isso corresponde a:")
    st.markdown(f"# {round(ods_sum / total_sum, 3) * 100}% dos gastos totais")
