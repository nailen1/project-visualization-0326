import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title("지역별 물건 수 살펴보기")
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

list_address_sido = df['address_sido'].unique().tolist()
list_category = df['category'].unique().tolist()

st.subheader(f"시/도 단위 부동산 물건 수")

colA, colB = st.columns(2)
with colA:
    with st.expander(f"관심 지역 선택 (전국 {len(list_address_sido)}개 시도)"):
        selected_sidos = st.multiselect(
            "", options=list_address_sido, default=list_address_sido)

with colB:
    with st.expander(f"관심 카테고리 선택 (총 {len(list_category)}종)"):
        selected_cats = st.multiselect(
            "", options=list_category, default=list_category)

df_selected = df[df['address_sido'].isin(selected_sidos)]

with st.expander(f"선택 지역: {len(selected_sidos)}개, 선택 카테고리: {len(selected_cats)}개", expanded=True):

    cat_living = ['다가구주택', '아파트', '다세대', '연립주택', '단독주택']
    cat_comm = ['상가', '근린시설', '오피스텔', '기타']
    cat_terri = ['대지', '임야', '전답']

    tab_a, tab_b, tab_c, tab_d = st.tabs(
        ["주거용", "상업용", "토지", "관심 종류"])

    df_sido_total = df_selected.groupby(
        'address_sido').size().reset_index(name="number")

    df_sido_cat = df_selected[df_selected['category'].isin(cat_living)].groupby(
        'address_sido').size().reset_index(name="number")

    list_sido = df_sido_total['address_sido'].unique().tolist()

    y11 = df_sido_total['number'].values.tolist()
    y12 = df_sido_cat['number'].values.tolist()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="전체", x=list_sido, y=y11, text=y11))
    fig1.add_trace(go.Bar(
        name=f"선택된 카테고리 {cat_living[:3]} 등 주거용 {len(cat_living)}종", x=list_sido, y=y12, text=y12))

    fig1.update_traces(textfont_size=12, textangle=90,
                       textposition="outside", cliponaxis=False)

    fig1.update_traces(marker_line_width=0.5, opacity=1)

    fig1.update_xaxes(title_text='지역명')
    fig1.update_yaxes(title_text='물건 수')

    fig1.update_layout(legend_orientation="h",
                       legend_valign="top",
                       legend_x=0,
                       legend_y=1.2,
                       legend_entrywidthmode='fraction',
                       legend_entrywidth=1)

    tab_a.plotly_chart(fig1, theme='streamlit', use_container_width=True)

    df_sido_cat = df_selected[df_selected['category'].isin(cat_comm)].groupby(
        'address_sido').size().reset_index(name="number")

    list_sido = df_sido_total['address_sido'].unique().tolist()

    y11 = df_sido_total['number'].values.tolist()
    y12 = df_sido_cat['number'].values.tolist()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="전체", x=list_sido, y=y11, text=y11))
    fig1.add_trace(go.Bar(
        name=f"선택된 카테고리 {cat_comm[:3]} 등 상업용 {len(cat_comm)}종", x=list_sido, y=y12, text=y12))

    fig1.update_traces(textfont_size=12, textangle=90,
                       textposition="outside", cliponaxis=False)

    fig1.update_traces(marker_line_width=0.5, opacity=1)

    fig1.update_xaxes(title_text='지역명')
    fig1.update_yaxes(title_text='물건 수')

    fig1.update_layout(legend_orientation="h",
                       legend_valign="top",
                       legend_x=0,
                       legend_y=1.2,
                       legend_entrywidthmode='fraction',
                       legend_entrywidth=1)

    tab_b.plotly_chart(fig1, theme='streamlit', use_container_width=True)

    df_sido_cat = df_selected[df_selected['category'].isin(cat_terri)].groupby(
        'address_sido').size().reset_index(name="number")

    list_sido = df_sido_total['address_sido'].unique().tolist()

    y11 = df_sido_total['number'].values.tolist()
    y12 = df_sido_cat['number'].values.tolist()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="전체", x=list_sido, y=y11, text=y11))
    fig1.add_trace(go.Bar(
        name=f"선택된 카테고리 {cat_terri[:3]} 등 토지 {len(cat_terri)}종", x=list_sido, y=y12, text=y12))

    fig1.update_traces(textfont_size=12, textangle=90,
                       textposition="outside", cliponaxis=False)

    fig1.update_traces(marker_line_width=0.5, opacity=1)

    fig1.update_xaxes(title_text='지역명')
    fig1.update_yaxes(title_text='물건 수')

    fig1.update_layout(legend_orientation="h",
                       legend_valign="top",
                       legend_x=0,
                       legend_y=1.2,
                       legend_entrywidthmode='fraction',
                       legend_entrywidth=1)

    tab_c.plotly_chart(fig1, theme='streamlit', use_container_width=True)

    df_sido_cat = df_selected[df_selected['category'].isin(selected_cats)].groupby(
        'address_sido').size().reset_index(name="number")

    list_sido = df_sido_total['address_sido'].unique().tolist()

    y11 = df_sido_total['number'].values.tolist()
    y12 = df_sido_cat['number'].values.tolist()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(name="전체", x=list_sido, y=y11, text=y11))
    fig1.add_trace(go.Bar(
        name=f"선택된 카테고리 {selected_cats[:3]} 등 {len(selected_cats)}종", x=list_sido, y=y12, text=y12))

    fig1.update_traces(textfont_size=12, textangle=90,
                       textposition="outside", cliponaxis=False)

    fig1.update_traces(marker_line_width=0.5, opacity=1)

    fig1.update_xaxes(title_text='지역 이름)')
    fig1.update_yaxes(title_text='물건 수')

    fig1.update_layout(legend_orientation="h",
                       legend_valign="top",
                       legend_x=0,
                       legend_y=1.2,
                       legend_entrywidthmode='fraction',
                       legend_entrywidth=1)

    tab_d.plotly_chart(fig1, theme='streamlit', use_container_width=True)


