# :baby: 어린이를 위한 동화 제작 서비스, My AI Fairy-Tale :green_book:
<br>
</br>

<p align="center"><img src ="https://user-images.githubusercontent.com/119478998/228507228-d11276a3-f62d-4806-96d7-99826c7f3037.png"></p>

<div align="center">
안녕하세요! 어린이를 위한 동화 제작 서비스 My AI Fairy-Tale입니다. <br> 
그림을 그리면 MIT가 동화를 만들어 줄거에요. MIT와 같이 재밌게 동화를 만들어 보아요!
</div>

<br>
</br>

## :family: 팀원 소개
|     :camera: |  Member	|             R & R   	|
|:-----:	|:-----:|:-------------------------------------------------------:	|
|     <img src="https://user-images.githubusercontent.com/119478998/228486556-2aa892ef-467a-45e7-9d8d-8c1608061d08.png" width = 120> |  김민주 <br> [@Minju-nimm](https://github.com/Minju-nimm) 	|             데이터 구축 및 전처리 <br> 딥러닝 모델 구현 및 성능 평가(koGPT)  <br> Github, Notion 관리   	|
|   <img src="https://user-images.githubusercontent.com/119478998/228479938-280d9099-5753-4c9b-a922-4e7ba2c3fec3.png" width = 100> 	|   김기준 <br> [@AppleKimkijun](https://github.com/AppleKimkijun) 	|  딥러닝 모델 구현 및 성능 평가 <br> 웹 서비스 구현(React, Flask)	|
|   <img src="https://user-images.githubusercontent.com/119478998/228500320-feb1cd01-d33c-4c40-8543-5469b32deed1.png" width = 90> 	| 허정윤  <br>  [@heojeongyun](https://github.com/heojeongyun)	|          데이터 구축 및 전처리 <br> 딥러닝 모델 구현 및 성능 평가(CNN)	|
|   <img src="https://user-images.githubusercontent.com/119478998/228480501-9c912752-9479-47d1-82ae-abe55c5440b2.png" width = 90>  	|  	권준혁	<br> [@BraveJunyeok](https://github.com/BraveJunyeok)| 딥러닝 모델 구현 및 성능 평가 <br> 웹 서비스 구현(React, Flask)     	|
|   <img src="https://user-images.githubusercontent.com/119478998/228480867-4eda595e-05e4-42ce-8e58-99b13c964ce7.png" width = 110>  	|  최이삭 <br> [@isaac0930](https://github.com/isaac0930)	| 데이터 구축 및 전처리 <br> 딥러닝 모델 구현 및 성능 평가(koGPT)  	|
| <img src="https://user-images.githubusercontent.com/119478998/228481599-f84242a7-aa9d-4413-b966-a173c850aecd.png" width = 90> 	| 박성현 <br> [@KKDDDS](https://github.com/KKDDDS)       | 데이터 구축 및 전처리  <br> 웹 서비스 구현(React, Flask)  	|




## :information_desk_person: 서비스 소개
오늘날 어린이들은 스마트폰과 태블릿을 통해 단순히 영상을 시청하는 등 수동적으로 미디어를 소비합니다. 심지어 3-4세의 경우 WHO의 권장 소비시간을 훨씬 넘어 평균 4시간 8분 이상 미디어를 소비합니다. 어린이들이 수동적으로 소비하게 되는 미디어가 아니라, 적극적으로 참여할 수 있는 서비스의 필요성을 느껴 서비스를 개발하게 되었습니다. 

My AI Fairytale은 어린이가 그린 그림을 바탕으로 동화 이미지와 동화를 생성하여 직접 읽어주는 기능까지 탑재한 참여형 창작 웹서비스 입니다. 어린이의 마음을 사로잡는 새로운 동화와 그림을 생성함으로써 어린이의 정서적 발달에도 크게 기여할 것으로 기대합니다.


### My AI Fairy-Tale 바로가기 - 링크 첨부

## 시연영상 넣기



## Installation
```bash
pip install -r requirements.txt
```

## Architecture

:baby:
:child:
:book:


## Project Tree :deciduous_tree:
```bash
MIT_PJT
├── CNN
│   ├── RESULT
│   ├── README.md
│   ├── kogpt_inference.py
│   ├── kogpt_trainer.py
│   └── util.py
├── KoGPT2
│   ├── RESULT
│   ├── datasets
│   ├── README.md
│   ├── inference.py
│   ├── main.py
│   ├── train.py
│   └── util.py
├── koGPT2_split
│   ├── data
│   ├── dataset.py
│   ├── inference.py
│   ├── main.py
│   ├── model.py
│   └── train.py
├── react
│   ├── App.css
│   ├── App.js
│   ├── index.css
│   ├── index.js
│   ├── layer.py
│   ├── components
│   ├── images
│   ├── pages
│   └── redux
├── flask
│   ├── perplexity_compute_metrics.py
│   ├── perplexity_test.py
│   ├── preprocessing.py
│   └── scrapper.py
├── requirements.txt
└── README.md
```

## Usage
문서형식으로 간단히 ㅅ정리하면 될듯

koGPT2 
python KoGPT/kogpt_trainer.py







## Dataset



## Reference



---
해당 프로젝트는 멀티캠퍼스 데이터 분석 및 웹 개발자 13회차 파이널 프로젝트 3조 MIT가 기획하였습니다.
