import koreanize_matplotlib
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Streamlit 앱 제목
st.title("나이대별 스캔방향에 따른 움직임 분석 (2x2 카이제곱 검정)")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('Ch1-환자 움직임_최종.csv', encoding='cp949')

data = load_data()

# 나이대 생성
bins = [0, 39, 49, 59, 69, float('inf')]
labels = ['30대 이하', '40대', '50대', '60대', '70대 이상']
data['나이대'] = pd.cut(data['나이'], bins=bins, labels=labels)

# 나이대별 분석
st.header("나이대별 2x2 교차표 및 카이제곱 검정 결과")

age_groups = data['나이대'].unique()

for age_group in age_groups:
    st.subheader(f"나이대: {age_group}")
    
    # 해당 나이대 데이터 필터링
    age_group_data = data[data['나이대'] == age_group]
    
    # 2x2 교차표 생성
    contingency_table = pd.crosstab(age_group_data['스캔방향'], age_group_data['움직임_전체'])
    st.write(f"2x2 교차표 (스캔방향 vs 움직임):\n", contingency_table)
    
    # 카이제곱 검정
    if contingency_table.shape == (2, 2):  # 교차표가 2x2일 때만 수행
        chi2, p, dof, expected = chi2_contingency(contingency_table)
        st.write(f"카이제곱 통계량: {chi2:.3f}")
        st.write(f"p-value: {p:.3f}")
    else:
        st.write("데이터가 부족하여 카이제곱 검정을 수행할 수 없습니다.")
    
    # 시각화
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(contingency_table, annot=True, fmt="d", cmap="Blues", cbar=False, ax=ax)
    ax.set_title(f"2x2 교차표 (나이대: {age_group})")
    ax.set_xlabel("움직임 (0: 없음, 1: 있음)")
    ax.set_ylabel("스캔방향 (0, 1)")
    st.pyplot(fig)



