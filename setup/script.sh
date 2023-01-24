#--------- para executar, abrir o terminal e executar:
#--------- bash setup/script.sh

sudo apt-get update
sudo apt-get install python3-pip
sudo apt install ubuntu-drivers-common
pip install wget
pip install transformers
pip install sentencepiece
pip install datasets
pip install pytorch-lightning==1.6.5
pip install neptune-client
pip install wikipedia
pip install gensim
pip install google-cloud
pip install gsutil
pip install requests -U
pip install pyserini==0.16
pip install faiss-cpu
pip install faiss-gpu
sudo apt install python-is-python3
sudo apt install default-jdk
pip install pygaggle
pip install openai



#--------- google bucket
# sudo apt-get install apt-transport-https ca-certificates gnupg
# echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
# curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
# sudo apt-get update && sudo apt-get install google-cloud-cli
# sudo apt-get install google-cloud-cli
# #--------- para conectar no google
# gcloud init
# gcloud auth login
# gcloud auth application-default login
# gsutil config

# #--------- drive nvidia
# sudo ubuntu-drivers autoinstall
# sudo apt install nvidia-driver-510
# sudo apt install nvidia-utils-510
# nvidia-smi

