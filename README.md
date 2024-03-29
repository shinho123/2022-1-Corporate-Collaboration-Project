# 2022-1-Sanhak-Project
* 2022년도 1학기 산학프로젝트
* 기업 : (주)플레도(Edutech)
* 프로젝트 기간 : 2022년 05월 ~ 2022년 08월
* 수행 업무 : Data preprocessing, EDA(Data visualization analysis, Data group analysis, Data missing value analysis)
# 산학 프로젝트 플레도 AI 학습블록


## Ⅰ. 데이터 소개 
- **사용 데이터** : 플레도 AI 학습블록 사용 로그 데이터
  - 총 데이터 수 : 63,366개
  - 유저 수 : 105명
  - Feature 종류 : 아이 고유 식별값, 아이 생년월일, 아이 성별, 단계, 컨텐츠 분류1, 컨텐츠 분류2, 컨텐츠 분류3, 단계, 단계별 문제, 문제 세부 번호, 문제 고유 식별 값, 학습 시각, 문제풀이 소요시간, 문제 정답, 아이 블록 입력 데이터, 정오답, 통계 메인 키, 향상 능력
 
- **같은 유저가 같은 문제에 대한 로그가 중복으로 쌓일 경우 하나로 COUNT**
  - 컨텐츠 분류 중 요리, 음악, 미술의 경우는 정오답이 아닌 과정이 로그 데이터로 쌓임
  - 컨텐츠 분류 중 한글, 수학, 영어의 경우 여러 번 오답을 제출한 뒤 정답에 도달하는 경우
 
- **문제풀이 소요시간은 전체 데이터(로그)를 살리고 3가지 분류별로 나이, 성별에 따라 EDA를 진행함**
  - 컨텐츠, 향상능력, 문제풀이 소요시간 → 나이, 성별에 따라 EDA 진행
    
![image](https://github.com/shinho123/2022-1-Sanhak-Project/assets/105840783/5bee1196-8826-401c-be0c-393c394eef55)

## Ⅱ. EDA
- EDA는 나이, 성별, 이상치 순으로 나누어 분석함
  - **나이** : 나이별 컨텐츠 분류, 나이별 향상능력 분류, 나이별 문제풀이 소요시간
  - **성별** : 성별별 컨텐츠 분류, 성별별 향상능력
  - **이상치 확인 및 제거** : 각 컨텐츠 별로 이상치를 확인함(Q1-(1.5*IQR)미만, Q3+(1.5*IQR) 초과인 값을 제거함)
 
## Analysis

**나이·성별**

<img width="612" alt="image" src="https://github.com/shinho123/2022-1-Sanhak-Project/assets/105840783/56295fc1-4a26-4831-a9b2-3791a6084c04">

- 105명 → 96명(10세 보다 나이가 많은 유저는 제외시킴)
- 5~7세의 유아가 가장 많이 이용함
  - 유아의 경우 1살 차이도 발달 능력에서 큰 차이를 보임
- 남자 : 51명, 여자 : 45명으로 남녀의 비율 차이가 없음


**컨텐츠 분류**

**나이별 컨텐츠 분류**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/852b850b-7360-4530-a653-cd7399ab506d)

* 국어(한글) 컨텐츠를 많이 이용하는 것을 볼 수 있음
* 5세 이상에서는 수학과 영어 컨텐츠의 비율이 증가함을 볼 수 있음

**나이별 향상능력 분류**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/b92ccb31-1e27-4dd8-884c-d816bf5052ec)

* 나이별 향상능력 분류에서도 앞선 나이별 컨텐츠 분류와 같이 이해력 부분이 가장 많은 부분을 차지하고 있음

* 나이와 상관없이 비슷한 비율을 보임

**나이에 따른 문제풀이 소요시간**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/0e2a9d6b-6e39-4f6b-a49e-8283a7f99a73)

* 8세이상부터 전체적으로 문제풀이 소요시간이 단축되고 있음


**성별별 컨텐츠 분류**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/2175c2b6-8388-4d02-be21-2c83978f6474)

* 컨텐츠 활용 패턴에서 남성은 주로 한글, 수학, 영어 분야를 선호하는 반면, 여성은 미술, 음악, 요리에 큰 관심을 보이고 있음

**성별별 향상능력 분류**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/6a9afcb5-8196-49cb-9215-a4dc2c6e97a8)

* 향상된 역량 측면에서는 남성이 이해력에서 높은 사용량을 나타내며, 여성은 상상력, 표현력, 집중력, 창의력 등의 분야에서 더 뛰어난 역량을 보이고 있음

**성별별 문제풀이 소요시간**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/468b25d3-bbc6-4d95-aeb8-1255e9c5c769)

* 성별 간 문제풀이 소요시간의 큰 차이는 없지만 한글을 제외한 모든 컨텐츠에서 남자아이의 평균 문제풀이 소요시간이 짧게 나타

