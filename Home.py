import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Auction items data dashboard",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
    }
)

st.title("법원 부동산 경매 데이터")
st.text('')

df = pd.read_csv('./database/auction-items-nonan.csv')

num_of_items = str(df.shape[0])
mean_of_miss = str(round(df['number_miss'].mean(), 1))


def convertPrice(price):
    if price == 0:
        return price
    if price >= 1000000 and price < 10000000:
        price = str(round(price/1000000, 1))+'백만'
        return price
    if price >= 10000000 and price < 100000000:
        price = str(round(price/10000000, 1))+'천만'
        return price
    if price > 100000000 and price < 1000000000000:
        price = str(round(price/100000000, 1))+'억'
    if price > 1000000000000 and price < 10000000000000000:
        price = str(round(price/1000000000000, 1))+'조'
        return price


total_estimate = convertPrice(df['price_estimate'].sum())
total_bidding = convertPrice(df['price_bidding'].sum())

date_min = min(df['casedate_full'].unique().tolist())
date_max = max(df['casedate_full'].unique().tolist())

st.subheader(
    f":chart_with_upwards_trend: 부동산 경매 시장 동향")
# st.text('')

# st.markdown("---")
with st.expander("요약 정보", expanded=True):
    st.metric('기간', f'{date_min} ~ {date_max}',
              delta_color="normal", help=None, label_visibility="visible")
    st.text('')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('전체 경매 물건 수', num_of_items+'개', "-3%",
                  delta_color="normal", help=None, label_visibility="visible")
    with col2:
        st.metric('경매 물건 감정가 총합', total_estimate+'원', "-8%",
                  delta_color="normal", help=None, label_visibility="visible")
    with col3:
        st.metric('평균 물건 입찰가 총합', total_bidding+'원', delta='-5%',
                  delta_color="normal", help=None, label_visibility="visible")
    with col4:
        st.metric('평균 유찰 횟수', mean_of_miss+'회', delta='0',
                  delta_color="normal", help=None, label_visibility="visible")

st.text('')
st.subheader(':chart_with_downwards_trend: 공판기일(날짜)별 물건 수')

with st.expander(f"5일 이동 평균선", expanded=True):
    df_date_line = df.groupby(
        'casedate_full').size().reset_index(name="number")
    df_date_line['date'] = pd.to_datetime(df_date_line['casedate_full'])

    fig3 = px.scatter(df_date_line, x="date", y="number", trendline="rolling",
                      trendline_options=dict(window=5))
    fig3.update_layout(xaxis=dict(rangeslider_visible=True))

    st.plotly_chart(fig3, theme='streamlit', use_container_width=True)

st.text('')
st.subheader(
    f":bar_chart: 부동산 경매 시장 계층 구조")

list_var_kr = ['감정가', '경매 시작가', '유찰횟수', '면적']
dict_var = {'감정가': 'price_estimate', '경매 시작가': 'price_bidding',
            '유찰횟수': 'number_miss', '면적': 'area'}

selected_key = st.selectbox('관심 변수 선택', list_var_kr)

with st.expander(f"트리맵: {selected_key}", expanded=True):
    ones = pd.DataFrame(np.ones(5812, dtype=int)).rename(columns={0: 'pop'})
    df_p = pd.concat([df, ones], axis=1)

    tab_a, tab_b = st.tabs(["지역 기준", "물건 종류 기준"])

    fig_a = px.treemap(df_p, path=['address_sido', 'category'], color=dict_var[selected_key],
                       color_continuous_scale='Blues',
                       )
    fig_a.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # 차트 불러오기
    tab_a.plotly_chart(fig_a, theme=None, use_container_width=True)

    fig_b = px.treemap(df_p, path=['category', 'address_sido'], color=dict_var[selected_key],
                       color_continuous_scale='Blues',
                       )
    fig_b.update_layout(margin=dict(t=50, l=25, r=25, b=25))

    # 차트 불러오기
    tab_b.plotly_chart(fig_b, theme=None, use_container_width=True)


st.text('')
st.subheader(
    f":bar_chart: 부동산 경매 시장 히트맵")

with st.expander(f"지역-물건 종류 교차 정보", expanded=True):

    tab_c, tab_d, tab_e = st.tabs(["물건 수 기준", '감정가 기준', "경매 시작가 기준"])

    df_crosstab1 = pd.crosstab(df['category'], df['address_sido'])

    heatmap1 = px.imshow(df_crosstab1,
                         labels=dict(x="지역(시도)", y="물건 종류", color="물건 수"),
                         color_continuous_scale='Blues',
                         x=df.address_sido.unique(),
                         y=df.category.unique()
                         )

    tab_c.plotly_chart(heatmap1, theme=None, use_container_width=True)

    df_crosstab4 = pd.crosstab(
        df['category'], df['address_sido'], values=df['price_estimate'], aggfunc='mean')

    heatmap4 = px.imshow(df_crosstab4,
                         labels=dict(x="지역(시도)", y="물건 종류",
                                     color="감정가 평균"),
                         color_continuous_scale='Blues',
                         x=df_crosstab4.columns,
                         y=df_crosstab4.index
                         )

    tab_d.plotly_chart(heatmap4, theme=None, use_container_width=True)

    df_crosstab3 = pd.crosstab(
        df['category'], df['address_sido'], values=df['price_bidding'], aggfunc='mean')

    heatmap3 = px.imshow(df_crosstab3,
                         labels=dict(x="지역(시도)", y="물건 종류",
                                     color="경매 시작가 평균"),
                         color_continuous_scale='Blues',
                         x=df_crosstab3.columns,
                         y=df_crosstab3.index
                         )

    tab_e.plotly_chart(heatmap3, theme=None, use_container_width=True)
