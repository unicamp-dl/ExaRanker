
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
import json
from utils import MyUtils
from gen_monoT5out import MyGenOut

func = MyGenOut()

#func.run('model name')
func.run(500)
