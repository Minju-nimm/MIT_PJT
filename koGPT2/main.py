# main.py

from transformers import AutoModelWithLMHead, PreTrainedTokenizerFast
import text_preprocessing
from koGPT2_trainer import train_kogpt2_model
from fastai.text.all import *
import fastai

# Read raw text data
lines = text_preprocessing.read_txt_files('./Data/Raw')
cleaned_lines = text_preprocessing.clean_text(lines)

# Initialize tokenizer and model
tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
                                                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                    pad_token='<pad>', mask_token='<mask>') 
model = AutoModelWithLMHead.from_pretrained("skt/kogpt2-base-v2")

# Train the model
trained_model = train_kogpt2_model(cleaned_lines, tokenizer, model)
