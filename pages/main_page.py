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
    page_title='Fome Zero Map',
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
filtered_df = df1[df1['country_code'].isin(country_options)]

# ===========================================================================

st.header('Fome Zero!')
st.markdown('### O melhor lugar para encontrar seu restaurante favorito!')
st.markdown('#### Temos as seguintes marcas dentro da nossa plataforma:')

col1, col2, col3, col4, col5 = st.columns(5)
# CSS para ajustar o alinhamento e o espaçamento
st.markdown(
    """
    <style>
    .metric-container {
        text-align: center;
    }
    .metric-number {
        font-size: 32px;
        margin-bottom: -10px; /* Ajusta o espaçamento */
    }
    .metric-label {
        font-size: 16px;
        margin-top: 0;
    }
    </style>
    """, 
    unsafe_allow_html=True
)

# Exibir métricas baseadas no DataFrame original, sem o filtro
with col1:
    restaurant_nunique = df1['restaurant_id'].nunique()  # Usando df1 original
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Restaurantes Cadastrados</div>
            <div class="metric-number">{restaurant_nunique}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    country_nunique = df1['country_code'].nunique()  # Usando df1 original
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Países Cadastrados</div>
            <div class="metric-number">{country_nunique}</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    city_nunique = df1['city'].nunique()  # Usando df1 original
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Cidades Cadastradas</div>
            <div class="metric-number">{city_nunique}</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    total_votes = df1['votes'].sum()  # Usando df1 original
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Avaliações na Plataforma</div>
            <div class="metric-number">{total_votes:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with col5:
    type_cuisine_nunique = df1['cuisines'].nunique()  # Usando df1 original
    st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Culinárias Oferecidas</div>
            <div class="metric-number">{type_cuisine_nunique}</div>
        </div>
    """, unsafe_allow_html=True)

# Agora, exiba o mapa com o DataFrame filtrado
map_center = [filtered_df['latitude'].mean(), filtered_df['longitude'].mean()]
base_map = folium.Map(location=map_center, zoom_start=2)

# Criar cluster de marcadores
marker_cluster = MarkerCluster().add_to(base_map)

# Adicionar marcadores com informações detalhadas
for _, restaurant in filtered_df.iterrows():
    popup_info = (
        f"<b>Restaurante:</b> {restaurant['restaurant_name']}<br>"
        f"<b>Cidade:</b> {restaurant['city']}<br>"
        f"<b>País:</b> {restaurant['country_code']}<br>"
        f"<b>Culinária:</b> {restaurant['cuisines']}<br>"
        f"<b>Avaliações:</b> {restaurant['votes']}<br>"
        f"<b>Custo Médio:</b> {restaurant['average_cost_for_two']}"
    )

    folium.Marker(
        location=[restaurant['latitude'], restaurant['longitude']],
        popup=folium.Popup(popup_info, max_width=300),
        icon=folium.Icon(color="green", icon="cutlery", prefix="fa")
    ).add_to(marker_cluster)

# Exibir mapa no Streamlit
base_map.save('restaurants_with_details_filtered.html')
folium_static(base_map, width=1024, height=600)
