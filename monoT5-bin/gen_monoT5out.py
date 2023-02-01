import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import json
from utils import MyUtils

class MyGenOut():
    def __init__(self):
        self.inicio = 1
        
    def run(self, model_n_in):
        os.system('clear')

        #control flags
        demo = 0
        #run verbos2
        verbose = 0
        #run gpt api openai
        run_monoT5 = 1      

        model_n = model_n_in

        tokenizer = T5Tokenizer.from_pretrained("monoT5-bin/chk/model-" + str(model_n))
        model = T5ForConditionalGeneration.from_pretrained("monoT5-bin/chk/model-" + str(model_n))

        
        if demo ==1 :
            file_run = 'baseline/run.dl20demo.txt'
        else:
            file_run = 'baseline/run.dl20.txt'

        id = 0

        func = MyUtils()


        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        
        print()
        print('RODANDO COM CUDA: ', torch.cuda.is_available() )
        print()


        model.to(device)

        with open(file_run, encoding='utf8') as f:
            for line in f:
                if id >= 0:

                    stringl = line.split()
                    query_id = stringl[0]
                    doc_id = stringl[2]
                    prompt_txt = func.gen_prompt(func.get_query(query_id),func.get_doc(doc_id) )
                        
                    if verbose ==1:
                        print('### ' + str(id))
                        print('Query ID: ' + query_id)
                        print(func.get_query(query_id))
                        print('Query DOC: ' + doc_id)
                        print(func.get_doc(doc_id))
                        print()
                        print(prompt_txt)
                    
                    if run_monoT5 ==1:
                        item1 = tokenizer(prompt_txt, truncation=True, max_length=512, padding='max_length', return_tensors="pt")
                        input_ids, attention_mask = item1.input_ids.to(device), item1.attention_mask.to(device)
                        
                        outputs = model.generate(input_ids=input_ids, attention_mask=attention_mask,
                                max_length=2,
                                output_scores=True,
                                return_dict=True,
                                return_dict_in_generate=True)
                        #text_seq = ""
                        text_seq = tokenizer.decode(outputs.sequences[0][1:])
                        
                        tokens_seq = tokenizer.convert_ids_to_tokens(outputs.sequences[0][1:])
                        tokens_seq = [s.replace('\u2581', '') for s in tokens_seq]
                        
                        # Greedy decoding:
                        mask = outputs.sequences != tokenizer.pad_token_id
                        probs = torch.stack(outputs.scores, dim=1).log_softmax(dim=-1)
                        prob_values, prob_indices = probs.max(dim=2)
                        score_seq = prob_values[0][:mask[0].sum()].tolist()
                        
                        

                        
                        dict = { "text": text_seq, "tokens": tokens_seq, "scores": score_seq}
                        
                        
                        jsonf = json.dumps(dict)
                        
                        
                        fj = open("monoT5-bin/chk/model-" + str(model_n) + "/out2/output" + str(id) + ".json","w")
                        
                        
                        fj.write(jsonf)
                        fj.close()
                        
                    
                        print(str(id))

                id = id +1


        f.close()

