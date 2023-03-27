import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.graph_objects as go

st.title("관심 평균값 살펴보기")

df = pd.read_csv('./database/auction-items-nonan.csv')

list_var_kr = ['감정가', '최저입찰가', '유찰횟수', '면적']
dict_var = {'감정가': 'price_estimate', '최저입찰가': 'price_bidding',
            '유찰횟수': 'number_miss', '면적': 'area'}
selected_key = st.selectbox('관심 변수 선택', list_var_kr)

list_sido = ['전체 지역'] + df['address_sido'].unique().tolist()
list_cat = ['모든 종류'] + df['category'].unique().tolist()


st.subheader(f":chart_with_upwards_trend: 지역별 {selected_key} 평균값")
st.text('')

selected_cat = st.selectbox('카테고리 선택', list_cat)

means_sido = []
df_cat = df[df['category'] == selected_cat]
if selected_cat == '모든 종류':
    df_cat = df
for sido in list_sido:
    if sido == '전체 지역':
        mean = df[dict_var[selected_key]].mean()
    else:
        mean = df_cat[df_cat['address_sido'] ==
                      sido][dict_var[selected_key]].mean()
    means_sido.append(mean)

fig1 = go.Figure()

fig1.add_trace(go.Bar(name="전체", x=list_sido, y=means_sido))

fig1.add_hline(y=means_sido[0], line_width=2,  # 수정사항 : 굵기를 1에서 2로 변경하였습니다.
               line_color="darkgray",  # 수정사항 : 흰색으로 바꿔서 시인성을 높였습니다.
               # 수정사항 : 전국평균의 수치를 넣었습니다.
               annotation_text=f"전국 평균 {round(means_sido[0]/1e8, 2)}억",
               annotation_position="top right",
               annotation_font_size=12)  # 수정의견 : annotation_font = dict()를 통해 사이즈뿐만 아니라 '전국평균' 폰트의 굵기를 변경하려 했으나 오류가 발생하였습니다.
fig1.update_traces(marker_line_width=0.5, opacity=1)

# 수정사항 시작
min_val = 0
max_val = 8 * 1e8
tick_interval = 1 * 1e8

tickvals = list(range(int(min_val), int(max_val)+1, int(tick_interval)))
ticktext = [f"{round(val/1e8, 1)}" for val in tickvals]

fig1.update_yaxes(tickvals=tickvals, ticktext=ticktext, title="단위: 억원")
# 수정사항 끝


with st.expander(f"선택 카테고리: {selected_cat}", expanded=True):
    st.plotly_chart(fig1, theme='streamlit', use_container_width=True)

st.subheader(f":chart_with_upwards_trend: 물건 종류별 {selected_key} 평균값")
st.text('')

selected_sido = st.selectbox('지역(시도) 선택', list_sido)

means_cat = []
df_sido = df[df['address_sido'] == selected_sido]
if selected_cat == '모든 종류':
    df_sido = df
for cat in list_cat:
    if cat == '모든 종류':
        mean = df[dict_var[selected_key]].mean()
    else:
        mean = df_sido[df_sido['category'] ==
                       cat][dict_var[selected_key]].mean()
    means_cat.append(mean)

fig2 = go.Figure()

fig2.add_trace(go.Bar(name="전체", x=list_cat, y=means_cat))

fig2.add_hline(y=means_cat[0], line_width=2,  # 수정사항 : fig1과 동일
               line_color="darkgray",  # 수정사항 : fig1과 동일
               # 수정사항 : fig1과 동일
               annotation_text=f"전국 평균 {round(means_cat[0]/1e8, 2)}억",
               annotation_position="top right",
               annotation_font_size=12)
fig2.update_traces(marker_line_width=0.5, opacity=1)

# 수정사항 시작
min_val = 0
max_val = 15 * 1e8
tick_interval = 2 * 1e8

tickvals = list(range(int(min_val), int(max_val)+1, int(tick_interval)))
ticktext = [f"{round(val/1e8, 1)}" for val in tickvals]

fig2.update_yaxes(tickvals=tickvals, ticktext=ticktext, title="단위: 억원")
# 수정사항 끝

with st.expander(f"선택 지역: {selected_sido}", expanded=True):
    st.plotly_chart(fig2, theme='streamlit', use_container_width=True)
