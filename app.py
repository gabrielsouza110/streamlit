import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

data = {
'name' : ['Gabriel','João', 'Pedro'],
'age': [17,18,20],
'City': ['Januária', 'São Francisco','Maria da Cruz']
}

df = pd.DataFrame(data)

st.title('Hello World')
st.write('This is a initial .py file using Streamlit!')

st.header('This is a header')
st.subheader('This is a subheader')

st.text('This is a text')#no fomratting
st.markdown('This is a **markdown** text')#with formatting

st.dataframe(df) # Display the dataframe
st.table(df) # Display the dataframe as a static table

fig, ax = plt.subplots()
ax.bar(df['name'], df['age'])
ax.set_xlabel('name')   # Define o rótulo do eixo x
ax.set_ylabel('age')    # Define o rótulo do eixo y
st.pyplot(fig)  # Display the matplotlib figure


