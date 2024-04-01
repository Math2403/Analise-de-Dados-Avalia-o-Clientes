import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import datetime as dt
import numpy as np
import streamlit as st
from collections import OrderedDict

st.set_page_config(layout='wide')

text = 'DASHBOARD DADOS DE AVALIAÇÃO CONSUMIDORES'
header = st.header(text)
title_style = f'<p style="font-family:sans-serif; color:#3d39fa; text-align: center; font-size: 50px; font-weight: bold;">{text}</p>'
header.markdown(title_style, unsafe_allow_html=True)

st.divider()

df = pd.read_csv('Customer_support_data.csv', sep=',')

df = df.drop(columns='Survey_response_Date')
df = df.drop(columns='connected_handling_time')
df = df.drop(columns='order_date_time')

df['Issue_reported at'] = pd.to_datetime(df['Issue_reported at'], format='%d/%m/%Y %H:%M')
df['issue_responded'] = pd.to_datetime(df['issue_responded'], format='%d/%m/%Y %H:%M')

avaliacoes_categorias = df.groupby(by=['CSAT Score', 'category', 'Sub-category'], as_index=False)[['Unique id']].count()
avaliacoes_categorias = avaliacoes_categorias.sort_values(by=['CSAT Score','Unique id'], ascending=[True, False])
avaliacoes_categorias_negativas = avaliacoes_categorias.loc[avaliacoes_categorias['CSAT Score'] == 1].head(10)
avaliacoes_categorias_positivas = avaliacoes_categorias.loc[avaliacoes_categorias['CSAT Score'] == 5].head(10)
total_avaliacoes_categorias = pd.concat([avaliacoes_categorias_negativas, avaliacoes_categorias_positivas], ignore_index=True)
total_avaliacoes_categorias['Categoria'] = total_avaliacoes_categorias['category'] + ' ' + total_avaliacoes_categorias['Sub-category']
total_avaliacoes_categorias = total_avaliacoes_categorias.drop(columns=['category', 'Sub-category'])
total_avaliacoes_categorias = total_avaliacoes_categorias.rename(columns={'CSAT Score':'Nota', 'Unique id':'Qtd_Clientes'})

avaliacoes_agentes = df.groupby(by=['CSAT Score', 'Agent_name'], as_index=False).agg({'Tenure Bucket': 'first','Unique id': 'count'})
avaliacoes_agentes = avaliacoes_agentes.sort_values(by=['CSAT Score', 'Unique id'], ascending=[True, False])

avaliacoes_agente_negativas = avaliacoes_agentes.loc[avaliacoes_agentes['CSAT Score'].isin([1, 2])]
avn = avaliacoes_agente_negativas.groupby(by='Agent_name', as_index=False)['Unique id'].sum().sort_values(by='Unique id', ascending=False).head(10)
avn = avn.rename(columns={'Agent_name': 'Nome_Agente', 'Unique id': 'Qtd_Avaliacoes'})

media_avaliacoes_negativas = avaliacoes_agentes.loc[avaliacoes_agentes['CSAT Score'].isin([1, 2]) ]['Unique id'].mean()
media_avaliacoes_positivas = avaliacoes_agentes.loc[avaliacoes_agentes['CSAT Score'].isin([4, 5]) ]['Unique id'].mean()

avaliacoes_agente_positivas = avaliacoes_agentes.loc[avaliacoes_agentes['CSAT Score'].isin([4, 5])]
avp = avaliacoes_agente_positivas.groupby(by='Agent_name', as_index=False)['Unique id'].sum().sort_values(by='Unique id', ascending=False).head(10)
avp = avp.rename(columns={'Agent_name': 'Nome_Agente', 'Unique id': 'Qtd_Avaliacoes'})

avaliacoes_dia_hora = df.groupby(by=['CSAT Score', 'Issue_reported at'], as_index=False)['Unique id'].count()
avaliacoes_dia_hora['Issue_reported at'] = avaliacoes_dia_hora['Issue_reported at'].dt.day
avaliacoes_dia_hora = avaliacoes_dia_hora.sort_values(by=['CSAT Score', 'Issue_reported at'], ascending=[True, True])

avaliacoes_dia = avaliacoes_dia_hora.groupby(by=['CSAT Score', 'Issue_reported at'], as_index=False)['Unique id'].count()
avaliacoes_dia = avaliacoes_dia.rename(columns={'CSAT Score': 'Nota', 'Issue_reported at':'Data_Reportacao','Unique id': 'Qtd_Clientes'})

tempo_agentes = df[['Agent_name', 'Issue_reported at', 'issue_responded']]
tempo_agentes['Response time'] = tempo_agentes['issue_responded'].sub(tempo_agentes['Issue_reported at'], axis=0)
tempo_agentes['Response time'] = tempo_agentes['Response time'] / np.timedelta64(1, 'm')
tempo_agentes.loc[tempo_agentes['Response time'] < 0, 'Response time'] += 1440 

