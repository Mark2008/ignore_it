import streamlit as st
import pandas as pd
import altair as alt

# 페이지 제목
st.set_page_config(page_title="국가별 MBTI 유형 분석", layout="centered")
st.title("🌍 국가별 MBTI 유형 분석 대시보드")

st.markdown("""
MBTI 유형별로 전 세계 국가들의 분포를 살펴보세요.  
특정 MBTI 유형을 선택하면, 그 유형의 비율이 높은 상위 10개 국가를 시각적으로 확인할 수 있습니다.
""")

df = pd.read_csv('countriesMBTI_16types.csv')

# 사용자 입력
mbti_types = [col for col in df.columns if col != 'Country']
selected_type = st.selectbox('🔍 분석할 MBTI 유형을 선택하세요:', mbti_types)

# 데이터 정렬 및 상위 10개 국가 추출
top10 = df[['Country', selected_type]].sort_values(by=selected_type, ascending=False).head(10)

# Altair 차트
chart = (
    alt.Chart(top10)
    .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
    .encode(
        x=alt.X(f'{selected_type}:Q', title=f'{selected_type} 비율 (%)'),
        y=alt.Y('Country:N', sort='-x', title='국가'),
        color=alt.Color(f'{selected_type}:Q', scale=alt.Scale(scheme='tealblues')),
        tooltip=['Country', selected_type]
    )
    .properties(
        width=600,
        height=400,
        title=f"🌟 {selected_type} 비율이 높은 국가 TOP 10"
    )
)

# 그래프 출력
st.altair_chart(chart, use_container_width=True)

# 세부 정보
st.markdown("📈 데이터 입력 가능합니다.")
uploaded = st.file_uploader("CSV 파일 업로드 (Country 열과 MBTI 유형 열이 포함되어야 합니다)", type=["csv"])

if uploaded is not None:
    user_df = pd.read_csv(uploaded)
    st.success("✅ CSV 파일이 업로드되었습니다!")
    if 'Country' in user_df.columns:
        if selected_type in user_df.columns:
            top10_user = user_df[['Country', selected_type]].sort_values(by=selected_type, ascending=False).head(10)
            chart_user = (
                alt.Chart(top10_user)
                .mark_bar(cornerRadiusTopLeft=8, cornerRadiusTopRight=8)
                .encode(
                    x=alt.X(f'{selected_type}:Q', title=f'{selected_type} 비율 (%)'),
                    y=alt.Y('Country:N', sort='-x', title='국가'),
                    color=alt.Color(f'{selected_type}:Q', scale=alt.Scale(scheme='tealblues')),
                    tooltip=['Country', selected_type]
                )
                .properties(title=f"📊 업로드한 데이터 기반 {selected_type} TOP 10")
            )
            st.altair_chart(chart_user, use_container_width=True)
        else:
            st.error(f"⚠️ 업로드한 CSV에 '{selected_type}' 열이 없습니다.")
    else:
        st.error("⚠️ 업로드한 CSV에 'Country' 열이 없습니다.")
