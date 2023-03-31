import argparse
import os
import shutil
import json

import numpy as np
import torch
import torch.nn as nn
from tensorboardX import SummaryWriter
from torch.utils.data import DataLoader

from src.dataset import MyDataset
from src.model import QuickDraw
from src.utils import get_evaluation

import deepspeed 
import torch.optim as optim
import torch.optim.lr_scheduler as lr_scheduler
#from deepspeed.ops.adam import DeepSpeedCPUAdam, DeepSpeedCPUAdamW, DeepSpeedFusedAdam
# from transformers import AdamW
# from torch.optim import Adam
from deepspeed.ops.adam import FusedAdam



def get_args():
    parser = argparse.ArgumentParser(
        """Implementation of the Quick Draw model proposed by Google""")
    #parser.add_argument("--optimizer", type=str, choices=["sgd", "adam"], default="adam")
    parser.add_argument("--total_images_per_class", type=int, default=7000)
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
    parser = deepspeed.add_config_arguments(parser)
    args = parser.parse_args()
    return args

def save_checkpoint(state, filename='checkpoint.pth.tar'):
    torch.save(state, filename)
    
deepspeed.init_distributed()

def train(opt):
    if torch.cuda.is_available():
        torch.cuda.manual_seed(123)
        device = torch.device("cuda")
    else:
        torch.manual_seed(123)
        
    if opt.deepspeed_config is not None:
        with open(opt.deepspeed_config) as f:
            deepspeed_config = json.load(f)
        train_batch_size = deepspeed_config["train_batch_size"]
        max_epochs = deepspeed_config["max_epochs"]
        # train_micro_batch_size_per_gpu = deepspeed_config["train_micro_batch_size_per_gpu"]
        # gradient_accumulation_steps = deepspeed_config["gradient_accumulation_steps"]
        
        training_params = {"batch_size": train_batch_size,
                        "shuffle": True,
                        "num_workers": 0,
                        "pin_memory": True}

        test_params = {"batch_size": train_batch_size,
                    "shuffle": False,
                    "num_workers": 0,
                    "pin_memory": True}

    output_file = open(opt.saved_path + os.sep + "logs.txt", "w")
    output_file.write("Model's parameters: {}".format(vars(opt)))

    training_set = MyDataset(opt.data_path, opt.total_images_per_class, opt.ratio, "train")
    training_generator = DataLoader(training_set, **training_params)
    print ("there are {} images for training phase".format(training_set.__len__()))
    test_set = MyDataset(opt.data_path, opt.total_images_per_class, opt.ratio, "test")
    test_generator = DataLoader(test_set, **test_params)
    print("there are {} images for test phase".format(test_set.__len__()))


    model = QuickDraw(num_classes=training_set.num_classes)
    optimizer = FusedAdam(model.parameters(), lr=1e-3)
    scheduler = lr_scheduler.CosineAnnealingLR(optimizer, T_max=100)
    model, optimizer, _, _ = deepspeed.initialize(model=model, config_params=opt.deepspeed_config, optimizer=optimizer)
    #모델 gpu로 옮기기
    model.to(device)
    #optimizer = Adam(model.parameters(), lr=1e-3)
    model.cuda()
    
    if os.path.isdir(opt.log_path):
        shutil.rmtree(opt.log_path)
    os.makedirs(opt.log_path)
    writer = SummaryWriter(opt.log_path)
    #writer.add_graph(model, torch.rand(opt.batch_size, 1, 28, 28))

    if torch.cuda.is_available():
        model_parameters = filter(lambda p: p.requires_grad, model.parameters())
        model_parameters = list(map(lambda x: x.cuda(), model_parameters))

    criterion = nn.CrossEntropyLoss()
    #손실 함수 정의
    
