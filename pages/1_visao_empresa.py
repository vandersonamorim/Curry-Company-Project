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

st.set_page_config(page_title = 'Visão Empresa', page_icon = '🏭', layout = 'wide')


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

def order_metric(df1):
    """
    Esta função recebe como parâmetro um dataframe e retorna um gráfico de barras da 
    quantidade de pedidos feitos por dia
    """
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby('Order_Date').count().reset_index()
    fig = px.bar(df_aux, x = 'Order_Date', y = 'ID')
    fig.update_layout(
        title = {
            'text': 'Quantidade de Pedidos por Dia',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    fig.update_xaxes(title_text = None)
    fig.update_yaxes(title_text = None)
    return fig

def traffic_order_share_pie(df1):
    """
    Esta função recebe como parâmetro um dataframe e retorna um gráfico de pizza da
    distribuição da quantidade de pedidos por tipo de tráfego
    """
    df_aux = df1.loc[:, ['ID', 'Road_traffic_density']]. groupby('Road_traffic_density').count().reset_index()

    # Criando uma coluna com a porcentagem
    df_aux['perc_ID'] = 100 * (df_aux['ID'] / df_aux['ID'].sum())

    # Formatando o gráfico
    fig = px.pie( df_aux, values = 'perc_ID', names = 'Road_traffic_density')
    fig.update_layout(
    title = {
        'text': 'Quantidade de Pedidos por Tráfego',
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': {'size': 16}
        },
    legend = dict(orientation="h", yanchor="bottom", y = -0.15, xanchor="center", x=0.5)
    )
    fig.update_traces(
        hovertemplate="Tipo de tráfego: %{label}")
    return fig

def traffic_order_share_scatter(df1):
    """
    Esta função recebe como parâmetro um dataframe e retorna um gráfico de bolha da
    quantidade de pedidos por cidade e tipo de tráfego
    """
    df_aux = ( df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                  .groupby( ['City', 'Road_traffic_density'] )
                  .count()
                  .reset_index() )
    fig = px.scatter(df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID')
    fig.update_layout(
        title = {
            'text': 'Quantidade de Pedidos por Cidade e Tráfego',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    return fig
    
def order_by_week(df1):
    """
    Esta função recebe como parâmetro um dataframe e retorna um gráfico de linhas da
    quantidade de pedidos por semana
    """ 
    # Criando uma coluna com a semana do ano
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )

    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()

    fig = px.line(df_aux, x = 'week_of_year', y = 'ID')
    fig.update_layout(
        title = {
            'text': 'Quantidade de Pedidos por Semana',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    return fig

def order_by_week_person(df1):
    """
    Esta função recebe como parâmetro um dataframe e retorna um gráfico de linhas da
    quantidade de pedidos por semana e por entregador
    """
    df_aux1 = df1.loc[:, ['ID', 'week_of_year']].groupby('week_of_year').count().reset_index()
    df_aux2 = df1.loc[:, ['Delivery_person_ID', 'week_of_year']].groupby('week_of_year').nunique().reset_index()

    # Fazendo a junção dos data frames anteriores
    df_aux = pd.merge(df_aux1, df_aux2, how = 'inner')

    # Fazendo o calculo
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']

    # Grafico
    fig = px.line(df_aux, x = 'week_of_year', y = 'order_by_delivery')
    fig.update_layout(
        title = {
            'text': 'Quantidade de Pedidos por Entregador por Semana',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size': 16}
        }
    )
    return fig

def country_maps(df1):
    """
    Esta função recebe como parâmetro um dataframe e retorna um mapa de
    acordo com a latitude e longitude
    """
    col = ['City','Road_traffic_density','Delivery_location_latitude','Delivery_location_longitude']
    col_groupby = ['City', 'Road_traffic_density']

    df1 = df1.loc[:, col].groupby(col_groupby).median().reset_index()
    df_aux = df1.head()

    map = folium.Map()

    for index, location_info in df_aux.iterrows():
        folium.Marker(
            [
                location_info['Delivery_location_latitude'],
                location_info['Delivery_location_longitude']
            ]
        ).add_to(map)

    folium_static( map )

    return None

    
# ===================================
#               Dataset
# ===================================


# Importando dataset
df = pd.read_csv('../datasets/train.csv')

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
#               layout
# ===================================


st.header( 'Marketplace - Visão Cliente' )

tab1, tab2, tab3 = st.tabs( ['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'] )

with tab1:
    
    with st.container():
        # Gráfico de Barras da Quantidade de Pedidos por Dia
        fig = order_metric(df1)
        st.plotly_chart( fig, use_container_width = True )
    
    with st.container():    
        # Criando 2 colunas
        col1, col2 = st.columns(2)

        with col1:
            
            # Gráfico de Pizza de Quantidade de Pedidos por Tráfego
            fig = traffic_order_share_pie(df1)
            st.plotly_chart( fig, use_container_width = True )            
        
        with col2:
            
            # Gráfico de Bolha de Quantidade de Pedidos por Ciade e Tráfego
            fig = traffic_order_share_scatter(df1)
            st.plotly_chart( fig, use_container_width = True )

    
with tab2:
    
    # Gráfico de Pedidos por Semana
    with st.container():
        fig = order_by_week(df1)
        st.plotly_chart( fig, use_container_width = True )
    
    # Gráfico de Pedidos por Entregador por Semana
    with st.container():
        fig = order_by_week_person(df1)
        st.plotly_chart( fig, use_container_width = True )

with tab3:
    
    # Mapa
    country_maps(df1)