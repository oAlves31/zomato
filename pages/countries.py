import pandas as pd
import inflection
import plotly.express as px
import folium
from folium.plugins import MarkerCluster
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster
from PIL import Image

df = pd.read_csv('dataset/zomato.csv')

df1 = df.copy()
df1 = df1.dropna()

# ============================= LIMPEZA ==================================
# Criando uma coluna Country Name
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
}
def country_name(country_id):
    return COUNTRIES.get(country_id, "Unknown")

df1['Country Code'] = df1['Country Code'].apply(country_name)

# Criação do Tipo de Categoria de Comida
def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

df1['Price range'] = df1['Price range'].apply(create_price_tye)

# Criação do nome das Cores
COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
}
def color_name(color_code):
    return COLORS.get(color_code, "undefined")

df1['Rating color'] = df1['Rating color'].apply(color_name)

# Renomear as colunas do DataFrame
def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

df1 = rename_columns(df1)

# Categorizar os restaurante por um tipo de culinária
df1["cuisines"] = df1["cuisines"].fillna("").apply(lambda x: x.split(",")[0])

# ============================ SideBar ===============================================
st.set_page_config(
    page_title='Fome Zero Countries',
    page_icon='🍴',
    layout='wide'
)
# SideBar
image = Image.open('logo.png')  
st.sidebar.image(image, width=120)
st.sidebar.markdown('# Fome Zero Insights')
st.sidebar.markdown('## Your Gateway to Restaurant Analytics')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')

# Filtro para países selecionados
country_options = st.sidebar.multiselect(
    'Selecione os países que deseja visualizar os restaurantes',
    ['Philippines', 'Brazil', 'Australia', 'United States of America',
     'Canada', 'Singapure', 'United Arab Emirates', 'India',
     'Indonesia', 'New Zeland', 'England', 'Qatar', 'South Africa',
     'Sri Lanka', 'Turkey'],
    default=['Brazil', 'Australia', 'United States of America',
             'England', 'Qatar', 'South Africa']
)

# Filtrando o df1 apenas para os países selecionados
linhas_selecionadas = df1['country_code'].isin(country_options)
df1 = df1.loc[linhas_selecionadas, :]

# ===========================================================================

st.markdown('# Visão Países')
col1, col2 = st.columns(2)
with col1:
    # Restaurantes Registrados por País
    st.markdown(
        """
        <style>
        .center-text {
            text-align: center;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown('<p class="center-text">Restaurantes Registrados por País</p>', unsafe_allow_html=True)

    df_aux = df1.groupby('country_code')['restaurant_id'].nunique().reset_index().sort_values(by='restaurant_id', ascending=False)
    fig = px.bar(df_aux, x='country_code', y='restaurant_id', labels={'country_code': 'País', 'restaurant_id': 'Quantidade de Restaurantes'})

    st.plotly_chart(fig, use_container_width=True)

with col2:
    # Custo Médio para Duas Pessoas por País
    st.markdown(
        """
        <style>
        .center-text {
            text-align: center;
        }
        </style>
        """, 
        unsafe_allow_html=True
    )
    st.markdown('<p class="center-text">Custo Médio para Duas Pessoas por País</p>', unsafe_allow_html=True)
    mean_average_cost_for_two_by_country = df1.groupby('country_code')['average_cost_for_two'].mean().reset_index().sort_values(by='average_cost_for_two', ascending=False)

    fig = px.bar( mean_average_cost_for_two_by_country, x='country_code', y='average_cost_for_two', labels={'average_cost_for_two': 'Custo Médio para Dois', 'country_code': 'País'} )
    st.plotly_chart(fig)

#==============================================================================
# Culinária mais popular em cada país
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
st.markdown('<p class="center-text">Culinária mais Popular em cada País</p>', unsafe_allow_html=True)
df_aux = df1.groupby(['country_code', 'cuisines']).size().reset_index(name='restaurant_count')
df_popular_cuisine = df_aux.loc[df_aux.groupby('country_code')['restaurant_count'].idxmax()].sort_values(by='restaurant_count', ascending=False)
df_popular_cuisine = df_popular_cuisine.rename(columns={'country_code': 'País', 'cuisines': 'Culinária', 'restaurant_count': 'Número de Restaurantes'})

st.dataframe(df_popular_cuisine, use_container_width=True)

# Top 10 Restaurantes com as Melhores Avaliações
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
    }
    </style>
    """, 
    unsafe_allow_html=True
)
st.markdown('<p class="center-text">Top 10 Restaurantes com as Melhores Avaliações</p>', unsafe_allow_html=True)
df_aux = df1.groupby('restaurant_name').agg({
    'aggregate_rating': 'mean', 
    'votes': 'sum'
}).reset_index().sort_values(by=['aggregate_rating', 'votes'], ascending=[False, False]).reset_index(drop=True)

df_aux = df_aux.rename(columns={'restaurant_name': 'Restaurante', 'aggregate_rating': 'Avaliação', 'votes': 'Quantidade de Avaliações'})


st.dataframe(df_aux.head(10), use_container_width=True)

