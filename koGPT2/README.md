# KoGPT2

## KoGPT2?
    - GPT-2의 부족한 한국어 성능 향상을 위해, 40GB 이상의 한국어 corpus로 학습된 모델
    - [https://github.com/SKT-AI/KoGPT2](https://github.com/SKT-AI/KoGPT2)
    - 본 프로젝트에서는 `skt/kogpt2-base-v2` 모델 사용

## Tokenizer
    - 허깅페이스 [tokenizers](https://github.com/huggingface/tokenizers) 패키지의 Character BPE tokenizer 사용
    - vocab size는 51,200이고, 일부 자주 사용되는 이모지와 이모티콘도 포함되어 있다고 합니다.
    
    ```python
    > from transformers import PreTrainedTokenizerFast
    > tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
      bos_token='</s>', eos_token='</s>', unk_token='<unk>',
      pad_token='<pad>', mask_token='<mask>')
    > tokenizer.tokenize("안녕하세요. 한국어 GPT-2 입니다.😤:)l^o")
    ['▁안녕', '하', '세', '요.', '▁한국어', '▁G', 'P', 'T', '-2', '▁입', '니다.', '😤', ':)', 'l^o']
    ```

## Data
  - KoGPT2의 경우 `한국어 위키 백과`, 뉴스, `모두의 말뭉치 v1.0`, `청와대 국민청원` 등의 다양한 데이터를 사용
  - 본 프로젝트에서는 여러 `동화 데이터`를 이용해 학습을 시켜 동화 생성에 최적화된 모델을 만드는 것을 목표로 합니다.
    - 어린이 청와대 - 전래동화 100선
    - 그림형제 동화 모음집
    - 이솝우화 모음집
    - tale.txt
  - Preprocessing
    - "(계속)"이라는 문자열 다음에 "●" 또는 "○"이라는 문자가 나타나면 그 사이의 문자열을 제거
    - 여러 개의 공백을 하나의 공백으로 대체
    - 괄호로 둘러싸인 문자열 삭제
    - 주소 링크 삭제
    - 번역가의 개인 견해 삭제
  
## Train
  - 동화 데이터 분리 학습 모델 (자세한 사항은 koGPT2_Split을 참고하세요.)
  - 동화 데이터 전체 학습 모델 ( 최종 모델 선정 )

## Usage

```python
# 모델 학습 명령어
python koGPT2/main.py

# 동화 생성 실행 명령어, 학습한 모델 필요
python koGPT2/inference.py
```
