# main.py : 모델 학습 및 models 폴더에 저장

## 라이브러리 추가하기
import argparse

from train import *


if __name__ == "__main__":
    ## Parser 생성하기
    parser = argparse.ArgumentParser(description="KoGPT2",
                                    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    dir_path = 'C:/Users/USER/final-project-level3-nlp-06-main/KoGPT2/datasets'
    model_name = 'skt/kogpt2-base-v2'
    output_dir = 'models'
    overwrite_output_dir = False
    per_device_train_batch_size = 1
    num_train_epochs = 10
    save_steps = 500

    parser.add_argument("--model_name", default='skt/kogpt2-base-v2', type=str, dest="model_name")
    parser.add_argument("--num_train_epochs", default=10, type=int, dest="num_train_epochs")

    parser.add_argument("--per_device_train_batch_size", default=16, type=int, dest="per_device_train_batch_size")
    parser.add_argument("--dir_path", default='C:/Users/USER/final-project-level3-nlp-06-main/KoGPT2/datasets', type=str, dest="dir_path")
    parser.add_argument("--output_dir", default="models", type=str, dest="output_dir")
    parser.add_argument("--overwrite", default=False, type=bool, dest="overwrite_output_dir")

    parser.add_argument("--save_steps", default=500, type=int, dest="save_steps")

    args = parser.parse_args()
    train(args)
