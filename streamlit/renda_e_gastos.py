import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
from fbprophet import Prophet
from datetime import datetime


def get_last_day_of_month(month):
    if month == 2:
        return 28
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30


month_names = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril", 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
               9: "Setembro",
               10: "Outubro", 11: "Novembro", 12: "Dezembro"}

st.sidebar.title("Explorador de receitas e gastos")

today_dt = datetime.today()
today_month = today_dt.month
today_year = today_dt.year

# Utilizamos o DataFrame de receitas apenas para carregar as cidades
receitas_df = pd.read_csv("../data/generated/receitas-timeseries.csv", encoding="iso-8859-9")
despesas_df = pd.read_csv("../data/generated/despesas-timeseries.csv", encoding="iso-8859-9")
cities_list = list(pd.unique(receitas_df['ds_municipio']))
cities_list = [city.encode('iso-8859-9').decode() for city in cities_list]
city = st.sidebar.selectbox('Escolha a sua cidade:', cities_list)
data_type = st.sidebar.radio("Tipo de dados", ("Atual", "Previsão"))

# Mostramos a situação atual dos gastos
if data_type == "Atual":
    atual_button_run = st.sidebar.button("Continuar")
    if atual_button_run:
        receitas_year_df = receitas_df[
            (receitas_df.ds_municipio.apply(lambda x: x.encode('iso-8859-9').decode()) == city) & (
                        receitas_df.ano_exercicio == today_year)]
        receitas_year_df['vl_arrecadacao'] = receitas_year_df['vl_arrecadacao'].apply(lambda x: x / 1000000)

        despesas_year_df = despesas_df[
            (despesas_df.ds_municipio.apply(lambda x: x.encode('iso-8859-9').decode()) == city) & (
                        despesas_df.ano_exercicio == today_year)]
        despesas_year_df['vl_despesa'] = despesas_year_df['vl_despesa'].apply(lambda x: x / 1000000)

        rounded_despesas = round(despesas_year_df.sum()["vl_despesa"] / 100, 3)
        rounded_receitas = round(receitas_year_df.sum()["vl_arrecadacao"] / 100, 3)

        st.markdown(
            f'Para a cidade de {city}, as receitas até agora no ano de {today_year} foram de **R${rounded_receitas} milhões.**')
        st.markdown(f'Já as despesas já somam **R${rounded_despesas} milhões**.')

        deficit = (rounded_receitas - rounded_despesas) < 0

        st.markdown(
            f"O {'déficit' if deficit else 'superávit'} atual é de **R${abs(round(rounded_receitas - rounded_despesas, 3))} milhões**.")

        st.header('Receitas:')

        ax = sns.barplot(x='mes_referencia', y='vl_arrecadacao', data=receitas_year_df, capsize=.2, color="green")
        ax.set(xlabel="Mês", ylabel="Arrecadação (milhões R$)")
        st.pyplot(plt)

        plt.clf()

        st.header('Despesas:')

        ax = sns.barplot(x='mes_referencia', y='vl_despesa', data=despesas_year_df, capsize=.2, color="red")
        ax.set(xlabel="Mês", ylabel="Despesas (milhões R$)")
        st.pyplot(plt)
# Mostramos a previsão de gastos até o final do ano
else:
    n_periods = st.sidebar.slider(
        f"Número de próximos meses para previsão (o dado mais recente é de {month_names[int(receitas_df.tail(1)['mes_referencia'])]} de {today_year})",
        12 - (today_month - 2), 12)
    previsao_button_run = st.sidebar.button("Continuar")
    if previsao_button_run:
        model_receitas_df = receitas_df.copy()
        model_receitas_df = model_receitas_df[
            receitas_df.ds_municipio.apply(lambda x: x.encode('iso-8859-9').decode()) == city]
        model_receitas_df['ds'] = pd.to_datetime(
            model_receitas_df.ano_exercicio * 10000 + model_receitas_df.mes_referencia * 100 + model_receitas_df.mes_referencia.apply(
                get_last_day_of_month), format='%Y%m%d')
        model_receitas_df['y'] = model_receitas_df['vl_arrecadacao']

        m1 = Prophet(interval_width=0.95, seasonality_mode='multiplicative')
        m1.fit(model_receitas_df[['ds', 'y']])
        future = m1.make_future_dataframe(periods=n_periods, freq='M')
        fcst = m1.predict(future)

        current_receitas_sum = sum(model_receitas_df[model_receitas_df.ano_exercicio == today_year]['vl_arrecadacao'])
        forecasted_receitas_sum = sum(fcst[fcst.ds.dt.year == today_year]['yhat'])
        receitas_predicted = current_receitas_sum + forecasted_receitas_sum

        model_despesas_df = despesas_df.copy()
        model_despesas_df = model_despesas_df[
            despesas_df.ds_municipio.apply(lambda x: x.encode('iso-8859-9').decode()) == city]
        model_despesas_df['ds'] = pd.to_datetime(
            model_despesas_df.ano_exercicio * 10000 + model_despesas_df.mes_referencia * 100 + model_despesas_df.mes_referencia.apply(
                get_last_day_of_month), format='%Y%m%d')
        model_despesas_df['y'] = model_despesas_df['vl_despesa']

        m2 = Prophet(interval_width=0.95, seasonality_mode='multiplicative')
        m2.fit(model_despesas_df[['ds', 'y']])
        future2 = m2.make_future_dataframe(periods=n_periods, freq='M')
        fcst2 = m2.predict(future2)

        current_despesas_sum = sum(model_despesas_df[model_despesas_df.ano_exercicio == today_year]['vl_despesa'])
        forecasted_despesas_sum = sum(fcst2[fcst2.ds.dt.year == today_year]['yhat'])
        despesas_predicted = current_despesas_sum + forecasted_despesas_sum

        st.markdown(
            f"Para o ano de {today_year}, a previsão de **receitas totais** é de **R${round(receitas_predicted / 1000000, 3)} milhões**.")
        st.markdown(f"Já a previsão de **despesas totais** é de **R${round(despesas_predicted / 1000000, 3)} milhões**.")

        if despesas_predicted > receitas_predicted:
            st.markdown(
                f"# ALERTA! Parece que sua tendência para o ano de {today_year} é fechar no vermelho. Tome cuidado com suas contas!")
        else:
            st.markdown(f"# PARABÉNS! Você está no caminho certo para fechar {today_year} com as contas em dia!")

        st.write("\nA previsão solicitada se encontra a seguir:")

        st.header("Receitas")
        fcst['mes'] = fcst.ds.apply(lambda x: pd.to_datetime(x).month)
        fcst['ano'] = fcst.ds.apply(lambda x: pd.to_datetime(x).year)
        st.table(
            fcst[['mes', 'ano', 'yhat']].rename(columns={'mes': 'Mês', 'ano': 'Ano', 'yhat': 'Receita prevista'}).tail(
                n_periods))
        fig = m1.plot(fcst)
        st.pyplot(fig)

        st.header("Despesas")
        fcst2['mes'] = fcst2.ds.apply(lambda x: pd.to_datetime(x).month)
        fcst2['ano'] = fcst2.ds.apply(lambda x: pd.to_datetime(x).year)
        st.table(
            fcst2[['mes', 'ano', 'yhat']].rename(columns={'mes': 'Mês', 'ano': 'Ano', 'yhat': 'Receita prevista'}).tail(
                n_periods))
        fig2 = m2.plot(fcst2)
        st.pyplot(fig2)
