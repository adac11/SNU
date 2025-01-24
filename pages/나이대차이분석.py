import koreanize_matplotlib
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Streamlit 앱 제목
st.title("나이대별 스캔방향별 움직임 분석")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('Ch1-환자 움직임_최종.csv', encoding='cp949')

data = load_data()

# 나이대 생성
bins = [0, 39, 49, 59, 69, float('inf')]
labels = ['30대 이하', '40대', '50대', '60대', '70대 이상']
data['나이대'] = pd.cut(data['나이'], bins=bins, labels=labels)

# 나이대별 데이터 분석
st.header("나이대별 분석 결과")
age_groups = data['나이대'].unique()

for age_group in age_groups:
    st.subheader(f"나이대: {age_group}")
    
    # 해당 나이대 데이터 필터링
    age_group_data = data[data['나이대'] == age_group]
    scan_directions = age_group_data['스캔방향'].unique()
    
    # 카이제곱 테스트
    chi2_results = []
    for direction in scan_directions:
        contingency_table = pd.crosstab(age_group_data[age_group_data['스캔방향'] == direction]['움직임_전체'],
                                        age_group_data[age_group_data['스캔방향'] == direction]['나이대'])
        if contingency_table.shape == (2, 1):  # 데이터가 부족하면 카이제곱 불가능
            chi2, p = None, None
        else:
            chi2, p, _, _ = chi2_contingency(contingency_table)
        chi2_results.append({'스캔방향': direction, '카이제곱 통계량': chi2, 'p-value': p})
    
    # 결과 테이블 표시
    chi2_results_df = pd.DataFrame(chi2_results)
    st.write(chi2_results_df)
    
    # 움직임 평균 계산
    avg_movement = age_group_data.groupby('스캔방향')['움직임_전체'].mean().reset_index()
    avg_movement.rename(columns={'움직임_전체': '평균 움직임'}, inplace=True)
    
    # 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(data=avg_movement, x='스캔방향', y='평균 움직임', ax=ax)
    
    # p-value 추가
    for i, row in avg_movement.iterrows():
        direction = row['스캔방향']
        p_value = chi2_results_df[chi2_results_df['스캔방향'] == direction]['p-value'].values[0]
        if p_value is not None:
            ax.text(i, row['평균 움직임'] + 0.02, f"p={p_value:.3f}", ha='center', va='bottom', fontsize=9, color='red')
    
    ax.set_title(f"{age_group} 스캔방향별 평균 움직임")
    ax.set_ylabel('평균 움직임')
    ax.set_xlabel('스캔방향')
    st.pyplot(fig)

