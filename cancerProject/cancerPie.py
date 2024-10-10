import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rc('font', family='NanumBarunGothic') #한글 폰트 
plt.rcParams['axes.unicode_minus'] = False  # 한글 변환 시 - 표기가 깨짐 방지

data = pd.read_csv('cancerDB.csv', encoding='utf-8')

# "암종"에 "모든암"제외 코드
fl_data = data[data['암종'] != '모든암']

# "발생연도"와 "성별"을 기준으로 그룹화
grd_data = fl_data.groupby(['발생연도', '성별'])

year_gender_data = {}

# 데이터를 연도와 성별로 나누어 저장
for (year, gender), group in grd_data:
    # 발생자수 기준으로 내림차순 정렬하고 상위 7개 선택
    top7 = group.sort_values(by='발생자수', ascending=False).head(7)
    # 연도를 확인하고 해당연도에 값이 아무것도 들어가있지 않다면 새로 다시생성 
    if year not in year_gender_data:
        year_gender_data[year] = {}
    year_gender_data[year][gender] = top7

# 사용자 정의 autopct 함수 (암종과 퍼센트 수치 모두 표시)
def autopct_format(pct, allvalues):
    absolute = int(pct / 100. * sum(allvalues))
    return f'{absolute}명\n({pct:.1f}%)'

# 연도별로 그래프 그리기
for year, gender_data in year_gender_data.items():
    fig, axes = plt.subplots(1, 2, figsize=(14, 7))  # 1행 2열의 서브플롯 설정

    # 남성 데이터 파이 차트 그리기
    if '남자' in gender_data:
        top7_male = gender_data['남자']
        labels_male = top7_male['암종']
        sizes_male = top7_male['발생자수']

        wedges_male, texts_male, autotexts_male = axes[0].pie(sizes_male, labels=labels_male, 
                                                               autopct=lambda pct: autopct_format(pct, sizes_male), startangle=140)
        axes[0].axis('equal')  # 남성 파이차트의 x축과 y축을 유지
        axes[0].set_title(f"{year}년 남성 상위 7개 암종별 발생자수 비율")
        axes[0].legend(wedges_male, labels_male, title="암종", loc="upper right", bbox_to_anchor=(1.3, 1))

    # 여성 데이터 파이 차트 그리기
    if '여자' in gender_data:
        top7_female = gender_data['여자']
        labels_female = top7_female['암종']
        sizes_female = top7_female['발생자수']

        wedges_female, texts_female, autotexts_female = axes[1].pie(sizes_female, labels=labels_female, 
                                                                     autopct=lambda pct: autopct_format(pct, sizes_female), startangle=140) #람다함수 사용 
        axes[1].axis('equal')  # 여성 파이차트의 x축과 y축을 유지
        axes[1].set_title(f"{year}년 여성 상위 7개 암종별 발생자수 비율")
        axes[1].legend(wedges_female, labels_female, title="암종", loc="upper right", bbox_to_anchor=(1.3, 1))

    # 그래프 보여주기
    plt.suptitle(f"{year}년 남성 vs 여성 암종 비교")
    plt.tight_layout()
    plt.show()