tempo_medio_agentes = tempo_agentes.groupby(by='Agent_name', as_index=False)['Response time'].mean()
maior_tempo_resposta = tempo_medio_agentes.sort_values(by='Response time', ascending=False).head(10)
maior_tempo_resposta = maior_tempo_resposta.rename(columns={'Agent_name': 'Nome_Agente', 'Response time':'Tempo_Resposta'})
menor_tempo_resposta = tempo_medio_agentes.sort_values(by='Response time', ascending=True).head(10)
menor_tempo_resposta = menor_tempo_resposta.rename(columns={'Agent_name': 'Nome_Agente', 'Response time':'Tempo_Resposta'})

media_tempo_resposta = tempo_agentes['Response time'].mean()

qtd_avaliacoes = df.groupby(by='CSAT Score', as_index=False)['Unique id'].count()

qtd_avaliacoes_positivas = qtd_avaliacoes.loc[qtd_avaliacoes['CSAT Score'].isin([5, 4])]
qtd_avaliacoes_positivas = qtd_avaliacoes_positivas['Unique id'].sum()

qtd_avaliacoes_media = qtd_avaliacoes.loc[qtd_avaliacoes['CSAT Score'] == 3]
qtd_avaliacoes_media = qtd_avaliacoes_media['Unique id'].sum()

qtd_avaliacoes_negativas = qtd_avaliacoes.loc[qtd_avaliacoes['CSAT Score'].isin([1, 2])]
qtd_avaliacoes_negativas = qtd_avaliacoes_negativas['Unique id'].sum()

col8, col9 = st.columns(2)

container_style = """
    <style>
        .container1 {
                background-color: #3d39fa;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 20px;
                width: 92%;
                padding-top: 35px
        }
    </style>
"""

st.markdown(container_style, unsafe_allow_html=True)

qtd_clientes = df.shape[0]

with col8:
        container1 = st.container()
        new_title1 = f'<div class="container1"><p style="font-family:sans-serif; color:White; font-size: 20px; text-align: center; font-weight: bold;">QUANTIDADE DE CLIENTES: {qtd_clientes}</p>'
        container1.markdown(new_title1, unsafe_allow_html=True)

with col9:
        container2 = st.container()
        new_title = f'<div class="container1"><p style="font-family:sans-serif; color:White; font-size: 20px; text-align: center; font-weight: bold;">MÉDIA TEMPO DE RESPOSTA: {int(media_tempo_resposta)} min</p>'
        container2.markdown(new_title, unsafe_allow_html=True)

st.divider()

col1, col2 = st.columns(2)
st.divider()
col3, col4 = st.columns(2)
st.divider()
col5, col6, col7 = st.columns(3)

PLOT_BGCOLOR = "#FFFFFF"

st.markdown(
    f"""
    <style>
    .stPlotlyChart {{
     outline: 5px solid {PLOT_BGCOLOR};
     border-radius: 5px;
     box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.20), 0 6px 20px 0 rgba(0, 0, 0, 0.30);
    }}
    </style>
    """, unsafe_allow_html=True
)

grafico_agentes_avaliacao_negativa = px.bar(avn, x='Nome_Agente', y='Qtd_Avaliacoes', text_auto=True, title='TOP-10 Funcionários com mais avaliações negativas (Nota 1 ou 2)')
# grafico_agentes_avaliacao_negativa.add_hline(y=media_avaliacoes_negativas, line_color='#141345')
grafico_agentes_avaliacao_negativa.update_traces(textfont_size=12, textposition='outside', cliponaxis=False, marker_color='#3d39fa', textfont_color='#000000')
grafico_agentes_avaliacao_negativa.update_layout(showlegend=True, xaxis_title='Nome Agentes', yaxis_title='Quantidade Avaliações', paper_bgcolor="#FFFFFF", font_color='#000000', title_font_color='#000000')
grafico_agentes_avaliacao_negativa.update_yaxes(visible=False)                                                        
grafico_agentes_avaliacao_negativa.update_xaxes(title=None, tickfont_color='#000000') 

grafico_agentes_avaliacao_negativa.add_trace(go.Scatter(
    x=['Brandy Foley', 'Jamie Smith'],
    y=[media_avaliacoes_negativas, media_avaliacoes_negativas],
    mode='lines',
    line_color='#141345',
    name='média',
    showlegend=True))

col1.plotly_chart(grafico_agentes_avaliacao_negativa, theme=None) 

grafico_agentes_avaliacao_positiva = px.bar(avp, x='Nome_Agente', y='Qtd_Avaliacoes', text_auto=True, title='TOP-10 Funcionários com mais avaliações positivas (Nota 4 ou 5)')
grafico_agentes_avaliacao_positiva.update_traces(textfont_size=12, textposition='outside', cliponaxis=False, marker_color='#141345')
grafico_agentes_avaliacao_positiva.update_layout(xaxis_title='Nome Agentes', yaxis_title='Quantidade Avaliações', paper_bgcolor="#FFFFFF", font_color='#000000', title_font_color='#000000')
grafico_agentes_avaliacao_positiva.update_yaxes(visible=False)                                                        
grafico_agentes_avaliacao_positiva.update_xaxes(title=None, tickfont_color='#000000') 