st.subheader(f"구/군 단위 부동산 물건 수")

with st.expander(f"세부 지역 단위", expanded=True):

    colC, colD = st.columns(2)
    with colC:
        selected_sido_2 = st.selectbox("시도 선택: ", list_address_sido)
    with colD:
        selected_cat_2 = st.selectbox("물건 종류 선택: ", list_category)

    df_gugun_total = df[df['address_sido'] == selected_sido_2].groupby(
        'address_gugun').size().reset_index(name="number")
    list_gugun = df_gugun_total['address_gugun'].unique().tolist()

    df_sido = df[df['address_sido'] == selected_sido_2]
    df_gugun_cat = df_sido[df_sido['category'] == selected_cat_2].groupby(
        'address_gugun').size().reset_index(name="number")
    df_gugun_zero = pd.DataFrame(
        {'address_gugun': list_gugun, 'number': [0]*len(list_gugun)})
    merged_df = pd.merge(df_gugun_zero, df_gugun_cat, how='outer',
                         on='address_gugun').fillna(0).drop(['number_x'], axis=1)

    number_gugun_total = df_gugun_total['number'].values.tolist()
    number_gugun_cat = merged_df['number_y'].values.tolist()

    fig = go.Figure()

    x = list_gugun
    y1 = number_gugun_total
    y2 = number_gugun_cat

    fig.add_trace(go.Bar(name="전체", x=x, y=y1))
    fig.add_trace(go.Bar(name=selected_cat_2, x=x, y=y2))

    fig.update_traces(textfont_size=12, textangle=90,
                      textposition="outside", cliponaxis=False)

    fig.update_traces(marker_line_width=0.5, opacity=1)

    fig.update_xaxes(title_text='지역명')
    fig.update_yaxes(title_text='물건 수')

    fig.update_layout(legend_orientation="h",
                      legend_valign="top",
                      legend_x=0,
                      legend_y=1.2,
                      legend_entrywidthmode='fraction',
                      legend_entrywidth=1)

    st.plotly_chart(fig, theme='streamlit', use_container_width=True)
