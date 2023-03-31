from flask import Flask, request , send_file, jsonify, session
from flask_cors import CORS
import json
import openai
import requests
import io
import random

import cv2
import numpy as np
from src.config import *
from src.dataset import CLASSES
import torch
import base64
# from PIL import Image // 이미지 저장 
import urllib.request

import os
import sys

from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
from fastai.text.all import *


app = Flask(__name__)
CORS(app)
app.secret_key = ""

class_dict = {'apple': '사과', 'book': '책', 'bowtie': '보타이', 'candle': '촛대', 'cloud': '구름', 'cup': '컵',
'door': '문', 'envelope': '봉투', 'eyeglasses': '안경', 'guitar': '기타', 'hammer': '망치', 'hat': '모자',
'ice cream': '아이스크림', 'leaf': '나뭇잎', 'scissors': '가위', 'star': '별', 't-shirt': '티셔츠',
'pants': '바지', 'lightning': '번개', 'tree': '나무'}

keyword_key = [] # 달리와 스토리에 들어갈 전역변수
story_key = [] # 스토리 담는 전역변수
story_key_en = [] # 스토리를 영어로 만들어서 달리에 넣어주는 전역변수 

def get_session_id():
    if 'user_id' in session:
        return session['user_id']
    else:
        session['user_id'] = request.remote_addr
        return session['user_id']

# download model and tokenizer
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>') 
model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")

class TransformersTokenizer(Transform):
    def __init__(self, tokenizer): self.tokenizer = tokenizer
    def encodes(self, x): 
        toks = self.tokenizer.tokenize(x)
        return tensor(self.tokenizer.convert_tokens_to_ids(toks))
    def decodes(self, x): return TitledStr(self.tokenizer.decode(x.cpu().numpy()))

class DropOutput(nn.Module):
    def __init__(self, p=0.):
        super().__init__()
        self.p = p


@app.route('/post_data', methods=['POST',"GET"])
def post_data():
    if 'user_id' not in session:
        user_id = get_session_id()
        # HTTP POST 요청 데이터를 추출합니다.
        data = request.get_json()
        image_data = data.get('image', '')
        # base64 문자열로부터 이미지 데이터를 복원합니다.
        image_64 = base64.b64decode(image_data.split(',')[1])
        image_array = np.frombuffer(image_64, np.uint8)
        # with open('./image/canvas_image.png', 'wb') as f:
        #     f.write(image_64)

        image = cv2.imdecode(image_array, cv2.IMREAD_UNCHANGED)
        _, _, _, alpha = cv2.split(image)
        image_gray = alpha

        # 여기서 부터 모델 코드 ------------------------------------------------------
        # 이미지를 28*28 크기로 조정합니다.
        img_resized = cv2.resize(image_gray, (28, 28))
        
        # 이미지를 numpy 배열로 변환합니다.
        img_array = np.array(img_resized, dtype=np.float32)

        # 이미지를 4차원 입력으로 만듭니다.
        img_tensor = np.expand_dims(img_array, axis=0)
        img_tensor = np.expand_dims(img_tensor, axis=0)

        # 이미지를 pytorch tensor로 변환합니다.
        img_tensor = torch.from_numpy(img_tensor)

        model = torch.load("/root/draw_flask/src/whole_model_quickdraw.txt", map_location=torch.device('cpu'))
        model.eval()

        with torch.no_grad():
            logits = model(img_tensor)
            pred = torch.argmax(logits, dim=1).item()
            pred_class = CLASSES[pred]
            pred_class_kr = class_dict.get(pred_class, '알 수 없는 객체')  # 클래스 이름을 한글로 변환합니다.
            keyword_key.clear()
            keyword_key.append(pred_class_kr)

        # 예측 결과를 로그에 기록합니다.
        app.logger.info(f'user_id: {user_id}, pred_class: {pred_class}, pred_class_kr: {pred_class_kr}')

        # 예측 결과를 클라이언트에게 반환합니다.
        return {"prediction": pred_class_kr}  


learn = load_learner('/root/draw_flask/src/koGPT2_model_0322.pkl')
learn.model.cuda() # 모델을 GPU로 이동

@app.route('/get_story', methods=['GET','POST'])
def get_story():
    if 'user_id' not in session:
        user_id = get_session_id()
        
        prompt1 = "옛날 옛적에 " + keyword_key[0]
        prompt_ids1 = tokenizer.encode(prompt1)
        inp1 = tensor(prompt_ids1)[None].cuda()
        
        prompt2 = ""
        max_iterations = 100

        for i in range(max_iterations):
            preds = learn.model.generate(inp1,
                                        max_length=20,
                                        pad_token_id=tokenizer.pad_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        bos_token_id=tokenizer.bos_token_id,
                                        repetition_penalty=2.0,
                                        use_cache=True,
                                        do_sample=True)

            generated_text = tokenizer.decode(preds[0].cpu().numpy())

        # 문장의 마지막 문자가 마침표, 느낌표, 물음표 중 하나이면, 이를 두 번째 프롬프트(prompt2)로 정의
            if generated_text[-1] in [".", "!", "?"]:
                prompt2 = generated_text
                break
            else:
                continue

        prompt_ids2 = tokenizer.encode(prompt2)
        inp2 = tensor(prompt_ids2)[None].cuda()

        prompt3 = ""

        for i in range(max_iterations):
            preds = learn.model.generate(inp2,
                                        max_length=40,
                                        pad_token_id=tokenizer.pad_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        bos_token_id=tokenizer.bos_token_id,
                                        repetition_penalty=2.0,
                                        use_cache=True,
                                        do_sample=True)

            generated_text2 = tokenizer.decode(preds[0].cpu().numpy())

        # 문장의 마지막 문자가 마침표, 느낌표, 물음표 중 하나이면, 이를 두 번째 프롬프트(prompt3)로 정의
            if generated_text2[-1] in [".", "!", "?"]:
                prompt3 = generated_text2 
                break
            else:
                continue

        prompt_ids3 = tokenizer.encode(prompt3)
        inp3 = tensor(prompt_ids3)[None].cuda()

