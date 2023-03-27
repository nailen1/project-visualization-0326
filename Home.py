import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.express as px

# map
import json
import folium
from streamlit_folium import folium_static

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
        st.metric('전체 경매 물건 수', num_of_items+'개', "-0%",
                  delta_color="normal", help=None, label_visibility="visible")
    with col2:
        st.metric('경매 물건 감정가 총합', total_estimate+'원', "-0%",
                  delta_color="normal", help=None, label_visibility="visible")
    with col3:
        st.metric('평균 물건 입찰가 총합', total_bidding+'원', delta='-0%',
                  delta_color="normal", help=None, label_visibility="visible")
    with col4:
        st.metric('평균 유찰 횟수', mean_of_miss+'회', delta='0',
                  delta_color="normal", help=None, label_visibility="visible")

st.text('')
st.subheader(':chart_with_downwards_trend: 공판기일(날짜)별 물건 수')

with st.expander(f"공판기일(날짜) 기준 정보", expanded=True):
    tab_u, tab_v = st.tabs(["5일 이동평균선", "막대그래프"])

    df_date_line = df.groupby(
        'casedate_full').size().reset_index(name="number")
    df_date_line['date'] = pd.to_datetime(df_date_line['casedate_full'])

    fig31 = px.scatter(df_date_line, x="date", y="number", trendline="rolling",
                       trendline_options=dict(window=5))
    fig31.update_layout(xaxis=dict(rangeslider_visible=True))
    fig31.update_xaxes(title="공판기일")
    fig31.update_yaxes(title="물건 수")

    fig32 = px.bar(df_date_line, x="date", y="number")
    fig32.update_layout(xaxis=dict(rangeslider_visible=True))
    fig32.update_xaxes(title="공판기일")
    fig32.update_yaxes(title="물건 수")

    tab_u.plotly_chart(fig31, theme='streamlit', use_container_width=True)
    tab_v.plotly_chart(fig32, theme='streamlit', use_container_width=True)


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
    fig_a.update_layout(margin=dict(t=50, l=10, r=10, b=25))
    fig_a.update_layout(legend_title_text=selected_key)
    fig_a.update_layout(legend_orientation='h')
    # 차트 불러오기
    tab_a.plotly_chart(fig_a, theme=None, use_container_width=True)

    fig_b = px.treemap(df_p, path=['category', 'address_sido'], color=dict_var[selected_key],
                       color_continuous_scale='Blues',
                       )
    fig_b.update_layout(margin=dict(t=50, l=10, r=10, b=25))

    # 차트 불러오기
    tab_b.plotly_chart(fig_b, theme=None, use_container_width=True)


st.text('')
st.subheader(
    f":bar_chart: 부동산 경매 시장 히트맵")

with st.expander(f"지역-물건 종류 교차 정보", expanded=True):

    tab_c, tab_d, tab_e = st.tabs(["물건 수 기준", '감정가 기준', "최저입찰가 기준"])

    df_crosstab1 = pd.crosstab(df['category'], df['address_sido'])

    heatmap1 = px.imshow(df_crosstab1,
                         labels=dict(x="지역(시도)", y="물건 종류", color="물건 수"),
                         color_continuous_scale='Blues',
                         x=df.address_sido.unique(),
                         y=df.category.unique()
                         )

    heatmap1.update_xaxes(title=None)
    heatmap1.update_yaxes(title=None)
    # heatmap1.update_traces(showlegend=False, selector=dict(type='heatmap'))

    tab_c.plotly_chart(heatmap1, theme=None, use_container_width=True)

    df_crosstab4 = pd.crosstab(
        df['category'], df['address_sido'], values=df['price_estimate'], aggfunc='mean')

    heatmap2 = px.imshow(df_crosstab4,
                         labels=dict(x="지역(시도)", y="물건 종류",
                                     color="감정가 평균"),
                         color_continuous_scale='Blues',
                         x=df_crosstab4.columns,
                         y=df_crosstab4.index
                         )

    heatmap2.update_xaxes(title=None)
    heatmap2.update_yaxes(title=None)

    tab_d.plotly_chart(heatmap2, theme=None, use_container_width=True)

    df_crosstab3 = pd.crosstab(
        df['category'], df['address_sido'], values=df['price_bidding'], aggfunc='mean')

    heatmap3 = px.imshow(df_crosstab3,
                         labels=dict(x="지역(시도)", y="물건 종류",
                                     color="최저입찰가 평균"),
                         color_continuous_scale='Blues',
                         x=df_crosstab3.columns,
                         y=df_crosstab3.index
                         )

    heatmap3.update_xaxes(title=None)
    heatmap3.update_yaxes(title=None)

    tab_e.plotly_chart(heatmap3, theme=None, use_container_width=True)