grafico_agentes_avaliacao_positiva.add_trace(go.Scatter(
    x=['Matthew White PhD', 'Wendy Taylor'],
    y=[media_avaliacoes_negativas, media_avaliacoes_negativas],
    mode='lines',
    line_color='#7aace6',
    name='média',
    showlegend=True))

col2.plotly_chart(grafico_agentes_avaliacao_positiva, theme=None) 

gv_avalicao_empresa = px.line(avaliacoes_dia, x='Data_Reportacao', y='Qtd_Clientes', markers=True, color='Nota', color_discrete_sequence=['#7aace6', '#0894ff', '#3d39fa', '#0e008c', '#141345'], title='Avaliações Mês (Agosto)')
gv_avalicao_empresa.update_layout(xaxis_title='Dia do Mês', yaxis_title='Quantidade Avaliações', legend_title='Notas', paper_bgcolor="#FFFFFF", font_color='#000000', title_font_color='#000000', legend_title_font_color="#000000")
gv_avalicao_empresa.update_xaxes(tickfont_color='#000000', title_font_color='#000000', showgrid=False)
gv_avalicao_empresa.update_yaxes(tickfont_color='#000000', title_font_color='#000000', showgrid=False)
col3.plotly_chart(gv_avalicao_empresa, theme=None) 

df_colors = list(OrderedDict.fromkeys(total_avaliacoes_categorias['Nota']))
df_colors[0] = str(df_colors[0])
df_colors[1] = str(df_colors[1])
colors_dict = {'1': '#141345', '5': '#3d39fa'}
plotly_colors = [colors_dict[c] for c in df_colors]

grafico_total_avaliacoes_categoria = px.histogram(total_avaliacoes_categorias, x='Categoria', y='Qtd_Clientes', color='Nota', color_discrete_sequence=plotly_colors, title='Categorias com mais avaliações positivas e negativas')
grafico_total_avaliacoes_categoria.update_layout(paper_bgcolor="#FFFFFF", title_font_color='#000000', legend_title_font_color="#000000", font_color='#000000')
grafico_total_avaliacoes_categoria.update_yaxes(title=None, showgrid=False)
grafico_total_avaliacoes_categoria.update_xaxes(automargin=True, title=None, tickfont_color='#000000', title_font_color='#000000')
col4.plotly_chart(grafico_total_avaliacoes_categoria, theme=None) 

grafico_ag_maior_tempo = px.bar(maior_tempo_resposta, x='Tempo_Resposta', y='Nome_Agente', orientation='h', text_auto=True, 
                                title='Agentes com maior tempo médio de resposta (Minutos)', width=500)
grafico_ag_maior_tempo.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor="#FFFFFF", title_font_color='#000000')
grafico_ag_maior_tempo.update_traces(marker_color='#141345')
grafico_ag_maior_tempo.update_yaxes(title=None, showgrid=False, zeroline=False, ticksuffix = "  ", tickfont_color='#000000', ticklabelposition='inside')                                    
grafico_ag_maior_tempo.update_xaxes(showgrid=False, zeroline=False, visible=False)                         
col5.plotly_chart(grafico_ag_maior_tempo, theme=None) 

grafico_ag_menor_tempo = px.bar(menor_tempo_resposta, x='Tempo_Resposta', y='Nome_Agente', orientation='h', text_auto=True, 
                                title='Agentes com menor tempo médio de resposta (Minutos)', width=500)
grafico_ag_menor_tempo.update_layout(yaxis=dict(autorange="reversed"), paper_bgcolor="#FFFFFF", title_font_color='#000000')
grafico_ag_menor_tempo.update_traces(marker_color='#3d39fa', textposition='inside')
grafico_ag_menor_tempo.update_yaxes(title=None, showgrid=False, zeroline=False, ticksuffix = "  ", tickfont_color='#000000', ticklabelposition='inside')                                    
grafico_ag_menor_tempo.update_xaxes(showgrid=False, zeroline=False, visible=False)                         
col6.plotly_chart(grafico_ag_menor_tempo, theme=None) 

labels = ['Avaliações Positivas', 'Avaliações Médias', 'Avaliações Negativas']
grafico_qtd_avaliacoes = go.Figure(data=[
                                    go.Pie(labels=labels, 
                                           values=[qtd_avaliacoes_positivas, qtd_avaliacoes_media, qtd_avaliacoes_negativas],
                                           textinfo='label+percent', hole=.8, marker=dict(colors=['#141345', '#3d39fa', '#7aace6']))])
grafico_qtd_avaliacoes.update_layout(annotations=[dict(text='AVALIAÇÕES', x=0.50, y=0.5, font_size=30, showarrow=False, font_color='#000000')], showlegend=False, width=500, paper_bgcolor="#FFFFFF", font_color='#000000', title=dict(text='Porcentagem Avaliações Mês (Agosto)'))
col7.plotly_chart(grafico_qtd_avaliacoes, theme=None) 





