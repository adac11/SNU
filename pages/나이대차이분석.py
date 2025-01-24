import koreanize_matplotlib
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind
from matplotlib import rc
from matplotlib import font_manager

# 한글 폰트 설정 (자동 폰트 설정)
try:
    font_path = font_manager.findfont(font_manager.FontProperties(family="NanumGothic"))
    rc('font', family='NanumGothic')
except:
    st.warning("한글 폰트를 찾을 수 없어 기본 설정으로 진행합니다.")
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

# Streamlit 앱 제목
st.title("나이대에 따른 스캔방향별 움직임 분석")

# 데이터 로드
@st.cache_data
def load_data():
    return pd.read_csv('Ch1-환자 움직임_최종.csv', encoding='cp949')

data = load_data()

# 나이대 범주화
def categorize_age(age):
    if age <= 39:
        return '30대 이하'
    elif age <= 49:
        return '40대'
    elif age <= 59:
        return '50대'
    elif age <= 69:
        return '60대'
    else:
        return '70대 이상'

data['나이대'] = data['나이'].apply(categorize_age)

# 데이터 확인
st.header("데이터 미리보기")
st.write(data.head())

# 나이대 및 스캔방향별 t-test 수행
st.header("나이대 및 스캔방향별 T-test 분석")
scan_directions = data['스캔방향'].unique()
age_groups = data['나이대'].unique()
test_results = []

for direction in scan_directions:
    for age_group in age_groups:
        group_data = data[data['스캔방향'] == direction]
        group_1 = group_data[group_data['나이대'] == age_group]['움직임_전체']
        group_others = group_data[group_data['나이대'] != age_group]['움직임_전체']
        t_stat, p_value = ttest_ind(group_1, group_others, nan_policy='omit')
        test_results.append({'스캔방향': direction, '나이대': age_group, 't-statistic': t_stat, 'p-value': p_value})

results_df = pd.DataFrame(test_results)
st.write(results_df)

# 나이대와 스캔방향별로 그룹화하여 '움직임_전체'의 평균 계산
st.header("나이대 및 스캔방향별 움직임 평균 분석")
grouped_data = data.groupby(['나이대', '스캔방향'])['움직임_전체'].mean().reset_index()
grouped_data.rename(columns={'움직임_전체': '평균 움직임'}, inplace=True)
st.write(grouped_data)

# 시각화
st.header("나이대 및 스캔방향별 움직임 시각화")
fig, ax = plt.subplots(figsize=(10, 8))
sns.barplot(data=grouped_data, x='스캔방향', y='평균 움직임', hue='나이대', ax=ax)

# p-value 추가
for i, direction in enumerate(scan_directions):
    for j, age_group in enumerate(age_groups):
        p_value = results_df[(results_df['스캔방향'] == direction) & (results_df['나이대'] == age_group)]['p-value'].values[0]
        ax.text(i + j * 0.1, grouped_data[(grouped_data['스캔방향'] == direction) & (grouped_data['나이대'] == age_group)]['평균 움직임'].max() + 0.02, 
                f"p={p_value:.3f}", ha='center', va='bottom', fontsize=9, color='red')

ax.set_title('나이대 및 스캔방향별 평균 움직임')
ax.set_ylabel('평균 움직임')
ax.set_xlabel('스캔방향')
st.pyplot(fig)

# 추가 분석: 데이터 설명
st.header("추가 데이터 설명")
with st.expander("데이터의 주요 특징"):
    st.markdown("- **나이대**: 30대 이하, 40대, 50대, 60대, 70대 이상\n- **스캔방향**: 스캔이 수행된 방향\n- **움직임_전체**: 움직임이 발생한 경우 1, 그렇지 않으면 0")
