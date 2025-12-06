##############################
## 1. Naive Implementation
##############################
# import pandas as pd
# from model import BikeShareSystem

# def run_simulation(p1, p2, num_steps, initial_olin=10):
#     """
#     시뮬레이션을 실행하고 결과를 반환하는 함수
    
#     :param p1: Olin -> Wellesley 이동 확률
#     :param p2: Wellesley -> Olin 이동 확률
#     :param num_steps: 시뮬레이션 진행 시간 (분)
#     :param initial_olin: Olin 초기 자전거 수
#     :return: 시뮬레이션 결과 DataFrame
#     """
#     # Wellesley 초기값은 전체 12대라고 가정할 때 나머지
#     total_bikes = 12
#     initial_wellesley = total_bikes - initial_olin
    
#     # 시스템 객체 생성
#     system = BikeShareSystem(olin_bikes=initial_olin, wellesley_bikes=initial_wellesley)
    
#     # 정해진 스텝만큼 반복
#     for _ in range(num_steps):
#         system.step(p1, p2)
        
#     # 결과를 Pandas DataFrame으로 변환하여 반환
#     df = pd.DataFrame(system.results)
#     return df

##############################
## 2. Improved Implementation_version1
##############################
# import pandas as pd
# from model import BikeShareSystem

# def run_simulation(p1, p2, num_steps, initial_olin=10):
#     """
#     주어진 파라미터로 시뮬레이션을 실행하고 결과와 메트릭을 반환합니다.
    
#     매개변수:
#         p1, p2: 이동 확률
#         num_steps: 시뮬레이션 스텝 수
#         initial_olin: 초기 자전거 수
        
#     반환값:
#         df (DataFrame): 시간대별 자전거 수 변화
#         metrics (dict): 시뮬레이션 요약 지표 (불만족 고객 수 등)
#     """
#     total_bikes = 12
#     initial_wellesley = total_bikes - initial_olin
    
#     # [유연성] State 객체 생성
#     system = BikeShareSystem(olin_bikes=initial_olin, wellesley_bikes=initial_wellesley)
    
#     # 시뮬레이션 루프
#     for _ in range(num_steps):
#         system.step(p1, p2)
        
#     # 결과 데이터프레임 생성
#     df = pd.DataFrame(system.results)
    
#     # [추가] 메트릭 수집 (불만족 고객 수 확인)
#     metrics = {
#         "olin_empty": system.olin_empty,
#         "wellesley_empty": system.wellesley_empty,
#         "total_unhappy": system.olin_empty + system.wellesley_empty
#     }
    
#     return df, metrics  # 데이터프레임과 메트릭을 함께 반환

###############################
## 3. Improved Implementation_version2
###############################
import pandas as pd
import numpy as np
from model import BikeShareSystem

def run_simulation(p1, p2, num_steps, initial_olin=10):
    """
    단일 시뮬레이션을 실행하고 최종 상태(메트릭)를 반환합니다.
    (기존 기능 유지)
    """
    total_bikes = 12
    initial_wellesley = total_bikes - initial_olin
    
    system = BikeShareSystem(olin_bikes=initial_olin, wellesley_bikes=initial_wellesley)
    
    for _ in range(num_steps):
        system.step(p1, p2)
        
    df = pd.DataFrame(system.results)
    
    # [값을 반환하는 함수] 최종 상태를 요약한 객체(딕셔너리)를 반환
    metrics = {
        "olin_empty": system.olin_empty,
        "wellesley_empty": system.wellesley_empty,
        "total_unhappy": system.olin_empty + system.wellesley_empty
    }
    
    return df, metrics

def sweep_p1(p1_array, p2, num_steps, initial_olin=10):
    """
    [매개변수 스윕]
    p1(Olin->Wellesley 확률)의 범위를 입력받아 시뮬레이션을 반복하고,
    각 p1 값에 따른 '총 불만족 고객 수'를 SweepSeries로 반환합니다.
    
    매개변수:
        p1_array (array): np.linspace로 생성된 p1 값들의 배열
        p2 (float): 고정된 p2 확률
        num_steps (int): 시뮬레이션 시간
        
    반환값:
        sweep_series (pd.Series): 인덱스는 p1 값, 값은 total_unhappy 수
    """
    # [SweepSeries 객체 도입] 
    # 여기서는 Pandas Series를 사용하여 매개변수(p1)와 결과(metric)를 매핑합니다.
    sweep_results = []
    
    print(f"매개변수 스윕 시작: {len(p1_array)}개의 p1 값에 대해 실험합니다.")
    
    for p1 in p1_array:
        # [점진적 개발] 기존에 잘 작동하는 run_simulation 함수를 활용합니다.
        _, metrics = run_simulation(p1, p2, num_steps, initial_olin)
        
        # 결과값 수집 (여기서는 '총 불만족 고객 수'를 분석 대상으로 함)
        sweep_results.append(metrics['total_unhappy'])
        
    # 결과를 Pandas Series(SweepSeries 역할)로 변환하여 반환
    sweep_series = pd.Series(sweep_results, index=p1_array)
    return sweep_series