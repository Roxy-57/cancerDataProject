import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rc('font', family='NanumBarunGothic')
plt.rcParams['axes.unicode_minus'] = False  # 한글 변환 시 - 표기가 깨짐 방지

# 파일 불러오기
data = pd.read_csv('cancer.csv', encoding='cp949')

years = data['연도'].unique()
regions = data['시도'].unique()

# 전국 데이터만 가져오기
nationwide_data = data[data['시도'] == '전국 Whole country']

# 그래프 생성 (시도별 그래프 + 전국 데이터 비교 그래프)
fig, axes = plt.subplots(nrows=len(years) + 1, ncols=1, figsize=(14, (len(years) + 1) * 6))

# 연도별 시도별 그래프 생성
for i in range(len(years)):
    year = years[i]  # 인덱스를 사용하여 연도 가져오기
    subset = data[data['연도'] == year]
    index = np.arange(len(subset))
    width = 0.4  # 남녀 막대가 겹치지 않도록

    ax = axes[i]  # 각 연도에 대해 개별 그래프
    men_bars = ax.bar(index - width / 2, subset['남자 암발생자수(명)'], width, color='blue', label='Men')
    women_bars = ax.bar(index + width / 2, subset['여자 암발생자수(명)'], width,color='tomato', label='Women')

    # 그래프 스타일링
    ax.set_title(f'{year}년 연도별 시도 남녀 암발생자수', fontsize=16)
    ax.set_ylabel('암발생자수(명)', fontsize=14)
    ax.set_xlabel('시도', fontsize=14)
    ax.set_xticks(index)
    ax.set_xticklabels(subset['시도'], rotation=45)
    ax.legend()

    # 남성 암발생자수 텍스트 표시
    for bar in men_bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=8)

    # 여성 암발생자수 텍스트 표시
    for bar in women_bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=8)

# 전국 데이터 비교 그래프 생성
ax_nationwide = axes[-1]  # 마지막에 전국 데이터를 추가하기위한 코드
nationwide_men_bars = ax_nationwide.bar(np.arange(len(nationwide_data)) - width / 2, nationwide_data['남자 암발생자수(명)'], width, color='blue', label='Men')
nationwide_women_bars = ax_nationwide.bar(np.arange(len(nationwide_data)) + width / 2, nationwide_data['여자 암발생자수(명)'], width, color='tomato', label='Women')

# 전국 그래프 스타일링
ax_nationwide.set_title('연도별 전국 남녀 암발생자수 비교', fontsize=16)
ax_nationwide.set_ylabel('암발생자수(명)', fontsize=14)
ax_nationwide.set_xlabel('연도', fontsize=14)
ax_nationwide.set_xticks(np.arange(len(nationwide_data)))
ax_nationwide.set_xticklabels(nationwide_data['연도'])
ax_nationwide.legend()

# 전국 남성 암발생자수 텍스트 표시
for bar in nationwide_men_bars:
    yval = bar.get_height()
    ax_nationwide.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=6)

# 전국 여성 암발생자수 텍스트 표시
for bar in nationwide_women_bars:
    yval = bar.get_height()
    ax_nationwide.text(bar.get_x() + bar.get_width() / 2, yval, int(yval), ha='center', va='bottom', fontsize=6)

plt.tight_layout()
plt.show()