import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit 앱 제목
st.title("성별에 따른 스캔방향별 움직임 분석")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('Ch1-환자 움직임_최종.csv')

data = load_data()

# 데이터 확인
st.header("데이터 미리보기")
st.write(data.head())

# 성별과 스캔방향별로 그룹화하여 '움직임_전체'의 평균 계산
st.header("성별 및 스캔방향별 움직임 평균 분석")
grouped_data = data.groupby(['성별', '스캔방향'])['움직임_전체'].mean().reset_index()
grouped_data.rename(columns={'움직임_전체': '평균 움직임'}, inplace=True)
st.write(grouped_data)

# 시각화
st.header("성별 및 스캔방향별 움직임 시각화")
fig, ax = plt.subplots(figsize=(8, 6))
sns.barplot(data=grouped_data, x='스캔방향', y='평균 움직임', hue='성별', ax=ax)
ax.set_title('성별 및 스캔방향별 평균 움직임')
ax.set_ylabel('평균 움직임')
ax.set_xlabel('스캔방향')
st.pyplot(fig)

# 추가 분석: 데이터 설명
st.header("추가 데이터 설명")
with st.expander("데이터의 주요 특징"):
    st.markdown("- **성별**: M(남성), F(여성)\n- **스캔방향**: 스캔이 수행된 방향\n- **움직임_전체**: 움직임이 발생한 경우 1, 그렇지 않으면 0")

