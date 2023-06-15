# ===================================
#               Importações
# ===================================

import pandas as pd
from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image
import numpy as np

st.set_page_config(page_title = 'Visão Restaurantes', page_icon = '🍽️', layout = 'wide')


# ===================================
#               Funções
# ===================================


def clean_code(df1):
    
    """ 
     Esta função tem a responsabilidade de limpar o dataframe
     Tipos de limpeza:
      1. Remoção dos dados NaN
      2. Mudança do tipo de coluna de dados
      3. Remoção dos espaços vazios das variáveis de texto
      2. Formatação da coluna de data
      2. Limpeza da coluna de tempo (remoção do texto da variável numérica) 
      
      Input: Dataframe
      Output: Dataframe
    """
    
    # 1 - Selecionando as linhas que não possuem o valor NaN
    select_age = df['Delivery_person_Age'] != "NaN "
    select_rating = df['Delivery_person_Ratings'] != "NaN "
    select_deliveries = df['multiple_deliveries'] != "NaN "
    select_weather = df['Weatherconditions'] != "conditions NaN"
    select_festival = df['Festival'] != "NaN "
    select_city = df['City'] != "NaN "

    df1 = df1.loc[select_age, :]
    df1 = df1.loc[select_rating, :]
    df1 = df1.loc[select_deliveries, :]
    df1 = df1.loc[select_weather, :]
    df1 = df1.loc[select_festival, :]
    df1 = df1.loc[select_city, :]

    # 2 - Convertendo a coluna Delivery_person_Age para int
    df1["Delivery_person_Age"] = df1['Delivery_person_Age'].astype(int)

    # 3 - Convertendo a coluna Delivery_person_Ratings para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # 4 - Convertendo a coluna Order_Date para datetime
    df1['Order_Date'] = pd.to_datetime( df['Order_Date'], format='%d-%m-%Y' )

    # 5 - Convertendo a coluna multiple_deliveries para int
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # 6 - Limpando a coluna time taken
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ' )[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    # 7 - Removendo os espaços dentro de strings
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1.loc[:, 'Festival'] = df1.loc[:, 'Festival'].str.strip()
    
    return df1

