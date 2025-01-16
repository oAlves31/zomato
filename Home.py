import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Fome Zero Dashboard',
    page_icon='🍴',
    layout='wide'
)

# Sidebar
image = Image.open('logo.png')  
st.sidebar.image(image, width=120)

st.sidebar.markdown('# Fome Zero Insights')
st.sidebar.markdown('## Your Gateway to Restaurant Analytics')
st.sidebar.markdown("""---""")

st.write('# Fome Zero Growth Dashboard')

st.markdown(
    """
    Bem-vindo ao **Fome Zero Growth Dashboard**! Este painel foi criado para fornecer uma visão abrangente dos dados do dataset Zomato, permitindo que você explore insights globais e locais sobre os restaurantes registrados.

    ### O que você encontrará neste dashboard?
    - **Mapa Interativo**:
        - Localize os restaurantes registrados em um mapa interativo, com destaque para o número total de restaurantes em cada local.
    - **Visão Países**:
        - Conheça o número de restaurantes registrados em cada país.
        - Descubra o custo médio para duas pessoas por país.
        - Identifique a culinária mais popular em cada localidade.
        - Explore os 10 restaurantes mais bem avaliados do mundo.
    - **Visão Cidades**:
        - Analise as cidades com o maior número de restaurantes cadastrados.
        - Entenda a relação entre avaliações e delivery em diferentes cidades.
        - Descubra as cidades com mais restaurantes altamente avaliados (nota acima de 4).
        - Veja as cidades com mais restaurantes de baixa avaliação (nota abaixo de 2.5).
    

    ### Como navegar pelo dashboard?
    - Use o menu na barra lateral para acessar as diferentes visões e análises.
    - Explore gráficos interativos, tabelas e informações que ajudarão você a entender tendências e padrões dos dados do Zomato.

    ### Dúvidas ou sugestões?
    - Entre em contato por e-mail: torre.eric@gmail.com
    """
)