# json파일
with open('./database/TL_SCCO_SIG_WGS84.json', 'r') as file:
    json_korea_sgg = json.load(file)
with open('./database/CTP_RVN_WGS84.json', 'r') as file:
    json_korea_sido = json.load(file)

# 데이터 로드
df = pd.read_csv('./database/auction-items-nonan.csv')
sgg_nm = pd.read_csv('./database/SGG_NM.csv', encoding='euc-kr')

# 시도코드 매기기
merged_df = pd.merge(df, sgg_nm, how='left', left_on=[
                     'address_sido', 'address_gugun'], right_on=['SIDO_NM', 'SGG_NM'])
merged_df = merged_df.drop(['SIDO_NM', 'SGG_NM'], axis=1)
merged_df.loc[merged_df['address_sido'] ==
              '세종특별자치시', 'CTPRVN_CD'] = 36  # 세종특별자치시 처리
merged_df.loc[merged_df['address_sido'] == '세종특별자치시', 'SIG_CD'] = 36110

# count열 생성
merged_df['count'] = 1

# 실행부분
merged_df_copy = merged_df.copy()

list_category = ['전체', '다가구주택', '아파트', '대지', '다세대', '상가', '임야',
                 '근린시설', '기타', '오피스텔', '연립주택', '단독주택', '전답']
list_sido = ['광역 선택', '서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
             '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도',
             '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도']
region_options = {
    '전국': ['서울특별시', '부산광역시', '대구광역시', '인천광역시', '광주광역시',
           '대전광역시', '울산광역시', '세종특별자치시', '경기도', '강원도', '충청북도', '충청남도',
           '전라북도', '전라남도', '경상북도', '경상남도', '제주특별자치도'],
    '서울특별시': ['강남구', '강동구', '강북구', '강서구', '관악구', '광진구', '구로구', '금천구', '노원구', '도봉구',
              '동대문구', '동작구', '마포구', '서대문구', '서초구', '성동구', '성북구', '송파구', '양천구', '영등포구',
              '용산구', '은평구', '종로구', '중구', '중랑구'],
    '부산광역시': ['강서구', '금정구', '기장군', '남구', '동구', '동래구', '부산진구', '북구', '사상구', '사하구',
              '서구', '수영구', '연제구', '영도구', '중구', '해운대구'],
    '대구광역시': ['남구', '달서구', '달성군', '동구', '북구', '서구', '수성구', '중구'],
    '인천광역시': ['강화군', '계양구', '남동구', '동구', '미추홀구', '부평구', '서구', '연수구', '옹진군', '중구'],
    '광주광역시': ['광산구', '남구', '동구', '북구', '서구'],
    '대전광역시': ['대덕구', '동구', '서구', '유성구', '중구'],
    '울산광역시': ['남구', '동구', '북구', '울주군', '중구'],
    '세종특별자치시': ['세종특별자치시'],
    '경기도': ['가평군', '고양시', '과천시', '광명시', '광주시', '구리시', '군포시', '김포시', '남양주시', '동두천시',
            '부천시', '성남시', '수원시', '시흥시', '안산시', '안성시', '안양시', '양주시', '양평군', '여주시',
            '연천군', '오산시', '용인시', '의왕시', '의정부시', '이천시', '파주시', '평택시', '포천시', '하남시', '화성시'],
    '강원도': ['강릉시', '고성군', '동해시', '삼척시', '속초시', '양구군', '양양군', '영월군', '원주시', '인제군', '정선군',
            '철원군', '춘천시', '태백시', '평창군', '홍천군', '화천군', '횡성군'],
    '충청북도': ['괴산군', '단양군', '보은군', '영동군', '옥천군', '음성군', '제천시', '증평군', '진천군', '청주시', '충주시'],
    '충청남도': ['계룡시', '공주시', '금산군', '논산시', '당진시', '보령시', '부여군', '서산시', '서천군', '아산시', '예산군',
             '천안시', '청양군', '태안군', '홍성군'],
    '전라북도': ['고창군', '군산시', '김제시', '남원시', '무주군', '부안군', '순창군', '완주군', '익산시', '임실군', '장수군',
             '전주시', '정읍시', '진안군'],
    '전라남도': ['강진군', '고흥군', '곡성군', '광양시', '구례군', '나주시', '담양군',
             '목포시', '무안군', '보성군', '순천시', '신안군', '여수시', '영광군',
             '영암군', '완도군', '장성군', '장흥군', '진도군', '함평군', '해남군', '화순군'],
    '경상북도': ['경산시', '경주시', '고령군', '구미시', '군위군', '김천시', '문경시',
             '봉화군', '상주시', '성주군', '안동시', '영덕군', '영양군', '영주시',
             '영천시', '예천군', '울릉군', '울진군', '의성군', '청도군', '청송군',
             '칠곡군', '포항시'],
    '경상남도': ['거제시', '거창군', '고성군', '김해시', '남해군', '밀양시', '사천시',
             '산청군', '양산시', '의령군', '진주시', '창녕군', '창원시', '통영시',
             '하동군', '함안군', '함양군', '합천군'],
    '제주특별자치도': ['제주시', '서귀포시']
}

