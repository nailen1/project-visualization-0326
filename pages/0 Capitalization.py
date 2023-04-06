import streamlit as st
import plotly.express as px
import pandas as pd


def openDataFrame(path):
    return pd.read_csv(path, on_bad_lines='skip', encoding="utf-8")


df = openDataFrame("./database/auction-items-nonan.csv")
st.title(f'부동산 경매 시장 전체 규모(Capitalization)')

list_var_kr = ['감정가', '최저입찰가']
dict_var = {'감정가': 'price_estimate', '최저입찰가': 'price_bidding',
            '유찰횟수': 'number_miss', '면적': 'area'}
selected_key = st.selectbox('관심 변수 선택', list_var_kr)

list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
list_cat = ['모든 종류'] + df['category'].unique().tolist()

st.subheader(f'물건 종류별 {selected_key} 총합')

selected_sido = st.selectbox('지역(시도) 선택', list_sido)

df_sido = df
if selected_sido != '전체 지역':
    df_sido = df[df['address_sido'] == selected_sido]

df_sorted_sido = df_sido.sort_values(
    by=dict_var[selected_key], ascending=False)
fig_a = px.bar(df_sorted_sido, y="category", x=dict_var[selected_key], color="category",
               color_discrete_sequence=px.colors.qualitative.G10)
fig_a.update_xaxes(title="단위: 원")
fig_a.update_yaxes(title=None)

with st.expander(f'{selected_sido} 기준', expanded=True):
    st.plotly_chart(fig_a)


st.subheader(f'지역별 {selected_key} 총합')

df_cat = df
selected_cat = st.selectbox('물건 종류 선택', list_cat)

if selected_cat != '모든 종류':
    df_cat = df[df['category'] == selected_cat]

df_sorted_cat = df_cat.sort_values(by=dict_var[selected_key], ascending=False)
fig_b = px.bar(df_sorted_cat, y="address_sido", x=dict_var[selected_key], color="address_sido",
               color_discrete_sequence=px.colors.qualitative.G10)
fig_b.update_xaxes(title="단위: 원")
fig_b.update_yaxes(title=None)

with st.expander(f'{selected_cat} 기준', expanded=True):
    st.plotly_chart(fig_b)
