# ===================================
#               Importações
# ===================================


import pandas as pd
from haversine import haversine
import plotly.express as px
import streamlit as st
import folium
from streamlit_folium import folium_static
from PIL import Image
from datetime import datetime

st.set_page_config(page_title = 'Visão Entregadores', page_icon = '🛵', layout = 'wide')

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

def top_deliver(df1, top_asc):
    """
    Recebe como parâmetro um dataframe e a forma de ordenamento da coluna de tempo e 
    retorna um dataframe com os entregadores ordenados pelo tempo de entrega
    """
    df_aux = ( df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
                  .groupby(['City', 'Delivery_person_ID'])
                  .max()
                  .sort_values(['City', 'Time_taken(min)'], ascending = top_asc)
                  .reset_index() )
    df_aux01 = df_aux.loc[df_aux['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df_aux.loc[df_aux['City'] == 'Semi-Urban', :].head(10)
    df_aux03 = df_aux.loc[df_aux['City'] == 'Urban', :].head(10)
    df_ordenado = pd.concat( [df_aux01,df_aux02,df_aux03] ).reset_index( drop = True )
    
    return df_ordenado

def rating_avg_std(df1, col):
    """
    Recebe como parâmetro um dataframe e o novo de uma coluna (string) e retorna
    um dataframe com a média e desvio padrão das avaliações organizados pela coluna informada
    """
    df_aux = ( df1.loc[:, [col, 'Delivery_person_Ratings']]
              .groupby(col)
              .agg( {'Delivery_person_Ratings': ['mean', 'std'] } ) )
    df_aux.columns = ['delivery_mean', 'delivery_std']
    df_med_std = df_aux.reset_index()
    return df_med_std


# ===================================
#               Dataset
# ===================================

# Importando dataset
df = pd.read_csv('./datasets/train.csv')

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
    # value = pd.datetime( 2022, 3, 5 ),
    # min_value = pd.datetime( 2022, 2, 11 ),
    # max_value = pd.datetime( 2022, 4, 6 ),
    value = datetime.strptime(pd.to_datetime('2022-03-05').strftime('%Y-%m-%d'), '%Y-%m-%d'),
    min_value = datetime.strptime(pd.to_datetime('2022-02-11').strftime('%Y-%m-%d'), '%Y-%m-%d'),
    max_value = datetime.strptime(pd.to_datetime('2022-04-06').strftime('%Y-%m-%d'), '%Y-%m-%d'),
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
#               Layout
# ===================================


st.header( 'Marketplace - Visão Entregadores' )

with st.container():
    
    st.title('Métricas Gerais')
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        maior_idade = df1.loc[:, 'Delivery_person_Age'].max()
        col1.metric( 'Maior idade', maior_idade )
        
    with col2:
        menor_idade = df1.loc[:, 'Delivery_person_Age'].min()
        col2.metric( 'Menor idade', menor_idade )
        
    with col3:
        melhor = df1.loc[:, 'Vehicle_condition'].max()
        col3.metric( 'Melhor condição', melhor )
        
    with col4:
        pior = df1.loc[:, 'Vehicle_condition'].min()
        col4.metric( 'Pior condição', pior )
        
st.markdown('---')

with st.container():
    
    st.title('Avaliações')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown( '##### Avaliações média por entregador' )
        table_med_ent = ( df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                            .groupby('Delivery_person_ID')
                            .mean()
                            .reset_index() )
        st.dataframe( table_med_ent, height = 492 )
        
    with col2:
        st.markdown( '##### Avaliação média por trânsito' )
        df_avg_std_traf = rating_avg_std(df1, 'Road_traffic_density')
        st.dataframe( df_avg_std_traf )
        
        st.markdown( '##### Avaliação média por clima' )
        df_avg_std_weather = rating_avg_std(df1, 'Weatherconditions')
        st.dataframe( df_avg_std_weather )
        
st.markdown('---')

with st.container():
    
    st.title('Velocidade de entrega')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown( '##### Top entregadores mais rápidos' )
        df_rapidos = top_deliver(df1, True)
        st.dataframe( df_rapidos )    
        
    with col2:
        st.markdown( '##### Top entregadores mais lentos' )
        df_lentos = top_deliver(df1, False)
        st.dataframe( df_lentos )
        
        
        
