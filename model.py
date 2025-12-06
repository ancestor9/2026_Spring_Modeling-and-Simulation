########################################
## 1. Naive Implementation
########################################
# import random

# class BikeShareSystem:
#     def __init__(self, olin_bikes=10, wellesley_bikes=2):
#         """
#         초기 상태 설정
#         :param olin_bikes: Olin에 있는 자전거 수
#         :param wellesley_bikes: Wellesley에 있는 자전거 수
#         """
#         self.olin = olin_bikes
#         self.wellesley = wellesley_bikes
#         self.clock = 0
        
#         # 기록용 데이터
#         self.results = {'time': [], 'olin': [], 'wellesley': []}
#         self.record_state()

#     def record_state(self):
#         """현재 상태를 기록"""
#         self.results['time'].append(self.clock)
#         self.results['olin'].append(self.olin)
#         self.results['wellesley'].append(self.wellesley)

#     def bike_to_wellesley(self):
#         """Olin에서 Wellesley로 자전거 이동"""
#         if self.olin > 0:
#             self.olin -= 1
#             self.wellesley += 1

#     def bike_to_olin(self):
#         """Wellesley에서 Olin으로 자전거 이동"""
#         if self.wellesley > 0:
#             self.wellesley -= 1
#             self.olin += 1

#     def step(self, p1, p2):
#         """
#         단위 시간(1분) 동안의 변화 시뮬레이션
#         :param p1: Olin -> Wellesley 이동 확률
#         :param p2: Wellesley -> Olin 이동 확률
#         """
#         self.clock += 1
        
#         # Olin에서 Wellesley로 이동할지 결정
#         if random.random() < p1:
#             self.bike_to_wellesley()
            
#         # Wellesley에서 Olin으로 이동할지 결정
#         if random.random() < p2:
#             self.bike_to_olin()
            
#         self.record_state()
        
################################
## 2. Improved Implementation_version1
################################
import random

class BikeShareSystem:
    """
    자전거 공유 시스템의 상태와 규칙을 정의하는 클래스입니다.
    Olin College와 Wellesley College 간의 자전거 이동을 시뮬레이션합니다.
    """

    def __init__(self, olin_bikes=10, wellesley_bikes=2):
        """
        시스템의 초기 상태를 설정합니다.
        
        매개변수:
            olin_bikes (int): Olin에 있는 초기 자전거 수
            wellesley_bikes (int): Wellesley에 있는 초기 자전거 수
        """
        # [변경] State 객체 속성 정의 (자전거 수)
        self.olin = olin_bikes
        self.wellesley = wellesley_bikes
        self.clock = 0
        
        # [추가] 메트릭 도입: 불만족 고객 수 (자전거가 없어 대여 실패한 횟수)
        self.olin_empty = 0
        self.wellesley_empty = 0
        
        # 기록용 데이터 저장소
        self.results = {'time': [], 'olin': [], 'wellesley': []}
        self.record_state()

    def record_state(self):
        """현재 시점의 자전거 분포 상태를 기록합니다."""
        self.results['time'].append(self.clock)
        self.results['olin'].append(self.olin)
        self.results['wellesley'].append(self.wellesley)

    def bike_to_wellesley(self):
        """
        Olin에서 Wellesley로 자전거를 이동시킵니다.
        
        [추가 요구사항 반영]
        - 음수 자전거 문제 처리: 자전거가 0이면 이동하지 않고 함수를 종료(return)합니다.
        - 메트릭 도입: 자전거가 없으면 '불만족 고객(olin_empty)' 수를 증가시킵니다.
        """
        if self.olin == 0:
            self.olin_empty += 1  # [메트릭] 자전거 부족으로 인한 불만족 카운트
            return                # [음수 방지] 함수 즉시 종료 (State 보호)
            
        self.olin -= 1
        self.wellesley += 1

    def bike_to_olin(self):
        """
        Wellesley에서 Olin으로 자전거를 이동시킵니다.
        
        [추가 요구사항 반영]
        - 음수 자전거 문제 처리 및 불만족 고객 메트릭 계산
        """
        if self.wellesley == 0:
            self.wellesley_empty += 1  # [메트릭] 불만족 카운트
            return                     # [음수 방지]
            
        self.wellesley -= 1
        self.olin += 1

    def step(self, p1, p2):
        """
        단위 시간(1분) 동안의 시뮬레이션 단계를 수행합니다.
        
        매개변수:
            p1 (float): Olin -> Wellesley 이동 확률
            p2 (float): Wellesley -> Olin 이동 확률
        """
        self.clock += 1
        
        # [반복적 모델링] 확률에 따라 이동 함수 호출
        if random.random() < p1:
            self.bike_to_wellesley()
            
        if random.random() < p2:
            self.bike_to_olin()
            
        self.record_state()
        
################################
## 3. Improved Implementation_version2
################################
# 위와 동일