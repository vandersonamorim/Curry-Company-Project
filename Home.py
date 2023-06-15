import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = 'Home',
    page_icon = '🏚️',
    initial_sidebar_state = 'expanded'
)

image_path = './logo_entregador.png'
image = Image.open(image_path)

st.sidebar.image(image, width = 80)

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('### Fastest Delivery in Town')

st.sidebar.markdown('---')

st.sidebar.caption('Desenvolvido por Vanderson P. Amorim')

st.markdown(
    '''
    ## Curry Company Growth Dashboard
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
            ''')


