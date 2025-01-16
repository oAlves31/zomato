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

# ===========================================================================
st.set_page_config(
    page_title='Fome Zero Cities',
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
st.markdown('# Visão Cidades')

st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
        font-size: 30px;  /* Altere o valor conforme necessário */
        font-weight: bold;  /* Opcional: para deixar o texto em negrito */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Usando a tag <div> para aplicar a classe ao texto
st.markdown('<div class="center-text">Cidades com Maior Número de Restaurantes</div>', unsafe_allow_html=True)

city_most_restaurants = (df1.groupby(['city', 'country_code'])['restaurant_id']
                            .count()
                            .reset_index()
                            .sort_values('restaurant_id', ascending=False)
                            .reset_index(drop=True))
fig = (px.bar(city_most_restaurants, x='city', y='restaurant_id', 
              color='country_code', 
              category_orders={"city": city_most_restaurants['city'].tolist()},
              labels={'city': 'Cidades', 
                      'restaurant_id': 'QTD Restaurantes', 
                      'country_code': 'País'}))

st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
        font-size: 30px;  /* Altere o valor conforme necessário */
        font-weight: bold;  /* Opcional: para deixar o texto em negrito */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Usando a tag <div> para aplicar a classe ao texto
st.markdown('<div class="center-text">Relação entre Avaliação e Delivery por Cidade</div>', unsafe_allow_html=True)

# Filtrar cidades com maior número de restaurantes (opcional, para melhor visualização)
top_cities = df1['city'].value_counts().head(10).index
filtered_data = df1[df1['city'].isin(top_cities)]

# Converter a coluna 'has_online_delivery' para mais legível
filtered_data['delivery_status'] = filtered_data['has_online_delivery'].map({1: 'Com Delivery', 0: 'Sem Delivery'})

# Configurar o tamanho da figura
plt.figure(figsize=(14, 8))

# Criar o boxplot
sns.boxplot(
    data=filtered_data,
    x='city',
    y='aggregate_rating',
    hue='delivery_status',
    palette='Set2'
)

# Personalizar o gráfico
#plt.title('Relação entre Avaliação e Disponibilidade de Delivery por Cidade', fontsize=16)
plt.xlabel('Cidade', fontsize=14)
plt.ylabel('Avaliação (Aggregate Rating)', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.legend(title='Status de Delivery', fontsize=12)
plt.tight_layout()

# Mostrar o gráfico no Streamlit
st.pyplot(plt)

# ==============================================================================
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
        font-size: 30px;  /* Altere o valor conforme necessário */
        font-weight: bold;  /* Opcional: para deixar o texto em negrito */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Usando a tag <div> para aplicar a classe ao texto
st.markdown('<div class="center-text">Cidades com mais Restaurantes com Avaliação Acima de 4</div>', unsafe_allow_html=True)

df_aux = df1.loc[df1['aggregate_rating'] >= 4, ['city', 'country_code', 'aggregate_rating']].groupby(['city', 'country_code']).count().reset_index().sort_values('aggregate_rating', ascending=False)
city_restaurant_big_rating = df_aux.iloc[:10, :]

fig = (px.bar(city_restaurant_big_rating, x='city', y='aggregate_rating', color='country_code',
       category_orders={"city": city_restaurant_big_rating['city'].tolist()},
       labels={'city': 'Cidades',
               'country_code': 'País',
               'aggregate_rating': 'Avaliação'}))

st.plotly_chart(fig)

# ==============================================================================
st.markdown(
    """
    <style>
    .center-text {
        text-align: center;
        font-size: 30px;  /* Altere o valor conforme necessário */
        font-weight: bold;  /* Opcional: para deixar o texto em negrito */
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Usando a tag <div> para aplicar a classe ao texto
st.markdown('<div class="center-text">Cidades com mais Restaurantes com Avaliação Abaixo de 2.5</div>', unsafe_allow_html=True)

df_aux = df1.loc[df1['aggregate_rating'] < 2.5, ['country_code', 'city', 'aggregate_rating']].groupby(['country_code', 'city']).count().reset_index().sort_values('aggregate_rating', ascending=False).reset_index(drop=True)
city_restaurant_small_rating = df_aux.iloc[:10, :]

fig = (px.bar(city_restaurant_small_rating, x='city', y='aggregate_rating', color='country_code',
       category_orders={"city": city_restaurant_small_rating['city'].tolist()},
       labels={'city': 'Cidades',
               'country_code': 'País',
               'aggregate_rating': 'Avaliação'}))


st.plotly_chart(fig)