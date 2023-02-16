# ExaRanker finetuning and inference
Instructions:

1) To finetune the model run the code main_trainer.py
the checkpoint will be saved in `/chk`.

2) To generate the outputs from the finetuned model, run `run.py` specifying the model name saved in the `/chk` path. The outputs will be saved in a json file in the `/chk/model_name/out2` folder.

3) To calculate the model score and rerank the passage from TREC-DL 2020, run `gen_monot5.py` specifying the model name saved in the `/chk` path. The run file will be saved in the path `/run` and the scores will be presented in the prompt.
