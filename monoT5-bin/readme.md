# T5-base finetune and inference

Instructions:

1) To fine tune the model
run the code main_trainer.py
the check point will be saved in the path /chk

2) To generate the outputs from the model fine tunned
run the code run.py specifying the model name save in the /chk path
the outputs will be saved in a json filed in the /chk/model_name/out2

3) To calculate the model score and rerank the passage from TREC-DL 2020
run the code gen_monot5.py specifying the model name save in the /chk path
the run file will be save in the path /run and the score presented in the prompt
