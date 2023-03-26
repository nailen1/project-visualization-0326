import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.subheader('물건 종류별 비율 살펴보기')

df = pd.read_csv('./database/auction-items-nonan.csv')

list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
list_cat = ['모든 종류'] + df['category'].unique().tolist()


tab_a, tab_b = st.tabs(['전체 지역 비교', '개별 지역'])

df_grouped = df.groupby(['address_sido', 'category']
                        ).size().reset_index(name='count')
# 비율 계산
df_grouped['percent'] = df_grouped.groupby(
    'address_sido')['count'].apply(lambda x: x / x.sum() * 100)
# stacked bar chart 그리기
fig_a = px.bar(df_grouped, x='percent', y='address_sido', color='category',
               barmode='stack', color_discrete_sequence=px.colors.qualitative.Alphabet,
               template='simple_white')
fig_a.update_layout(xaxis_title='percent', yaxis_title='address_sido')

tab_a.plotly_chart(fig_a, theme=None, use_container_width=True)


address_sido = tab_b.selectbox('지역 선택(시도)', list_sido)
selected_region = address_sido

if address_sido != '전체 지역':
    df = df[df['address_sido'] == address_sido]

fig_b = px.pie(df, names="category")

tab_b.plotly_chart(fig_b, theme=None, use_container_width=True)
