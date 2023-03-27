import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 제목
st.title('가격별 물건 수 살펴보기')
st.text(' ')
# 데이터프레임 정의
df = pd.read_csv('./database/auction-items-nonan.csv')

list_var_kr = ['감정가', '최저입찰가']
dict_var = {'감정가': 'price_estimate', '최저입찰가': 'price_bidding',
            '유찰횟수': 'number_miss', '면적': 'area'}
selected_key = st.selectbox('관심 변수 선택', list_var_kr)

colA, colB = st.columns(2)
with colA:
    list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
    selected_sido = st.selectbox('지역(시도) 선택', list_sido)

with colB:
    price_start = 0
    price_end = 1000000000
    price_step = 1000000
    price_range = st.slider("가격 범위 선택", 0, 1000000000,
                            (price_start, price_end), price_step)
    price_min = price_range[0]
    price_max = price_range[1]

    # 폭 계산
    range_width = price_max - price_min

    # 각 구간의 폭 계산
    interval_width = range_width / 19

    # 20개의 원소를 가지는 리스트 초기화
    price_list = [price_min]
    for i in range(1, 20):
        next_price = price_min + interval_width * i
        price_list.append(next_price)

    def convertPrice(price):
        if price == 0:
            return str(price)
        if price >= 1000000 and price < 10000000:
            price = str(round(price/1000000, 1))+'백만'
            return price
        if price >= 10000000 and price < 100000000:
            price = str(round(price/10000000, 1))+'천만'
            return price
        if price > 100000000:
            price = str(round(price/100000000, 1))+'억'
            return price

with st.expander(f"{selected_sido} 기준 {selected_key} {convertPrice(price_min)}원부터 {convertPrice(price_max)}원 사이의 물건 수", expanded=True):
    df_price = df[df[dict_var[selected_key]] <= price_range[1]
                  ][df[dict_var[selected_key]] >= price_range[0]]

    if selected_sido != '전체 지역':
        df_price = df_price[df_price['address_sido'] == selected_sido]

    df_bin_estimate = df_price.groupby(
        pd.cut(df_price[dict_var[selected_key]], bins=20)).size().reset_index(name='number')
    df_bin_estimate = df_bin_estimate.reset_index()
    df_bin_estimate['index'] = df_bin_estimate['index']+1

    fig = px.bar(df_bin_estimate, x='index', y='number', text='number')

    list_price_range = [convertPrice(price_min), convertPrice(price_max*0.25), convertPrice(
        price_max * 0.5), convertPrice(price_max*0.75), convertPrice(price_max)]

    fig.update_xaxes(
        title_text=f'가격범위: 최소 {list_price_range[0]}원 ~ 최대 {list_price_range[-1]}원')
    fig.update_yaxes(title_text='물건 수')

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
