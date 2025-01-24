import koreanize_matplotlib
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Streamlit 앱 제목
st.title("나이대에 따른 스캔방향별 움직임 분석")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('Ch1-환자 움직임_최종.csv', encoding='cp949')

data = load_data()

# 나이대 생성
bins = [0, 39, 49, 59, 69, float('inf')]
labels = ['30대 이하', '40대', '50대', '60대', '70대 이상']
data['나이대'] = pd.cut(data['나이'], bins=bins, labels=labels)

# 데이터 확인
st.header("데이터 미리보기")
st.write(data.head())

# 나이대 및 스캔방향별 카이제곱 테스트
st.header("나이대 및 스캔방향별 카이제곱 테스트")
scan_directions = data['스캔방향'].unique()
age_results = []

for direction in scan_directions:
    contingency_table = pd.crosstab(data[data['스캔방향'] == direction]['나이대'], 
                                    data[data['스캔방향'] == direction]['움직임_전체'])
    chi2, p, _, _ = chi2_contingency(contingency_table)
    age_results.append({'스캔방향': direction, '카이제곱 통계량': chi2, 'p-value': p})

age_results_df = pd.DataFrame(age_results)
st.write(age_results_df)

# 나이대 및 스캔방향별 움직임 시각화
st.header("나이대 및 스캔방향별 움직임 시각화")
grouped_data = data.groupby(['나이대', '스캔방향'])['움직임_전체'].mean().reset_index()
grouped_data.rename(columns={'움직임_전체': '평균 움직임'}, inplace=True)

fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=grouped_data, x='스캔방향', y='평균 움직임', hue='나이대', ax=ax)

# p-value 추가
for i, direction in enumerate(scan_directions):
    p_value = age_results_df[age_results_df['스캔방향'] == direction]['p-value'].values[0]
    ax.text(i, grouped_data[grouped_data['스캔방향'] == direction]['평균 움직임'].max() + 0.02, 
            f"p={p_value:.3f}", ha='center', va='bottom', fontsize=9, color='red')

ax.set_title('나이대 및 스캔방향별 평균 움직임')
ax.set_ylabel('평균 움직임')
ax.set_xlabel('스캔방향')
st.pyplot(fig)
