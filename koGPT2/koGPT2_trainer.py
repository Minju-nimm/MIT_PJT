# kogpt2_trainer.py

import torch
import torch.nn as nn
from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
import fastai
from typing import List

from fastai.text.all import *

import re
import text_preprocessing

def train_kogpt2_model(lines: List[str], tokenizer: PreTrainedTokenizerFast, model: GPT2LMHeadModel):
    """
    trains a GPT2LMHeadModel on the given lines and returns the trained model
    :param lines: List of strings, representing training data
    :param tokenizer: PreTrainedTokenizerFast, tokenizer used to encode the training data
    :param model: GPT2LMHeadModel, pre-trained model used as the basis for transfer learning
    :return: trained GPT2LMHeadModel
    """
    
    tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>') 
    model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2")

    # Define TransformersTokenizer
    class TransformersTokenizer(Transform):
        def __init__(self, tokenizer): 
            self.tokenizer = tokenizer
        def encodes(self, x): 
            toks = self.tokenizer.tokenize(x)
            return tensor(self.tokenizer.convert_tokens_to_ids(toks))
        def decodes(self, x): 
            return TitledStr(self.tokenizer.decode(x.cpu().numpy()))

    # Split data
    train = lines[:int(len(lines)*0.8)]
    test = lines[int(len(lines)*0.8):]
    splits = [[0],[1]]

    # Initialize dataloader
    tls = TfmdLists([train,test], TransformersTokenizer(tokenizer), splits=splits, dl_type=LMDataLoader)
    batch,seq_len = 2,256 # OOM problem 8,256
    dls = tls.dataloaders(bs=batch, seq_len=seq_len)

    # Define Callback class
    class DropOutput(Callback):
        def after_pred(self): 
            self.learn.pred = self.pred[0]

    # Initialize learner
    learn = Learner(dls, model, loss_func=CrossEntropyLossFlat(), 
                    cbs=[DropOutput], metrics=Perplexity()).to_fp16()

    # Find learning rate
    lr=learn.lr_find()
    print(lr)

    # Train the model
    learn.fit_one_cycle(5, lr)
    
    # Save the trained model
    learn.export('./models/koGPT2_model_0322_2.pkl') # model name

    return learn.model
