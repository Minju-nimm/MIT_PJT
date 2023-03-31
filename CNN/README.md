# MIT_QuickDrawCNN
어린이를 위한 AI 기반 동화 생성 웹 서비스 ‘My AI Fairy-Tale’에서 사용자의 그림을 인식하기 위해 사용되는 CNN 모델 학습 코드입니다.

[https://github.com/uvipen/QuickDraw](https://github.com/uvipen/QuickDraw) 의 CNN 학습 코드에 딥스피드 라이브러리를 적용하고 더 많은 데이터를 학습에 사용했습니다.

- CNN
    - 합성곱 신경망. 이미지나 영상 분류에 주로 사용되는 모델
    - 입력 이미지의 특징맵을 추출하여 분류에 사용
        
        → DNN보다 훨씬 적은 파라미터를 사용하고, 입력 데이터의 변형에 강하다
        
- [Deepspeed](https://github.com/microsoft/DeepSpeed)
    - 파이토치의 연산과 개발 속도를 더욱 가속화하는 최적화 라이브러리
    - 적은 코드 변경으로 GPU 로컬 메모리를 효과적으로 활용할 수 있음
    - 단일 GPU보다는 다중 GPU를 사용할 때 추천… ****🥲****
    - 해당 모델은 단순하기 때문에 사용하지 않아도 무방합니다.
- Data
    - [https://github.com/googlecreativelab/quickdraw-dataset](https://github.com/googlecreativelab/quickdraw-dataset)
    - Google Creative Lab에서 제공하는 Quick, Draw! 데이터셋
    - 총 345개 클래스의 5천만개 그림 데이터
    
- Usage
    - `src/model.py` 의 num_classes, `src/config.py`의 CLASSES 부분을 수정하여 사용할 클래스 갯수 조정 가능
    - `src/dataset.py` 와 `[train.py](http://train.py)` 에서 `total_image_per_class` 파라미터를 조정하여 클래스 당 학습에 사용할 데이터 갯수 조절 가능
    - `deepspeedconfig.json` 에서 배치 사이즈나 max_epoch 등 다양한 파라미터 조절 가능

```
python traincopy.py #딥스피드를 사용하지 않고 모델을 학습합니다. traincopy.py 파일은 참고한 깃허브의 학습 코드 원본입니다.
deepspeed train.py --deepspeed_config deepspeedconfig.json #딥스피드를 사용하여 모델을 학습합니다.
python modelsave.py #학습 중간에 생성된 checkpoint 파일을 불러와 모델로 저장합니다.
```