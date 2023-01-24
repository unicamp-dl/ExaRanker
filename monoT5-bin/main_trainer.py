#inicio / imports
import os
import torch
import numpy as np
from torch.utils.data import DataLoader
from transformers import TrainingArguments, AdamW
from sklearn.model_selection import train_test_split
from pathlib import Path
import pandas as pd
from datasets import Dataset
from datasets import load_dataset
import os.path
from os import path
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import NeptuneLogger
from pytorch_lightning.callbacks import LearningRateMonitor

neptune_logger = NeptuneLogger(
            api_key='key',
            project='project', 
            
        )

#os.environ["TOKENIZERS_PARALLELISM"] = "false"

os.system('clear')

# se 1: utiliza a amostra de demonstracao
# se 0: utiliza o dataset real
demo = 0
verbose = 1


#-----------------------------------------------------------------------------------------------------------------
#dataset
#-----------------------------------------------------------------------------------------------------------------
from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained("t5-base")
model = T5ForConditionalGeneration.from_pretrained("t5-base")

f_main = 'ds/dsMonoT5v5bin.tsv'


#carrega dos arquivos csv
if demo ==0:
    #set_train = load_dataset('csv', delimiter = ',', data_files=f_main, split='train[:20000]')
    #set_eval = load_dataset('csv', delimiter = ',', data_files=f_main, split='train[20000:]')
    
    set_train = load_dataset('csv', delimiter = '\t', data_files=f_main, split='train[:30000]')
    set_eval = load_dataset('csv', delimiter = '\t', data_files=f_main, split='train[:500]')
    
        
else:
    set_train = load_dataset('csv', delimiter = '\t', data_files=f_main, split='train[:32]')
    set_eval = load_dataset('csv', delimiter = '\t', data_files=f_main, split='train[100:132]')

#shape do dataset
print(tokenizer.pad_token_id)
print('Train:', set_train.shape)
print('Eval:', set_eval.shape)
print()

#criando os datasets
from utils import MyDataset

max_length = 512


batch_n = 4

#cria datasets
train_dataset = MyDataset(set_train,max_length, tokenizer)
eval_dataset = MyDataset(set_eval,max_length, tokenizer)

#testa um item do dataset - para visualização
if verbose == 1:
    print()
    idx = 2
    x1= train_dataset.__getitem__(idx)
    print()
    print('     input_ids shape: ', x1['input_ids'].shape)
    print('Attention_mask shape: ', x1['attention_mask'].shape)
    print('               Label:', tokenizer.decode(x1['label']))
    print('\nDecodifica uma amosta:\n', tokenizer.decode(x1['input_ids']))
    print()


#cria o data loader de test
train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=batch_n, num_workers = 0, shuffle=True)
eval_dataloader =  torch.utils.data.DataLoader(eval_dataset, batch_size=batch_n, num_workers = 0)

#modelo
from utils import MyModel

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

if verbose == 1:
    print()
    print('RODANDO COM CUDA: ', torch.cuda.is_available() )
    print()

num_gpus = 0
if torch.cuda.is_available():
    num_gpus = 1



model.to(device)
model.train()


#treinamento
num_epoch = 30 #19 ou 150

accum_batch = 32

num_batch = int(np.ceil(train_dataset.__len__() / batch_n))
model_pl = MyModel(model,device,tokenizer)

lr_monitor = LearningRateMonitor(logging_interval='epoch')

trainer = pl.Trainer(enable_checkpointing=False, log_every_n_steps=1, default_root_dir = 'monoT5-bin/chk',accumulate_grad_batches=accum_batch, gpus=num_gpus, max_epochs=num_epoch, logger=neptune_logger, callbacks=[lr_monitor])

trainer.fit(model_pl,train_dataloader,eval_dataloader)


neptune_logger.experiment.stop()
