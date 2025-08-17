import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Configuração da página
st.set_page_config(
    page_title="Análise de Triagem de Autismo",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Carregar e pré-processar os dados
@st.cache_data
def load_data():
    df = pd.read_csv("autism_screening.csv")
    # Renomear colunas para melhor legibilidade
    df = df.rename(columns={
        'Class/ASD': 'Diagnóstico',
        'age': 'Idade',
        'gender': 'Gênero',
        'ethnicity': 'Etnia',
        'jundice': 'Icterícia',
        'austim': 'Histórico Familiar de Autismo',
        'result': 'Pontuação Total'
    })
    # Converter para valores booleanos
    df['Icterícia'] = df['Icterícia'].map({'yes': 'Sim', 'no': 'Não'})
    df['Histórico Familiar de Autismo'] = df['Histórico Familiar de Autismo'].map({'yes': 'Sim', 'no': 'Não'})
    df['Diagnóstico'] = df['Diagnóstico'].map({'YES': 'Positivo', 'NO': 'Negativo'})
    return df

data_df = load_data()

# Título e descrição
st.title('Análise de Triagem de Autismo')
st.markdown("""
Esta aplicação fornece uma análise interativa dos dados de triagem de autismo.
Use os filtros na barra lateral para explorar os dados.
""")

# Sidebar com filtros
st.sidebar.header('Filtros')

gender = st.sidebar.multiselect(
    'Selecione o gênero:',
    options=data_df['Gênero'].unique(),
    default=data_df['Gênero'].unique()
)

age_range = st.sidebar.slider(
    'Selecione a faixa etária:',
    min_value=int(data_df['Idade'].min()),
    max_value=int(data_df['Idade'].max()),
    value=(int(data_df['Idade'].min()), int(data_df['Idade'].max()))
)

# Aplicar filtros
df_filtered = data_df[
    (data_df['Gênero'].isin(gender)) &
    (data_df['Idade'] >= age_range[0]) &
    (data_df['Idade'] <= age_range[1])
]

# Métricas principais
st.subheader('Visão Geral')
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total de Casos", len(df_filtered))
with col2:
    st.metric("Média de Idade", f"{df_filtered['Idade'].mean():.1f} anos")
with col3:
    positive_cases = len(df_filtered[df_filtered['Diagnóstico'] == 'Positivo'])
    st.metric("Casos Positivos", f"{positive_cases} ({(positive_cases/len(df_filtered)*100):.1f}%)")
with col4:
    st.metric("Média da Pontuação", f"{df_filtered['Pontuação Total'].mean():.1f}")

# Gráficos
st.markdown("---")
st.subheader('Distribuição dos Dados')

# Layout em colunas
col1, col2 = st.columns(2)

with col1:
    # Distribuição por Gênero
    fig_gender = px.pie(
        df_filtered, 
        names='Gênero',
        title='Distribuição por Gênero',
        color='Gênero',
        color_discrete_map={'m': '#1f77b4', 'f': '#ff7f0e'}
    )
    st.plotly_chart(fig_gender, use_container_width=True)
    
    # Distribuição por Idade
    fig_age = px.histogram(
        df_filtered, 
        x='Idade',
        nbins=20,
        title='Distribuição por Idade',
        color='Diagnóstico',
        color_discrete_map={'Positivo': '#2ca02c', 'Negativo': '#d62728'}
    )
    st.plotly_chart(fig_age, use_container_width=True)

with col2:
    # Distribuição por Etnia
    fig_eth = px.bar(
        df_filtered['Etnia'].value_counts().reset_index(),
        x='count',
        y='Etnia',
        orientation='h',
        title='Distribuição por Etnia',
        labels={'count': 'Contagem', 'Etnia': 'Etnia'}
    )
    st.plotly_chart(fig_eth, use_container_width=True)
    
    # Distribuição por Pontuação
    fig_score = px.box(
        df_filtered,
        x='Diagnóstico',
        y='Pontuação Total',
        color='Diagnóstico',
        title='Distribuição de Pontuação por Diagnóstico',
        color_discrete_map={'Positivo': '#2ca02c', 'Negativo': '#d62728'}
    )
    st.plotly_chart(fig_score, use_container_width=True)

# Mapa de Calor de Correlação
st.markdown("---")
st.subheader('Correlação entre Características')

# Calcular matriz de correlação apenas para colunas numéricas
numeric_cols = data_df.select_dtypes(include=['int64', 'float64']).columns
df_corr = data_df[numeric_cols].corr()

fig_corr = go.Figure(data=go.Heatmap(
    z=df_corr.values,
    x=df_corr.columns,
    y=df_corr.columns,
    colorscale='RdBu',
    zmin=-1,
    zmax=1
))

fig_corr.update_layout(
    title='Mapa de Calor de Correlação',
    xaxis_title='Características',
    yaxis_title='Características',
    width=800,
    height=700
)

st.plotly_chart(fig_corr, use_container_width=True)

# Tabela de Dados
st.markdown("---")
st.subheader('Visualização dos Dados')
st.dataframe(
    df_filtered.head(100),
    column_config={
        'Idade': st.column_config.NumberColumn('Idade', format='%d anos'),
        'Pontuação Total': st.column_config.NumberColumn('Pontuação Total', format='%.1f')
    },
    hide_index=True,
    use_container_width=True
)

# Estatísticas Descritivas
st.markdown("---")
st.subheader('Estatísticas Descritivas')
st.dataframe(
    df_filtered.describe(),
    use_container_width=True
)

# Estilo
st.markdown("""
<style>
    .stMetricValue {
        font-size: 20px;
    }
    .stMetricLabel {
        font-size: 14px;
    }
</style>
""", unsafe_allow_html=True)