# 각 도시의 중심점 위경도와 위도, 경도 범위
city_info = {
    '서울특별시': {
        'center': (37.566, 126.9784),
        'lat_range': (37.42, 37.7),
        'lon_range': (126.7, 127.2)
    },
    '부산광역시': {
        'center': (35.1796, 129.0756),
        'lat_range': (34.8, 35.5),
        'lon_range': (128.8, 129.5)
    },
    '대구광역시': {
        'center': (35.8714, 128.6014),
        'lat_range': (35.5, 36.2),
        'lon_range': (128.2, 129.0)
    },
    '인천광역시': {
        'center': (37.4563, 126.7052),
        'lat_range': (37.1, 37.8),
        'lon_range': (126.2, 127.2)
    },
    '광주광역시': {
        'center': (35.1606, 126.8514),
        'lat_range': (34.8, 35.5),
        'lon_range': (126.4, 127.3)
    },
    '대전광역시': {
        'center': (36.3504, 127.3845),
        'lat_range': (36.0, 36.7),
        'lon_range': (126.8, 127.8)
    },
    '울산광역시': {
        'center': (35.5384, 129.3114),
        'lat_range': (35.1, 35.9),
        'lon_range': (128.6, 129.9)
    },
    '세종특별자치시': {
        'center': (36.4803, 127.2891),
        'lat_range': (36.3, 36.7),
        'lon_range': (127.0, 127.6)
    },
    '경기도': {
        'center': (37.4138, 127.5183),
        'lat_range': (36.8, 38.0),
        'lon_range': (126.8, 128.5)
    },
    '강원도': {
        'center': (37.8856, 127.7306),
        'lat_range': (37.0, 38.8),
        'lon_range': (126.4, 129.3)
    },
    '충청북도': {
        'center': (36.6285, 127.9293),
        'lat_range': (36.0, 37.4),
        'lon_range': (126.8, 128.4)
    },
    '충청남도': {
        'center': (36.5184, 126.8006),
        'lat_range': (35.8, 36.8),
        'lon_range': (126.2, 127.4)
    },
    '전라북도': {
        'center': (35.7175, 127.153),
        'lat_range': (34.9, 36.3),
        'lon_range': (126.6, 128.2)
    },
    '전라남도': {
        'center': (34.816, 126.4627),
        'lat_range': (34.1, 35.5),
        'lon_range': (125.9, 127.6)
    },
    '경상북도': {
        'center': (36.4919, 128.8889),
        'lat_range': (35.5, 37.0),
        'lon_range': (127.6, 130.1)
    },
    '경상남도': {
        'center': (35.4606, 128.2132),
        'lat_range': (34.6, 36.1),
        'lon_range': (127.4, 129.6)
    },
    '제주특별자치도': {
        'center': (33.4996, 126.5312),
        'lat_range': (33.0, 34.0),
        'lon_range': (126.0, 127.0)
    }
}


