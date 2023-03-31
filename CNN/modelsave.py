import argparse
import os

import numpy as np
import torch

from src.dataset import MyDataset
from src.model import QuickDraw

#체크포인트 파일로 모델을 만드는 코드

def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of the Quick Draw model proposed by Google""")
    #parser.add_argument("--optimizer", type=str, choices=["sgd", "adam"], default="adam")
    parser.add_argument("--total_images_per_class", type=int, default=10000)
    parser.add_argument("--ratio", type=float, default=0.8, help="the ratio between training and test sets")
    #parser.add_argument("--num_epochs", type=int, default=20)
    parser.add_argument("--gradient_accumulation_steps", type=int, default=1, help="Number of updates steps to accumulate before performing a backward/update pass.")
    parser.add_argument("--es_min_delta", type=float, default=0.0,
                        help="Early stopping's parameter: minimum change loss to qualify as an improvement")
    parser.add_argument("--es_patience", type=int, default=3,
                        help="Early stopping's parameter: number of epochs with no improvement after which training will be stopped. Set to 0 to disable this technique.")
    parser.add_argument("--data_path", type=str, default="data", help="the root folder of dataset")
    parser.add_argument("--log_path", type=str, default="tensorboard")
    parser.add_argument("--saved_path", type=str, default="/your/path/trained_models")
    parser.add_argument('--local_rank', type=int, default=-1,
                    help='local rank passed from distributed launcher')
    #deepspeed /root/finalproject/QuickDraw-master/train.py --deepspeed_config /root/finalproject/deepspeedconfig.json으로 실행
    args = parser.parse_args()
    return args


def train(opt):
    training_set = MyDataset(opt.data_path, opt.total_images_per_class, opt.ratio, "train")
    model = QuickDraw(num_classes=training_set.num_classes)

    checkpoints = [f for f in os.listdir() if f.startswith('checkpoint')]
    if checkpoints:
        latest_checkpoint = max(checkpoints)
        checkpoint = torch.load(latest_checkpoint, map_location=torch.device('cpu'))
        start_epoch = checkpoint['epoch']
        start_iter = checkpoint['iteration']
        new_state_dict = {}
        for k, v in checkpoint['state_dict'].items():
            name = k[7:]  # remove module.
            new_state_dict[name] = v
        model.load_state_dict(new_state_dict)
        print("=> loaded checkpoint (epoch {}, iteration {})".format(start_epoch+1, start_iter))
    else:
        start_epoch = 0
        start_iter = 0
        print("=> no checkpoint found")
        
        
    torch.save(model, opt.saved_path + os.sep + "whole_model_MIT330")

    

if __name__ == "__main__":
    opt = get_args()
    train(opt)
