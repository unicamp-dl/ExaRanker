import csv
import json


class MyUtils():
    #def __init__(self):
    #    self.searcher = LuceneSearcher.from_prebuilt_index('msmarco-v1-passage')
        
    def gen_prompt(self, label, query, doc):
        with open('rerankgpt3-1k/gen_ds10k/prompt_model.txt') as f:
            prompt_txt = f.readlines()
        f.close()
        prompt_txt.append('\n\nQuestion: ' + query)
        prompt_txt.append('\n\nPassage: ' + doc)
        if label =='0':
            prompt_txt.append('\n\nFinal Answer: The passage is not relevant to the question')
            prompt_txt.append('\n\nExplanation:')
        else:
            prompt_txt.append('\n\nFinal Answer: The passage is relevant to the question')
            prompt_txt.append('\n\nExplanation:')
               

        return ''.join(prompt_txt)