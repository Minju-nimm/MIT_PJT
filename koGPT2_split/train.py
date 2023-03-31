from transformers import (
    GPT2LMHeadModel,
    Trainer,
    TrainingArguments,
    PreTrainedTokenizerFast
)
from util import load_dataset, load_data_collator, compute_metrics, TextDataset
from ml_things import plot_dict
import math
import torch

# Train
def train(args):
    dir_path = args.dir_path
    model_name = args.model_name
    output_dir = args.output_dir
    overwrite_output_dir = args.overwrite_output_dir
    per_device_train_batch_size = args.per_device_train_batch_size
    num_train_epochs = args.num_train_epochs
    save_steps = args.save_steps

    print(f'Model is {model_name}')

    # https://github.com/SKT-AI/KoGPT2
    tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name,
                    bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                    pad_token='<pad>', mask_token='<mask>')

    print('load dataset...')
    train_data, eval_data = load_dataset(dir_path, test_size=0.1)
    print(f'train_data : {len(train_data)}, eval_data : {len(eval_data)}')

    train_datasets = TextDataset(tokenizer=tokenizer,file_list=train_data, train=True)
    eval_datasets = TextDataset(tokenizer=tokenizer,file_list=eval_data, train=False)

    data_collator = load_data_collator(tokenizer)
    print(f'{dir_path} loaded!')
    print(f'train_dataset : {len(train_datasets)}, eval_dataset : {len(eval_datasets)}')
    
    tokenizer.save_pretrained(output_dir, legacy_format=False)
    print(f'Tokenizer save_pretrained. {output_dir}')
    
    model = GPT2LMHeadModel.from_pretrained(model_name)
    model.save_pretrained(output_dir)
    print(f'Model save_pretrained. {output_dir}')

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=overwrite_output_dir,
        per_device_train_batch_size=per_device_train_batch_size, # 4 -> 2 해도 cuda out of memory 뜸
        per_device_eval_batch_size=1,
        num_train_epochs=num_train_epochs,
        save_total_limit=2,
        evaluation_strategy='steps', # steps epoch
        eval_steps=500,
        fp16 = True,
        eval_accumulation_steps=1 
    )
    print(training_args)

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=train_datasets,
        eval_dataset=eval_datasets,
        compute_metrics=compute_metrics
    )
        
    trainer.train()
    print("Training Done!!")

    trainer.save_model()
    print(f'model saved.')


    # Keep track of train and evaluate loss.
    loss_history = {'train_loss':[], 'eval_loss':[]}

    # Keep track of train and evaluate perplexity.
    # This is a metric useful to track for language models.
    perplexity_history = {'train_perplexity':[], 'eval_perplexity':[]}

    print(trainer.state.log_history)
    # Loop through each log history.
    for log_history in trainer.state.log_history:
        if 'loss' in log_history.keys():
            # Deal with trianing loss.
            loss_history['train_loss'].append(log_history['loss'])
            perplexity_history['train_perplexity'].append(math.exp(log_history['loss']))
            
        elif 'eval_loss' in log_history.keys():
            # Deal with eval loss.
            loss_history['eval_loss'].append(log_history['eval_loss'])
            perplexity_history['eval_perplexity'].append(math.exp(log_history['eval_loss']))

    # Plot Losses.
    plot_dict(loss_history, start_step=training_args.logging_steps, 
            step_size=training_args.logging_steps, use_title='Loss', 
            use_xlabel='Train Steps', use_ylabel='Values', path='plot_loss.png', magnify=0.2)

    print()

    # Plot Perplexities.
    plot_dict(perplexity_history, start_step=training_args.logging_steps, 
            step_size=training_args.logging_steps, use_title='Perplexity', 
            use_xlabel='Train Steps', use_ylabel='Values', path='plot_ppl.png', magnify=0.2)