**컨텐츠에 따른 문제풀이 소요시간**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/bd53c33e-0de8-4002-8036-56bc1c0cf0e4)

* 영어를 풀 때 소요시간이 가장 오래 걸림
* 음악을 풀 때 소요시간이 가장 적게 걸림
  * 단, 여기서의 문제 풀이 평균 소요시간을 계산할 때엔 모든 나이의 User를 포함하여 계산(11세 이상도 모두 포함)


**이상치 처리(1)**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/de70b81f-3974-444a-a808-138233bb1f7f)

* 각 컨텐츠 별로 Q1-1.5*IQR 미만, Q3+1.5*IQR 초과인 값을 제거함

**이상치 처리(2)**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/4816b1ab-ee96-4951-b6dd-75d3823cdcff)

* "문제풀이 소요시간" 분석을 위한 이상치(Outlier)처리를 실시

* 가장 자주 사용되는 IQR 기반의 이상치 탐지 및 처리 방법을 선택

* 히스토그램을 통해 이상치 구간을 추정 및 계산

* 데이터에서 이상치 구간 제거 진행 → Lower bound < Data < Upper bound

**문제풀이 소요시간(ANOVA 분석)**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/8d4dd7aa-ca76-4520-9a84-2e8485dbf8c1)

* 나이대가 높아질수록 평균문제풀이 시간이 점차 낮아지는 것을 확인할 수 있으며, 나이대에 따라 평균 문제풀이 소요시간이 다르므로 나이대에 알맞는 문제 추천이 필요함

**컨텐츠 선택(독립성 검정)**

![image](https://github.com/shinho123/2022-1-Corporate-Collaboration-Project/assets/105840783/0154f355-68a0-4093-bfd9-1223b1c36925)

* 컨텐츠 중 한글과 수학분야는 성별이나 나이에 상관없이 높은 것을 알 수 있으며, 나이대와 성별에 따라 컨텐츠 선택 수 차이가 있으므로 각 영역에 따라 선호하는 컨텐츠가 있을 것으로 예측됨

## Ⅲ. 결론

* User : 96명
* EDA : 나이, 성별, 컨텐츠, 향상 능력

* 5~7세 유아의 이용률이 가장 높으며, 국어(한글), 수학, 영어의 사용 비중이 가장 높음

* 결국 아이 학습의 경우 5~7세 사이에 국어, 영어, 수학에 비중을 많이 두고 교육하는 것을 알 수 있음

* 국, 영, 수에서 많은 학습이 이루어지면서 자연스럽게 이해력 부분에서 가장 많은 비중의 향상능력을 보였음


* **나이**

  * 5세 이상부터 교육의 변화가 가장 크게 나타나고 있음

  * 8세 이상부터 문제풀이 소요시간이 감소되는 것을 볼 수 있음

* **성별**
  
  * 남자 : 국어(한글), 수학, 영어의 이용률이 높게 나타나며, 이해력에서 높은 향상 능력을 보임

  * 여자 : 미술, 음악, 요리에 이용률이 높게 나타나고 있으며, 상상력, 표현력, 집중력, 창의력에서 높은 향상 능력을 보임

* **컨텐츠**

  * 영어를 풀 때 시간이 가장 많이 소요됨

  * 음악을 풀 때 시간이 가장 많이 소요됨

* **통계 분석**

  * 문제풀이 소요시간(ANOVA 분석)
  
  * 나이대가 높아질수록 평균문제풀이 시간이 점차 낮아지는 것을 확인할 수 있음
  
  * 나이대에 따라 평균 문제풀이 소요시간이 다르므로 나이대에 알맞는 문제 추천이 필요함

* **컨텐츠 선택(독립성 검정)**

  * 컨텐츠 중 한글과 수학분야는 성별이나 나이에 상관없이 높은 것을 알 수 있음

  * 나이대와 성별에 따라 컨텐츠 선택 수 차이가 있으므로 각 영역에 따라 선호하는 컨텐츠가 있을 것으로 사료됨


## Ⅳ. 신규 서비스 시나리오 제안
- 인터페이스 제공
  - User의 나이, 성별에 따른 평균 컨텐츠 진도 수준, 향상능력 수준 등을 그래프로 시각화
  - 각 문제에 따른 평균 문제풀이 소요시간 제공
    - 사용 데이터 : 전체 유저의 문제풀이 소요시간, 컨텐츠 선택 수, 향상능력 수
- 고객 이탈률 방지 서비스
  - 일정기간 접속하지 않은 고객에게 알람 서비스
    - 사용 데이터 : User의 학습 시각, 로그데이터
- 오답노트 서비스
  - 자주 틀린 문제를 다시 점검하여 반복학습이 가능하도록 하는 서비스
    - 사용 데이터 : User의 정오답, User 블록 입력 데이터
