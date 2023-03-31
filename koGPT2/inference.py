import torch
import torch.nn as nn
import transformers
import fastai

from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from fastai.text.all import *

import re

from pathlib import Path

# download model and tokenizer
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>') 
model = GPT2LMHeadModel.from_pretrained("skt/kogpt2-base-v2")

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

    def forward(self, x):
        if not self.training or self.p == 0.:
            return x
        mask = x.new_empty((x.size(0), 1, 1, 1), requires_grad=False).bernoulli_(1 - self.p)
        return mask * x / (1 - self.p)


# inference
def main():
    learn = load_learner(Path('C:/Users/USER/koGPT2_Sum_Ver/models/koGPT2_model_0322.pkl'))
    learn.model.cuda() # 모델을 GPU로 이동
    
    prompt = "옛날 옛적에 나무" # 동화 첫 부분. CNN keyword 포함.
    prompt_ids = tokenizer.encode(prompt)
    inp = tensor(prompt_ids)[None].cuda()

    preds = learn.model.generate(inp,
                                 max_length=128,
                                 pad_token_id=tokenizer.pad_token_id,
                                 eos_token_id=tokenizer.eos_token_id,
                                 bos_token_id=tokenizer.bos_token_id,
                                 repetition_penalty=2.0,
                                 use_cache=True,
                                 do_sample=True)
    
    generated_text = tokenizer.decode(preds[0].cpu().numpy())
    generated_text = generated_text.replace(". ", ".\n")
    return generated_text

    
if __name__ == "__main__":
    main()
    