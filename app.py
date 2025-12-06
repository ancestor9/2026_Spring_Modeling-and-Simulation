##############################
## 1. Naive Implementation
##############################
# import matplotlib.pyplot as plt
# from simulation import run_simulation

# def main():
#     # ==========================================
#     # [설정] 여기서 시뮬레이션 파라미터를 변경하세요
#     # ==========================================
#     P1 = 0.5           # Olin -> Wellesley 이동 확률
#     P2 = 0.5           # Wellesley -> Olin 이동 확률
#     NUM_STEPS = 60     # 시뮬레이션 시간 (분)
#     INITIAL_OLIN = 10  # Olin 초기 자전거 수
#     # ==========================================

#     print(f"시뮬레이션을 시작합니다... (p1={P1}, p2={P2}, steps={NUM_STEPS})")

#     # 1. 시뮬레이션 실행 (모듈 호출)
#     df = run_simulation(P1, P2, NUM_STEPS, INITIAL_OLIN)

#     # 2. 결과 텍스트 출력 (선택 사항)
#     print("\n--- 시뮬레이션 결과 (상위 5개 행) ---")
#     print(df.head())
#     print("\n--- 시뮬레이션 결과 (하위 5개 행) ---")
#     print(df.tail())

#     # 3. 결과 시각화 (그래프 창 띄우기)
#     plt.figure(figsize=(10, 6))
#     plt.plot(df['time'], df['olin'], label='Olin', color='blue')
#     plt.plot(df['time'], df['wellesley'], label='Wellesley', color='red')
    
#     plt.title(f'Bike Share Simulation (p1={P1}, p2={P2})')
#     plt.xlabel('Time step (minutes)')
#     plt.ylabel('Number of Bikes')
#     plt.ylim(0, 15)
#     plt.legend()
#     plt.grid(True)
    
#     print("\n그래프 창이 열렸습니다. 닫으면 프로그램이 종료됩니다.")
#     plt.show()

# if __name__ == "__main__":
#     main()
    
##############################
## 2. Improved Implementation_version1
##############################
# import matplotlib.pyplot as plt
# from simulation import run_simulation

# def main():
#     # 설정값
#     P1 = 0.5
#     P2 = 0.5
#     NUM_STEPS = 60
#     INITIAL_OLIN = 10

#     print(f"시뮬레이션을 시작합니다... (p1={P1}, p2={P2}, steps={NUM_STEPS})")

#     # [수정] run_simulation이 이제 (df, metrics) 두 가지를 반환하므로 언패킹합니다.
#     df, metrics = run_simulation(P1, P2, NUM_STEPS, INITIAL_OLIN)

#     # 결과 데이터 출력
#     print("\n--- 시뮬레이션 결과 데이터 (일부) ---")
#     print(df.head())

#     # [추가] 메트릭(성능 지표) 출력
#     print("\n--- 성능 지표 (불만족 고객 분석) ---")
#     print(f"Olin에서 자전거가 없어 대여 못한 횟수: {metrics['olin_empty']}")
#     print(f"Wellesley에서 자전거가 없어 대여 못한 횟수: {metrics['wellesley_empty']}")
#     print(f"총 불만족 건수: {metrics['total_unhappy']}")

#     # 그래프 시각화
#     plt.figure(figsize=(10, 6))
#     plt.plot(df['time'], df['olin'], label='Olin', color='blue')
#     plt.plot(df['time'], df['wellesley'], label='Wellesley', color='red')
    
#     plt.title(f'Bike Share Simulation (Unhappy Customers: {metrics["total_unhappy"]})') # 제목에 메트릭 추가
#     plt.xlabel('Time step (minutes)')
#     plt.ylabel('Number of Bikes')
#     plt.ylim(0, 15)
#     plt.legend()
#     plt.grid(True)
    
#     print("\n그래프 창이 열렸습니다.")
#     plt.show()

# if __name__ == "__main__":
#     main()
    
