# ExaRanker

[Link to the paper](https://arxiv.org/pdf/2301.10521.pdf) (published at SIGIR 2023)

This repository contains the code and dataset used to generate the ExaRanker model.

Summary:

* **/ds**: path to generate the dataset augmented with explanations

* **/monoT5-bin-plus**: finetunning and inference for the ExaRanker model

* **/monoT5-bin**: finetunning and inference for the T5 model (baseline model)

<img src="https://user-images.githubusercontent.com/26362929/234304094-8ea0121e-bc39-4941-ad9d-506f5a21d16a.png" width="629" height="441">

<img src="https://user-images.githubusercontent.com/26362929/234306391-42acaf11-dd12-4cb9-9b60-c4f8bd632078.png" width="627" height="230">

# How to cite this work
```
@inproceedings{10.1145/3539618.3592067,
    author = {Ferraretto, Fernando and Laitz, Thiago and Lotufo, Roberto and Nogueira, Rodrigo},
    title = {ExaRanker: Synthetic Explanations Improve Neural Rankers},
    year = {2023},
    isbn = {9781450394086},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3539618.3592067},
    doi = {10.1145/3539618.3592067},
    booktitle = {Proceedings of the 46th International ACM SIGIR Conference on Research and Development in Information Retrieval},
    pages = {2409–2414},
    numpages = {6},
    keywords = {multi-stage ranking, few-shot models, explanations, large language models, synthetic datasets, generative models},
    location = {<conf-loc>, <city>Taipei</city>, <country>Taiwan</country>, </conf-loc>},
    series = {SIGIR '23}
}
```