# 모델 학습 수행 전 초기화 작업 수행! (나중에 모델로 저장해두려고 변수에 저장해두는거임)
    epoch = 0
    best_loss = 1e5 #현재까지 관찰된 최적의 손실값
    best_epoch = 0 #현재까지 관찰된 최적의 epoch값
    save_freq = 5
    model.train() #모델을 학습 모드로 설정
    num_iter_per_epoch = len(training_generator) #학습 데이터로부터 생성된 배치의 총갯수
    
    checkpoints = [f for f in os.listdir() if f.startswith('checkpoint')]
    if checkpoints:
        latest_checkpoint = max(checkpoints)
        checkpoint = torch.load(latest_checkpoint)
        start_epoch = checkpoint['epoch']
        start_iter = checkpoint['iteration']
        model.load_state_dict(checkpoint['state_dict'])
        optimizer.load_state_dict(checkpoint['optimizer'])
        print("=> loaded checkpoint (epoch {}, iteration {})".format(start_epoch+1, start_iter))
    else:
        start_epoch = 0
        start_iter = 0
        print("=> no checkpoint found")

    #모델 train
    for epoch in range(start_epoch, max_epochs):
        for iter, batch in enumerate(training_generator, start=start_iter):
            images, labels = batch
            #데이터 gpu로 옮기기
            images = images.to(device)
            labels = labels.to(device)
            optimizer.zero_grad()
            predictions = model(images)
            loss = criterion(predictions, labels)
            #loss /= opt.gradient_accumulation_steps
            loss.backward()
            optimizer.step()
            scheduler.step()
            predictions = predictions.to(device) # predictions Tensor를 GPU 메모리로 이동
            
            #get_evaluation: label과 예측값을 입력받아 정확도를 계산하는 함수
            training_metrics = get_evaluation(labels.cpu().numpy(), predictions.cpu().detach().numpy(),list_metrics=["accuracy"]) 
            print(model.device)
            print("Epoch: {}, Iteration: {}/{}, Lr: {}, Loss: {}, Accuracy: {}".format(
                    epoch + 1,
                    iter + 1,
                    num_iter_per_epoch,
                    optimizer.param_groups[0]['lr'],
                    loss, training_metrics["accuracy"]))
            writer.add_scalar("Train/Loss", loss.item(), epoch * num_iter_per_epoch + iter)
            writer.add_scalar('Train/Accuracy', training_metrics["accuracy"], epoch * num_iter_per_epoch + iter)
            #모델을 학습하는 과정에서 매 epoch마다 손실과 정확도를 계산하고 Tensorboard에 기록
            
            #모델 가중치 저장해놓기
            if (iter) % save_freq == 0: 
            # 진행중인 iteration이랑 정해둔 저장빈도가 나누어떨어질 때 ex)10번째, 20번째...
                state = {
                    'epoch': epoch,
                    'iteration': iter,
                    'state_dict': model.state_dict(),
                    'optimizer': optimizer.state_dict(),
                }
                save_checkpoint(state, filename=f'checkpoint_epoch{epoch}_iter{iter}.pth.tar')
                if os.path.exists(f'checkpoint_epoch{epoch}_iter{iter-10}.pth.tar'):
                    os.remove(f'checkpoint_epoch{epoch}_iter{iter-10}.pth.tar')


    
    model.eval() #모델을 평가 모드로 설정
    loss_ls = []
    te_targets_ls = []
    te_pred_ls = []

    #테스트 데이터를 배치 단위로 가져와서 테스트 수행
    for idx, te_batch in enumerate(test_generator):
        te_images, te_labels = te_batch
        num_samples = te_labels.size()[0]
        if torch.cuda.is_available():
            #데이터 gpu로 옮기기
            te_images = te_images.to(device)
            te_labels = te_labels.to(device)
        te_predictions = model(te_images)
        te_loss = criterion(te_predictions, te_labels) #손실 계산
        loss_ls.append(te_loss * num_samples)
        te_targets_ls.extend(te_labels.clone().cpu())
        te_pred_ls.append(te_predictions.clone().cpu())
        te_loss = sum(loss_ls) / test_set.__len__()
        te_pred = torch.cat(te_pred_ls, 0)
        te_label = np.array(te_targets_ls)
        test_metrics = get_evaluation(te_label, te_pred.numpy(), list_metrics=["accuracy", "confusion_matrix"]) #모델의 성능 평가 지표 계산
        output_file.write(
            "Epoch: {} \nTest loss: {} Test accuracy: {} \nTest confusion matrix: \n{}\n\n".format(
                epoch + 1,
                te_loss,
                test_metrics["accuracy"],
                test_metrics["confusion_matrix"]))
        print("Epoch: {}, Lr: {}, Loss: {}, Accuracy: {}".format(
            epoch + 1,
            optimizer.param_groups[0]['lr'],
            te_loss, test_metrics["accuracy"]))
        writer.add_scalar('Test/Loss', te_loss, epoch)
        writer.add_scalar('Test/Accuracy', test_metrics["accuracy"], epoch)
        model.train()
        if te_loss + opt.es_min_delta < best_loss:
            best_loss = te_loss
            best_epoch = epoch
            #제일 최적인 모델 저장
            torch.save(model, opt.saved_path + os.sep + "whole_model_MIT")
            #더 안 나아질 때 학습 중단
        if epoch - best_epoch > opt.es_patience > 0:
            print("에포크 {}에서 train 종료. 가장 낮은 loss:{}".format(epoch, te_loss))
            break
    writer.close()
    output_file.close()


if __name__ == "__main__":
    opt = get_args()
    train(opt)