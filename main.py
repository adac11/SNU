import koreanize_matplotlib
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Streamlit 앱 제목
st.title("성별에 따른 스캔방향별 움직임 분석")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('Ch1-환자 움직임_최종.csv', encoding='cp949')

data = load_data()

# 데이터 확인
st.header("데이터 미리보기")
st.write(data.head())

# 성별 및 스캔방향별 카이제곱 테스트
st.header("성별 및 스캔방향별 카이제곱 테스트")
scan_directions = data['스캔방향'].unique()
gender_results = []

for direction in scan_directions:
    contingency_table = pd.crosstab(data[data['스캔방향'] == direction]['성별'], 
                                    data[data['스캔방향'] == direction]['움직임_전체'])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    gender_results.append({'스캔방향': direction, '카이제곱 통계량': chi2, 'p-value': p})

gender_results_df = pd.DataFrame(gender_results)
st.write(gender_results_df)

# 성별 및 스캔방향별 움직임 시각화
st.header("성별 및 스캔방향별 움직임 시각화")
grouped_data = data.groupby(['성별', '스캔방향'])['움직임_전체'].mean().reset_index()
grouped_data.rename(columns={'움직임_전체': '평균 움직임'}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=grouped_data, x='스캔방향', y='평균 움직임', hue='성별', ax=ax)

# p-value 추가
for i, direction in enumerate(scan_directions):
    p_value = gender_results_df[gender_results_df['스캔방향'] == direction]['p-value'].values[0]
    ax.text(i, grouped_data[grouped_data['스캔방향'] == direction]['평균 움직임'].max() + 0.02, 
            f"p={p_value:.3f}", ha='center', va='bottom', fontsize=9, color='red')

ax.set_title('성별 및 스캔방향별 평균 움직임')
ax.set_ylabel('평균 움직임')
ax.set_xlabel('스캔방향')
st.pyplot(fig)