################################
## 3. Improved Implementation_version2  
################################
# 확률 변화(p1)에 따른 불만족 고객 수"**를 보여줍니다
import matplotlib.pyplot as plt
import numpy as np  # [NumPy 도입]
from simulation import run_simulation, sweep_p1

def main():
    # ==========================================
    # [설정] 시뮬레이션 및 스윕 파라미터
    # ==========================================
    P2 = 0.5           # Wellesley -> Olin 이동 확률 (고정)
    NUM_STEPS = 60     # 시뮬레이션 시간 (분)
    INITIAL_OLIN = 10  # Olin 초기 자전거 수
    
    # [NumPy linspace 사용]
    # 0부터 1까지 일정한 간격으로 21개의 값을 생성합니다 (0.0, 0.05, ... 1.0)
    # 기존 range()는 정수만 가능하므로 linspace가 필수적입니다.
    p1_array = np.linspace(0, 1, 21)
    # ==========================================

    print("--- 1. 단일 시뮬레이션 테스트 (p1=0.5) ---")
    # 점진적 개발 확인: 기본 기능이 여전히 잘 작동하는지 확인
    df, metrics = run_simulation(0.5, P2, NUM_STEPS, INITIAL_OLIN)
    print(f"단일 실행 결과 - 총 불만족 고객: {metrics['total_unhappy']}\n")

    print(f"--- 2. 매개변수 스윕 실행 (p1 범위: 0.0 ~ 1.0) ---")
    # [매개변수 스윕 함수 호출]
    sweep_series = sweep_p1(p1_array, P2, NUM_STEPS, INITIAL_OLIN)

    # 결과 데이터 출력 (SweepSeries)
    print("\n[SweepSeries 결과 데이터]")
    print(sweep_series.head())
    print("...")
    print(sweep_series.tail())

    # 3. 결과 시각화 (매개변수 vs 성능)
    plt.figure(figsize=(10, 6))
    
    # Pandas Series는 plot() 메서드를 직접 지원합니다.
    # X축: p1 값 (Index), Y축: 불만족 고객 수 (Values)
    plt.plot(sweep_series.index, sweep_series.values, marker='o', linestyle='-', color='purple')
    
    plt.title('Parameter Sweep: Effect of p1 on Unhappy Customers')
    plt.xlabel('Probability of Bike from Olin to Wellesley (p1)')
    plt.ylabel('Total Unhappy Customers')
    plt.grid(True)
    
    # 최적점 표시 (불만족이 가장 적은 곳)
    min_unhappy = sweep_series.min()
    best_p1 = sweep_series.idxmin()
    plt.annotate(f'Best p1 (~{best_p1:.2f})', xy=(best_p1, min_unhappy), 
                 xytext=(best_p1, min_unhappy + 5),
                 arrowprops=dict(facecolor='black', shrink=0.05))

    print(f"\n분석 결과: 불만족 고객이 가장 적은 p1 값은 약 {best_p1:.2f} (불만족 {min_unhappy}명) 입니다.")
    print("그래프 창이 열렸습니다.")
    plt.show()

if __name__ == "__main__":
    main()
    
'''
결과 그래프:

X축은 p1 (Olin에서 자전거를 빌릴 확률)입니다.
Y축은 Total Unhappy Customers (자전거가 없어 못 빌린 사람 수)입니다.

그래프는 대개 U자 형태(또는 특정 구간에서 최소값을 갖는 형태)를 띨 것입니다. 
p1이 너무 낮으면 Olin에 자전거가 쌓여 Wellesley 고객이 불만이고, p1이 너무 높으면 Olin 자전거가 금방 동나서 Olin 고객이 불만이기 때문입니다.

의의: 이 스윕 과정을 통해 시스템이 가장 효율적으로 동작하는(불만족이 최소화되는) 최적의 p1 값을 찾아낼 수 있습니다. 
이것이 시뮬레이션 모델링의 주된 목적 중 하나입니다.
'''