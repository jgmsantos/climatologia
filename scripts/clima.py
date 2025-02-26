import streamlit as st
import pandas as pd
import plotly.express as px
import time
import glob
import numpy as np

from streamlit_option_menu import option_menu
import xarray as xr

st.sidebar.title("Monitoramento de dados ambientais")

with st.sidebar:
    selected = option_menu(
        'Menu',
        ['Focos de queimadas', 'Precipitação', 'Temperatura'],
        icons=['bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill'],
        menu_icon='cast',
        default_index=0,
        styles={
                    'menu-title' : {'font-size' : '18px'}, # Diminui o tamanho da fonte do título
                    'menu-icon': {'display': 'none'},  # Remove o ícone do título
                    'icon': {'font-size': '12px'},  # Estilo dos ícones
                    'nav-link': {
                        'font-size': '15px',  # Tamanho da fonte dos itens do menu
                        '--hover-color': '#778595',  # Cor de fundo ao passar o mouse
                    },
                    'nav-link-selected': {'background-color': '#FC981C'},  # Cor de fundo do item selecionado
                }
    )
    
if selected == 'Focos de queimadas':
    st.title('Focos de queimadas')
    tab1, tab2 = st.tabs(['Espacial', 'Série temporal'])

    with tab1:
        st.write('Mapa de focos de queimadas')
        try:
            # Abrir o arquivo NetCDF
            ds = xr.open_dataset("../output/clima_focos_espacial.nc")

            # Converter as coordenadas 'longitude' e 'latitude' para 'lon' e 'lat'
            #ds = ds.rename({'longitude': 'lon', 'latitude': 'lat'})

            # Criar uma lista de meses disponíveis no dataset
            months = list(ds['time'].dt.month.values)

            # Remover duplicatas da lista de meses
            months = list(dict.fromkeys(months))

            # Criar um seletor de mês
            selected_month = st.selectbox('Selecione o mês', months)

            # Filtrar o dataset para o mês selecionado
            ds_month = ds.sel(time=ds['time.month'] == selected_month)

            # Adicionar o token do Mapbox
            px.set_mapbox_access_token('YOUR_MAPBOX_ACCESS_TOKEN')

            # Criar o mapa usando plotly express
            fig = px.density_mapbox(
                data_frame=ds_month.to_dataframe().reset_index(),
                lat='lat',
                lon='lon',
                z='nf',
                radius=7,
                center=dict(lat=-15, lon=-50),
                zoom=2,
                mapbox_style="stamen-terrain",
                title=f'Focos de Queimadas - Mês {selected_month}',
                color_continuous_scale='viridis'
            )

            # Aumentar o tamanho da caixa do mapa
            fig.update_layout(
                width=800,
                height=600
            )

            fig.update_layout(
            xaxis_title="Longitude",
            yaxis_title="Latitude"
            )

            # Exibir o mapa no Streamlit
            st.plotly_chart(fig)

        except FileNotFoundError:
            st.error("Arquivo merge.nc não encontrado. Verifique o caminho do arquivo.")
        except Exception as e:
            st.error(f"Ocorreu um erro ao processar o arquivo: {e}")

elif selected == 'Precipitação':
    st.title('Precipitação')

elif selected == 'Temperatura':
    st.title('Temperatura')

else:
    st.write('Selecione uma opção no menu lateral')
