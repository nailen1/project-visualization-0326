import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# 물건종류
st.title("유찰횟수별 지역/물건종류 정보 살펴보기")
st.text('')

list_sido = [
    '전체 지역',
    '서울특별시',
    '부산광역시',
    '대구광역시',
    '인천광역시',
    '광주광역시',
    '대전광역시',
    '울산광역시',
    '세종특별자치시',
    '경기도',
    '강원도',
    '충청북도',
    '충청남도',
    '전라북도',
    '전라남도',
    '경상북도',
    '경상남도',
    '제주특별자치도']


df = pd.read_csv('./database/auction-items-nonan.csv')

# 유찰횟수
list_number_miss = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
# 전체
category_total = ['다가구주택', '아파트', '다세대', '연립주택', '단독주택',
                  '대지', '임야', '전답', '상가', '근린시설', '오피스텔', '기타']
# 주거용
category_living = ['다가구주택', '아파트', '다세대', '연립주택', '단독주택']
# 상업용
category_comm = ['상가', '근린시설', '오피스텔', '기타']
# 토지
category_terri = ['대지', '임야', '전답']
# category 종류
category_jongryu = ['개별(13 종)', '그룹별(3 종)']

df['cat_3'] = '토지'  # 기본값은 '토지'로 설정
df.loc[df['category'].isin(category_living), 'cat_3'] = '주거용'
df.loc[df['category'].isin(category_comm), 'cat_3'] = '상업용'
df_orign = df.copy()
df_total = df.copy()

selected_sidos = st.selectbox('관심지역 선택(시도)', list_sido)

st.subheader('유찰횟수별 물건수')
# df를 선택된 지역에 맞춰서 뽑아내기
if selected_sidos != '전체 지역':
    df = df[df['address_sido'] == selected_sidos]

new_df = df.groupby('number_miss')[
    'category', 'cat_3'].size().reset_index(name='count')
df_total = df_total.groupby('number_miss').size().reset_index(name='count')

# '전체 지역' 페이지 1. 전국 유찰횟수 물건 수 비교 bar chart
if selected_sidos == '전체 지역':
    with st.expander(f"전체지역: 유찰횟수별 물건 수 비교", expanded=True):
        fig = px.bar(new_df, x='number_miss', y='count')
        fig.update_traces(marker_line_width=0.5, opacity=1)
        fig.update_xaxes(title_text='유찰횟수')
        fig.update_yaxes(title_text='물건 수')
        fig.update_layout(legend_orientation="h",
                          legend_valign="top",
                          legend_x=0, legend_y=1.2,
                          legend_entrywidthmode='fraction',
                          legend_entrywidth=1)
        st.plotly_chart(fig, theme='streamlit', use_container_width=True)

    with st.expander(f"전체지역 유찰횟수별 물건 수 비교", expanded=True):
        df_crosstab1 = pd.crosstab(
            df_orign['number_miss'], df_orign['address_sido'])
        fig = px.density_heatmap(
            df_orign, x='address_sido', y='number_miss', color_continuous_scale='Blues')
        fig.update_layout(xaxis=dict(
            tickangle=30, title_standoff=100), yaxis=dict(title_standoff=10))

        st.plotly_chart(fig, theme=None, use_container_width=True)

# '선택 지역' 페이지 1. 전국/선택지역 유찰횟수 물건 수 비교 bar chart
if selected_sidos != '전체 지역':
    with st.expander(f"{selected_sidos}: 유찰횟수별 물건 수 비교", expanded=True):
        # 전체_선택지역 유찰횟수 비교
        fig = go.Figure()

        x = df_total['number_miss']
        y1 = df_total['count']
        y2 = new_df['count']

        fig.add_trace(go.Bar(name="전체지역", x=x, y=y1))
        fig.add_trace(go.Bar(name="관심지역", x=x, y=y2))
        fig.update_traces(textfont_size=12, textangle=90,
                          textposition="outside", cliponaxis=False)
        fig.update_traces(marker_line_width=0.5, opacity=1)
        fig.update_xaxes(title_text='유찰횟수')
        fig.update_yaxes(title_text='물건 수')
        fig.update_layout(legend_orientation="h",
                          legend_valign="top",
                          legend_x=0, legend_y=1.2,
                          legend_entrywidthmode='fraction',
                          legend_entrywidth=1)

        st.plotly_chart(fig, theme='streamlit', use_container_width=True)


st.subheader('유찰횟수에 따른 물건종류별 물건수 비교')
with st.expander(f"{selected_sidos}: 유찰횟수에 따른 물건종류별 물건수 비교", expanded=True):
    tab_0, tab_a = st.tabs(
        ["유찰횟수", "유찰여부"])
    # sunburst
    df = df.groupby('number_miss')[
        'category', 'cat_3'].value_counts().reset_index(name='count')
    fig = px.sunburst(
        df, path=['number_miss', 'cat_3', 'category'], values='count')

    tab_0.plotly_chart(fig, theme='streamlit', use_container_width=True)

    # cat_3 방사형
    df_miss_e = df.copy()
    df_miss_e['number_miss'] = df_miss_e['number_miss'].replace(
        df_miss_e[df_miss_e['number_miss'] >= 1]['number_miss'].values, 'miss')
    df_miss_0 = df_miss_e[df_miss_e['number_miss'] == 0]
    df_miss_yes = df_miss_e[df_miss_e['number_miss'] == 'miss']
    df_count_miss_0 = df_miss_0.groupby(
        ['cat_3', 'number_miss']).size().reset_index(name='count')
    df_count_miss_yes = df_miss_yes.groupby(
        ['cat_3', 'number_miss']).size().reset_index(name='count')
    df_count_miss_0yes = pd.concat([df_count_miss_0, df_count_miss_yes])
    fig = px.line_polar(df_count_miss_0yes, r='count',
                        theta='cat_3', color='number_miss', line_close=True)
    fig.update_traces(fill='none')

    tab_a.plotly_chart(fig, theme='streamlit', use_container_width=True)
