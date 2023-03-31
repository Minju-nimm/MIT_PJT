import torch
import torch.nn as nn
from math import pow

class QuickDraw(nn.Module):
    def __init__(self, input_size = 28, num_classes = 100):
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
    
    
print(QuickDraw.state_dict)
#     # DeepSpeed를 사용하는 경우
# if opt.deepspeed_config is not None:
#     model = QuickDraw()
#     model, _, _ = deepspeed.initialize(model=model, config_params=opt.deepspeed_config)
#     optimizer = deepspeed.ops.adam.DeepSpeedCPUAdamW(model.parameters())

# # DeepSpeed를 사용하지 않는 경우
# else:
#     model = QuickDraw()
#     if opt.optimizer == "adam":
#         optimizer = torch.optim.Adam(model.parameters(), lr=opt.lr)
#     elif opt.optimizer == "sgd":
#         optimizer = torch.optim.SGD(model.parameters(), lr=opt.lr, momentum=0.9)
#     else:
#         print("invalid optimizer")
#         exit(0)

# # 모델 학습 코드
# for epoch in range(opt.epochs):
#     for i, (inputs, targets) in enumerate(training_generator):
#         inputs, targets = inputs.to(device), targets.to(device)
#         optimizer.zero_grad()
#         outputs = model(inputs)
#         loss = criterion(outputs, targets)
#         loss.backward()
#         optimizer.step()

#         # 학습 결과 출력
#         if (i + 1) % opt.print_freq == 0:
#             print(f"Epoch: {epoch + 1}/{opt.epochs}, Iteration: {i + 1}/{len(training_generator)}, Lr: {opt.lr:.2e}, Loss: {loss.item():.6f}, Accuracy: {accuracy:.2f}")