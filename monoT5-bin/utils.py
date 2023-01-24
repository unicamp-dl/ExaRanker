import torch
import numpy as np
import wikipedia
import re
from urllib.parse import unquote
import pytorch_lightning as pl
from pytorch_lightning import Trainer
from pytorch_lightning.loggers import NeptuneLogger
import torch
import numpy as np
import csv
from pyserini.search.lucene import LuceneSearcher
import json
import os



class MyDataset(torch.utils.data.Dataset):
    def __init__(self, mydata, seq_length, tokenizer):
        self.labels = np.array(mydata['label'])
        self.seq1 = np.array(mydata['input'])
        self.seq2 = np.array(mydata['output'])
        self.seq_length = seq_length
        self.tokenizer = tokenizer
        
    def __getitem__(self, idx):
        seq1 = self.seq1[idx]
        label = self.labels[idx]
        
        seq2 = "false"        
        if label ==1:
            seq2="true"
        

        item1= self.tokenizer(seq1, truncation=True, max_length= self.seq_length, padding='max_length')
        item2= self.tokenizer(seq2, truncation=True, max_length= 2, padding='max_length')
        
        input_ids, attention_mask = torch.tensor(item1.input_ids), torch.tensor(item1.attention_mask)
        labels = torch.tensor(item2.input_ids)     

        item={'input_ids': input_ids}
        item['attention_mask']=attention_mask
        item['label'] = labels
        
        return item

    def __len__(self):
        return len(self.labels)

class MyModel(pl.LightningModule):

    def __init__(self,model,device,tokenizer):
        super(MyModel, self).__init__()
        self.model = model
        self.mydevice = device
        self.tokenizer = tokenizer
        self.mystep = 0
        
    def training_step(self, batch, batch_nb):
        input_ids = batch['input_ids'].to(self.mydevice)
        attention_mask = batch['attention_mask'].to(self.mydevice)
        labels = batch['label'].to(self.mydevice)
        outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
        
        #loss
        loss = outputs[0]

        # Calling self.log will surface up scalars for you in TensorBoard
        self.log('train_loss', loss, prog_bar=True)
        
        return loss
    
    def training_epoch_end(self, training_step_outputs):
        self.save_model()

    def on_train_batch_end(self,trainer,*args, **kwargs):
        self.mystep = self.mystep + 1
        
        if self.mystep % 500 == 0 and self.mystep >0 :
            
            directory = 'monoT5-bin/chk/model-' + str(self.mystep)
            if not os.path.exists(directory):
                os.makedirs(directory)
                os.makedirs(directory+'/out2')
            
            
            print('saving model --------' + str(self.mystep))
            model_to_save = self.model.module if hasattr(self.model, 'module') else self.model
            torch.save(model_to_save.state_dict(), 'monoT5-bin/chk/model-' + str(self.mystep) + '/pytorch_model.bin')
            model_to_save.config.to_json_file('monoT5-bin/chk/model-' + str(self.mystep) + '/config.json')
            self.tokenizer.save_pretrained('monoT5-bin/chk/model-' + str(self.mystep) + '/')    
    
    def validation_step(self, batch, batch_idx):
        self.model.eval()
        input_ids = batch['input_ids'].to(self.mydevice)
        attention_mask = batch['attention_mask'].to(self.mydevice)
        labels = batch['label'].to(self.mydevice)
        outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
        
        #loss
        loss = outputs[0]

        
        # Calling self.log will surface up scalars for you in TensorBoard
        self.log('val_loss', loss, prog_bar=True)
        
        self.model.train()
        
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=3e-5, weight_decay=0.01)
        lr_scheduler = {
            'scheduler': torch.optim.lr_scheduler.StepLR(optimizer, step_size=70, gamma=0.25),
            'name': 'log_lr'
            }
        return [optimizer], [lr_scheduler]
    
    def save_model(self):
        directory = 'monoT5-bin/chk/model'
        if not os.path.exists(directory):
            os.makedirs(directory)
            os.makedirs(directory+'/out2')
                
        model_to_save = self.model.module if hasattr(self.model, 'module') else self.model
        torch.save(model_to_save.state_dict(), 'monoT5-bin/chk/model/pytorch_model.bin')
        model_to_save.config.to_json_file('monoT5-bin/chk/model/config.json')
        self.tokenizer.save_pretrained('monoT5-bin/chk/model/')

class MyUtils():
    def __init__(self):
        self.searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
        
    def get_query(self, id):
        file_topic = 'baseline/topics.dl20.tsv'

        tsv_file = open(file_topic)
        read_tsv = csv.reader(tsv_file, delimiter="\t")
        for row in read_tsv:
            query_id = row[0]
            query_text = row[1]
            if query_id == id:
                tsv_file.close()
                return query_text
        tsv_file.close()
        return 'query not found'
    
    def get_doc(self, id):
        doc = self.searcher.doc(id)
        return json.loads(doc.raw())['contents']

    def gen_prompt(self, query, doc):
        prompt_txt = 'Is the question: \"' + query + "\" answered by the document: \"" + doc + "\"?"
        
        return ''.join(prompt_txt)