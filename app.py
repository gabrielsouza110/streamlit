import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data_df = pd.read_csv("autism_screening.csv")
st.set_page_config(layout="wide")

st.title('Análise de Dados com Streamlit')

st.write(data_df.head(15))
st.header("Estatísticas Descritivas")
st.write(data_df.describe())





