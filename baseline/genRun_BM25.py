import os
#generate run
os.system('python -m pyserini.search --topics baseline/topics.dl20.tsv --index msmarco-passage --output baseline/run.dl20.txt --bm25 --hits 1000')
#generate score
os.system('python -m pyserini.eval.trec_eval -m all_trec baseline/qrels.dl20-passage.txt baseline/run.dl20.txt')