# 최종적으로 텍스트를 생성
        for i in range(max_iterations):
            preds = learn.model.generate(inp3,
                                        max_length=70,
                                        pad_token_id=tokenizer.pad_token_id,
                                        eos_token_id=tokenizer.eos_token_id,
                                        bos_token_id=tokenizer.bos_token_id,
                                        repetition_penalty=2.0,
                                        use_cache=True,
                                        do_sample=True)

            generated_text3 = tokenizer.decode(preds[0].cpu().numpy())

        # 문장의 마지막 문자가 다., 요., 죠 중 하나일 때 종료
        # if generated_text3[-1] in [".", "!", "?"]:
            if generated_text3[-1] in ["다.", "요.", "죠."]:
                generated_text3 = generated_text3
            else:
                continue

        generated_text3 = generated_text3.replace(".", ". \n").replace("!", "! \n").replace("?","? \n").replace("다.","다. \n").replace("요.","요. \n").replace("죠.","죠. \n")

        # .replace("! ", "!\n").replace("? ", "?\n")
        #gpt에서 나온 스토리를 n번째 문장까지만 스토리 보이스에 넣을 코드
        sentences = generated_text3.split(". \n")
        story_key.clear()
        for i in range(10):
            if i < len(sentences):
                sentence = sentences[i].strip() + "."
                story_key.append(sentence)

        if story_key:  # 스토리 키 리스트가 비어있지 않은 경우에만 출력
            print(f"스토리 키 : {story_key}")
        else:
            print("세 번째 마침표 이전의 문장을 찾을 수 없습니다.")

        

        # 달리에 넣을 스토리 데이터 번역 파파고 api
        client_id = ""
        client_secret = ""
        encText = urllib.parse.quote(story_key[0])# 스토리에 담겨져있는 첫번째 문장을 번역 해서 달리에 넣음 첫번째만 넣어도 이미지와 스토리가 비슷하니까
        data = "source=ko&target=en&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if(rescode==200):
            response_body = response.read()
            print(response_body.decode('utf-8'))
        else:
            print("Error Code:" + rescode)
        data = response_body

        # 받아온 데이터 중에 translatedText 부분만 받아오는 코드
        parsed_data = json.loads(data)
        translated_text = parsed_data['message']['result']['translatedText'].replace('\n', ' ')
        print(f"translatedText 부분:{translated_text}")

        story_key_en.clear()
        story_key_en.append(translated_text) #달리에 넣을 스토리 번역 
        
        app.logger.info(f'user_id: {user_id}, story_key: {story_key}, story_key_en: {story_key_en}')
        # 리턴은 한글로 해서 보내주기
        return story_key[:-1]




@app.route('/get_data', methods=['GET','POST'])
def get_data():
    if 'user_id' not in session:
        user_id = get_session_id() # 사용자 IP 주소를 세션 id로 활용합니다.

        # dall-e api 가져오는 코드
        openai.api_key = ""
        openai.Model.list()
        response = openai.Image.create(
            prompt=f"Draw an incredibly cute and adorable illustration featuring characters with big, cheerful faces and small, adorable bodies that resemble babies. with{story_key_en[0]}",
            # story_key[0],keyword_key[0]
            n=1,
            size = "512x512"
        )
        if response and response.data and response.data[0].url:
            url = response.data[0].url
            image_data = requests.get(url).content

            # 이미지 데이터를 BytesIO 객체로 변환합니다.
            image_io = io.BytesIO(image_data)
            
            # 이미지를 저장할 파일 경로와 파일 이름을 지정합니다.
            save_path = './image/new_image.png'
            
            # 이미지를 파일로 저장합니다.
            with open(save_path, 'wb') as f:
                f.write(image_data)
                
        app.logger.info(f'user_id: {user_id}, send_file: {send_file}')
        return send_file(image_io, mimetype='image/png', as_attachment=True, download_name='new_image.png')


@app.route('/get_voice', methods=['GET','POST'])
def get_voice():
    if 'user_id' not in session:
        user_id = get_session_id()# 사용자 IP 주소를 세션 id로 활용합니다.
        client_id = ""
        client_secret = ""
        story_text = ''.join(story_key[:-1])# 스토리키에 있는 모든 문자열 데이터를 하나로 합치기
        encText = urllib.parse.quote(story_text,encoding="UTF-8") #story_kr
        data = f"speaker=ngoeun&volume=0&speed=0&pitch=0&format=mp3&text=" + encText
        url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode('utf-8'))
        rescode = response.getcode()
        if(rescode==200):
            print("TTS mp3 저장")
            response_body = response.read()
            with open('./image/1111.mp3', 'wb') as f:
                f.write(response_body)
        else:
            print("Error Code:" + rescode)

        app.logger.info(f'user_id: {user_id}, send_file: {send_file}')
        return send_file("./image/1111.mp3", mimetype='audio/mpeg') 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3500, debug=True)