def distance(df1, fig):
    """
    Recebe como parâmetro um dataframe e calcula a distância média entre
    restaurante e entrega, adicionando uma coluna chamada 'distance' que
    informa a distancia dentro de cada linha
    Parâmetro fig:
        - True: retorna o gráfico da distância média para o tipo de cidade
        - False: retorna o valor da distância média geral
    """
    col = ['Delivery_location_latitude', 'Delivery_location_longitude', 'Restaurant_latitude', 'Restaurant_longitude']
    df1['distance'] = ( df1.loc[:, col]
                       .apply(lambda x: haversine (
                                    (x['Delivery_location_latitude'],x['Delivery_location_longitude']),
                                    (x['Restaurant_latitude'], x['Restaurant_longitude'])
                                                ),
                              axis = 1
                                  ) )
    
    if fig:
        avg_distance = df1.loc[:, ['City', 'distance']].groupby('City').mean().reset_index()
    
        fig = go.Figure(
            data = [ go.Pie( labels = avg_distance['City'],
                            values = avg_distance['distance'],
                            pull = [0, 0.1, 0] ) ] 
        )
        fig.update_layout(
        title = {
            'text': 'Distância Média por Cidade',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
        return fig
    else:
        dist_med = df1['distance'].mean()
        dist_med = round(dist_med, 2)
        return dist_med

    

def festival_mean(df1, festival):
    """
    Recebe como parâmetro um dataframe e calcula o tempo médio de entrega
    quando tem ou não festival ('Yes' ou 'No')
    """
    df_aux = df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').mean().reset_index()
    df_aux = df_aux.loc[df_aux['Festival'] == festival, 'Time_taken(min)']
    tempo = round(df_aux, 2)
    return tempo
        
def festival_std(df1, festival):
    """
    Recebe como parâmetro um dataframe e calcula o desvio padrão do tempo de entrega
    quando tem ou não festival ('Yes' ou 'No')
    """
    df_aux = df1.loc[:, ['Time_taken(min)', 'Festival']].groupby('Festival').std().reset_index()
    df_aux = df_aux.loc[df_aux['Festival'] == festival, 'Time_taken(min)']
    tempo = round(df_aux, 2)
    return tempo

def avg_std_time_graph(df1):
    """
    Recebe como parâmetro um dataframe e retorna um gráfico de linha com
    a média e desvio padrão do tempo de entrega por cidade
    """
    cols = ['City', 'Time_taken(min)']
    df_aux = df1.loc[:, cols].groupby('City').agg( {'Time_taken(min)': ['mean', 'std']} )

    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = go.Figure()
    fig.add_trace( go.Bar( name = 'Control',
                           x = df_aux['City'],
                           y = df_aux['avg_time'],
                          error_y = dict( type = 'data', array = df_aux['std_time'] )) )
    fig.update_layout(barmode = 'group')
    return fig

def std_distribution_chart(df1):
    """
    Recebe como parâmetro um dataframe e retorna um gráfico de explosão solar com
    o desvio padrão do tempo de entrega por cidade e trânsito
    """
    cols = ['City', 'Time_taken(min)', 'Road_traffic_density']
    df_aux = df1.loc[:, cols].groupby( ['City', 'Road_traffic_density'] ).agg( {'Time_taken(min)': ['mean', 'std']} )
    df_aux.columns = ['avg_time', 'std_time']
    df_aux = df_aux.reset_index()
    fig = px.sunburst(df_aux, path = ['City', 'Road_traffic_density'], values = 'avg_time', color = 'std_time',
                     color_continuous_scale = 'RdBu_r', color_continuous_midpoint = np.average(df_aux['std_time']))
    fig.update_layout(
        title = {
            'text': 'Distribuição do desvio padrão por<br>cidade e trânsito',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    return fig


# ===================================
#               Dataset
# ===================================

# Importando dataset
df = pd.read_csv('/datasets/train.csv')

# Limpando o dataframe
df1 = clean_code(df)


# ===================================
#               Sidebar
# ===================================


image_path = 'logo_entregador.png'
image = Image.open(image_path)
st.sidebar.image( image, width = 80 )

st.sidebar.markdown('# Curry Company')
st.sidebar.markdown('### Fastest Delivery in Town')

st.sidebar.markdown('---')

st.sidebar.markdown('### Selecione uma data limite')

date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime( 2022, 3, 5 ),
    min_value = pd.datetime( 2022, 2, 11 ),
    max_value = pd.datetime( 2022, 4, 6 ),
    format = 'DD-MM-YYYY'
)

st.sidebar.markdown('---')

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low', 'Medium', 'High', 'Jam'],
    default = ['Low', 'Medium', 'High', 'Jam']
)

st.sidebar.markdown('---')

st.sidebar.caption('Desenvolvido por Vanderson P. Amorim')

# Utilizando o filtro no Dataset

# Filtro data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# Filtro trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )
df1 = df1.loc[linhas_selecionadas, :]


# ===================================
#               layout
# ===================================


st.header( 'Marketplace - Visão Restaurantes' )

with st.container():
    
    st.title('Métricas Gerais')
    
    col1, col2 = st.columns(2)
    
    with col1:
        ent_unic = df1['Delivery_person_ID'].nunique()
        col1.metric('Entreg. \n únicos', ent_unic)
       
    with col2:
        dist_med = distance(df1, False)
        col2.metric( 'Dist. média', dist_med )
        
    col1, col2 = st.columns(2)

        
    with col1:
        tempo = festival_mean(df1, 'Yes')
        col1.metric('Tempo médio entrega c/ festival', tempo)
        
    with col2:
        tempo = festival_std(df1, 'Yes')
        col2.metric('Desvio Padrão entrega c/ festival', tempo)
    
    col1, col2 = st.columns(2)
    
    
    with col1:
        tempo = festival_mean(df1, 'No')
        col1.metric('Tempo médio entrega s/ festival', tempo)
        
    with col2:
        tempo = festival_std(df1, 'No')
        col2.metric('Desvio Padrão entrega s/ festival', tempo)
    
st.markdown('---')
    
with st.container():
    
    st.title('Tempo médio de entrega por cidade')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = avg_std_time_graph(df1)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        cols = ['City', 'Time_taken(min)', 'Type_of_order']
        df_aux = df1.loc[:, cols].groupby(['City', 'Type_of_order']).agg( {'Time_taken(min)': ['mean', 'std']} )
        df_aux.columns = ['avg_time', 'std_time']
        df_aux = df_aux.reset_index()
        st.dataframe(df_aux)
    

    
st.markdown('---')

with st.container():
    
    st.title('Distribuição por cidade')
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico da Distância média por cidade
        fig = distance(df1, True)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        # Distribuição do desvio padrão por cidade e trânsito
        fig = std_distribution_chart(df1)
        st.plotly_chart(fig, use_container_width=True)
