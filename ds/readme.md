# Dataset and code
Instructions:

1)
Run `genOUT_GPT3.py` to generate the base model (GPT3) explanations.

It will use the samples random extracted from MSMARCO DS in the file `dsgpt3.tsv`.

The `prompt_model.txt` file will be used to extract the explanation from the base model.

2)
Run genDS_MonoT5v5.py to generate the dataset augmented with the explanation.

It will generate the dataset in the format used by the ExaRanker finetuning scripts.

Note:
The script `genDS_GPT3.py` is used to select 30k random samples from the MS MARCO's `triples.train.small.tsv` file.
This file can be downloaded from: "https://msmarco.blob.core.windows.net/msmarcoranking/triples.train.small.tar.gz"

The generated datasets are:

dsMonoT5v5.tsv - 30k examples augmented with explanations

dsMonoT5v5bin.tsv - 30k examples without explanations.
