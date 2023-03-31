import torch
import torch.nn as nn
from math import pow

class QuickDraw(nn.Module):
    def __init__(self, input_size = 28, num_classes = 200):
        super(QuickDraw, self).__init__()
        self.num_classes = num_classes
        #첫번째 컨볼루션 레이어
        self.conv1 = nn.Sequential(nn.Conv2d(1, 32, 5, bias=False), 
                                   #1채널의 흑백 이미지를 32개의 5x5 필터로 변환
                                   nn.BatchNorm2d(32), 
                                   #배치 정규화- 모델의 학습 속도와 성능을 향상시키기 위해 적용
                                   nn.ReLU(inplace=True),
                                   #렐루 활성화함수 적용!
                                   nn.MaxPool2d(2,2))
                                   #2x2 맥스풀링으로 특징 맵 크기를 절반으로 줄임
        #두번째 컨볼루션 레이어
        self.conv2 = nn.Sequential(nn.Conv2d(32, 64, 5, bias=False),
                                   # 32개의 입력 채널을 64개의 5x5 필터로 변환하여 출력
                                   nn.BatchNorm2d(64),
                                   # 배치정규화
                                   nn.ReLU(inplace=True), 
                                   # 렐루 활성화함수 적용
                                   nn.MaxPool2d(2, 2))
                                   # 2x2 맥스풀링으로 특징 맵 크기를 절반으로 줄임
                                   
        dimension = int(64 * pow(input_size/4 - 3, 2))
        # Fully Connected 레이어의 입력 차원 계산
        
        # 첫 번째 Fully Connected 레이어
        self.fc1 = nn.Sequential(nn.Linear(dimension, 512), 
                                 # 전결합층으로 출력 뉴런 512개를 가짐
                                 nn.BatchNorm1d(512),
                                 # 배치 정규화 적용
                                 nn.Dropout(0.5))
                                 # 드롭아웃 정규화를 통해 과적합 방지
        # 두 번째 Fully Connected 레이어
        self.fc2 = nn.Sequential(nn.Linear(512, 128), 
                                 # 전결합층으로 출력 뉴런 128개를 가짐
                                 nn.BatchNorm1d(128),
                                 # 배치정규화
                                 nn.Dropout(0.5))
                                 # 드롭아웃으로 과적합방지
        # 출력 레이어
        self.fc3 = nn.Sequential(nn.Linear(128, num_classes))
        # 분류하고자 하는 클래스 수에 맞게 출력 뉴런의 개수를 설정

    def forward(self, input):
        output = self.conv1(input)
        output = self.conv2(output)
        output = output.view(output.size(0), -1)
        output = self.fc1(output)
        output = self.fc2(output)
        output = self.fc3(output)
        return output
