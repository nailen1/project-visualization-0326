import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title("평당 가격 살펴보기")

df = pd.read_csv('./database/auction-items-nonan.csv')

list_var_kr = ['감정가', '최저입찰가']
dict_var = {'감정가': 'price_estimate', '최저입찰가': 'price_bidding'}
list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
list_cat = ['모든 종류'] + df['category'].unique().tolist()

selected_key = st.selectbox('관심 변수 선택', list_var_kr)

st.subheader(
    f":chart_with_upwards_trend: 지역별 평당 {selected_key}")
st.text('')

selected_cat = st.selectbox('카테고리 선택', list_cat)

df_cat_1 = df[df['category'] == selected_cat]
if selected_cat == '모든 종류':
    df_cat_1 = df

prices_py_1 = []
for sido in list_sido:
    df_sido_1 = df_cat_1[df_cat_1['address_sido'] == sido]
    if sido == '전체 지역':
        df_sido_1 = df_cat_1

    sum_price_1 = df_sido_1[dict_var[selected_key]].sum() or 0
    sum_area_1 = df_sido_1['area'].sum() or 1

    price_py_1 = int(sum_price_1/sum_area_1)
    prices_py_1.append(price_py_1)

df_1 = pd.DataFrame(
    {'sido': list_sido, 'price_py': prices_py_1}).sort_values('price_py', ascending=False)

fig1 = go.Figure()
fig1.add_trace(go.Bar(name="전체", x=df_1['sido'], y=df_1['price_py']))

# y축 타이틀로 단위 표시
fig1.update_yaxes(title="단위: 원")
# 수정사항 끝


with st.expander(f"선택 카테고리: {selected_cat}", expanded=True):
    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)


st.subheader(
    f":chart_with_upwards_trend: 물건 종류별 평당 {selected_key}")
st.text('')

selected_sido = st.selectbox('지역 선택', list_sido)

df_sido_2 = df[df['address_sido'] == selected_sido]
if selected_sido == '전체 지역':
    df_sido_2 = df

prices_py_2 = []
for cat in list_cat:
    df_cat_2 = df_sido_2[df_sido_2['category'] == cat]
    if cat == '모든 종류':
        df_cat_2 = df_sido_2

    sum_price_2 = df_cat_2[dict_var[selected_key]].sum() or 0
    sum_area_2 = df_cat_2['area'].sum() or 1
    price_py_2 = int(sum_price_2/sum_area_2)
    prices_py_2.append(price_py_2)

df_2 = pd.DataFrame(
    {'cat': list_cat, 'price_py': prices_py_2}).sort_values('price_py', ascending=False)

fig2 = go.Figure()
fig2.add_trace(go.Bar(name="전체", x=df_2['cat'], y=df_2['price_py']))


fig2.update_yaxes(title="단위: 원")
# 수정사항 끝

with st.expander(f"선택 지역: {selected_sido}", expanded=True):
    st.plotly_chart(fig2, theme='streamlit', use_container_width=True)