st.subheader(':round_pushpin: 지도상의 물건 정보')

selected_category = st.selectbox('물건 종류 선택', list_category)
selected_sido = st.selectbox('지역(시도) 선택', list(region_options.keys()))

with st.expander(f"선택 물건: {selected_category}, 선택 지역: {selected_sido}", expanded=True):
    def create_map_figure(selected_df, geojson, region_cat, key_col, geo_key_col, city_info=None, selected_sido=None):
        grouped_df = selected_df.groupby(region_cat).agg(
            {'count': 'count', key_col: 'first'}).reset_index()
        grouped_df[key_col] = grouped_df[key_col].astype(int)
        grouped_df[key_col] = grouped_df[key_col].astype(str)
        grouped_df = grouped_df[[key_col, region_cat, 'count']]

        # geo_df = gpd.GeoDataFrame.from_features(geojson["features"])
        # geo_df = pd.merge(geo_df, grouped_df[[key_col, 'count']], left_on=geo_key_col, right_on=key_col, how="left")
        # geo_df['count'] = geo_df['count'].fillna(0)
        # geojson["features"] = geo_df.to_dict("records")

        latitude = 35.6
        longitude = 127.5

        m = folium.Map(location=[latitude, longitude],
                       zoom_start=6.5,
                       width=700, height=700,
                       tiles="cartodbdark_matter")

        folium.GeoJson(
            geojson,
            name='SIG_KOR_NM',
            # tooltip=folium.features.GeoJsonTooltip(fields=['SIG_KOR_NM' if geo_key_col=='SIG_CD' else 'CTP_KOR_NM', 'count'])
        ).add_to(m)

        m.choropleth(geo_data=geojson,
                     data=grouped_df,
                     columns=[f"{key_col}", 'count'],
                     fill_color='BuPu',
                     fill_opacity=0.8,
                     line_opacity=1.5,
                     key_on=f"properties.{geo_key_col}",
                     legend_name='물건수',
                     legend_font_color='white',
                     highlight=True)

        folium_static(m)

    if selected_category != '전체':
        # 카테고리 전체X, 지역 전국이라면
        if selected_sido == list(region_options.keys())[0]:
            selected_df = merged_df_copy[merged_df_copy['category']
                                         == selected_category]
            create_map_figure(selected_df, json_korea_sido,
                              'address_sido', 'CTPRVN_CD', 'CTPRVN_CD')
        else:  # 카테고리 전체X, 지역 특정광역이라면
            selected_df = merged_df_copy[merged_df_copy['category']
                                         == selected_category]
            selected_df = selected_df[selected_df['address_gugun'].isin(
                region_options[selected_sido])]
            create_map_figure(selected_df, json_korea_sgg, 'address_gugun',
                              'SIG_CD', 'SIG_CD', city_info, selected_sido)
    else:
        # 카테고리 전체O, 지역 전국이라면
        if selected_sido == list(region_options.keys())[0]:
            selected_df = merged_df_copy
            create_map_figure(selected_df, json_korea_sido,
                              'address_sido', 'CTPRVN_CD', 'CTPRVN_CD')
        else:  # 카테고리 전체O, 지역 특정광역이라면
            selected_df = merged_df_copy[merged_df_copy['address_gugun'].isin(
                region_options[selected_sido])]
            create_map_figure(selected_df, json_korea_sgg, 'address_gugun',
                              'SIG_CD', 'SIG_CD', city_info, selected_sido)
