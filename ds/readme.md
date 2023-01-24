Steps

1)
Run genOUT_GPT3.py to generate the base model (GPT3) explanations
It will use the samples random extracted from MSMARCO DS in the file dsgpt3.tsv
The prompt_model.txt will be used to extract the explanation from the base model

2)
Run genDS_MonoT5v5.py to generate the data set augment with the explanation
It will generate the data set in the format used by the ExaRanker model

Note:
the code genDS_GPT3.py is the code used to select the random samples (30k) MSMARCO using the triples.train.small.tsv
This file can be downloaded from: "https://msmarco.blob.core.windows.net/msmarcoranking/triples.train.small.tar.gz"

The datasets are:
dsMonoT5v5.tsv - 30k dataset augmented with explanation
dsMonoT5v5bin.tsv - - 30k dataset without explanation
