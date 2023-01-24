#utiliza todo o texto predito pelo gpt3
import json
import os
import math

os.system('clear')

#control flags
#rodar em arquivo reduzido
demo = 0
#rodar verboso
verbose = 0

#model name
model_n = 500

if demo ==1 :
    file_run = 'baseline/run.dl20demo.txt'
    file_newrun = 'monoT5-bin-plus/run/runT5v1-' + str(model_n) + '.dl20demo.txt'
else:
    file_run = 'baseline/run.dl20.txt'
    file_newrun = 'monoT5-bin-plus/run/runT5v1-' + str(model_n) + '.dl20.txt'


def mygetKey(dict,index):
    return dict["tokens"][index]

def mygetValue(dict,index):
    return dict["scores"][index]


id = 0

fn_run = open(file_newrun, 'w')

with open(file_run, encoding='utf8') as f:
    for line in f:
        stringl = line.split()
        txt_out = stringl[0] + ' Q0 ' + stringl[2] + ' 1'

        fname = 'monoT5-bin-plus/chk/model-' + str(model_n) + '/out2/output' + str(id) + '.json'
        
        
        with open(fname) as json_file:
            dict = json.load(json_file) 
        json_file.close()

        
        len_in = -len(dict["scores"])         
        index = 0
        
        count_i = 0
        sum_i = 0
        flag_rel = 1 #set as 0 if NOT is founded
        
        if (mygetKey(dict,index).upper().strip() == 'FALSE'):
            flag_rel = 0
            #print('ID: ' + str(id) + ' not an answer')
        
        count_i = count_i+1
        sum_i = sum_i + math.exp(mygetValue(dict,index))


        
        if count_i ==0:
            print('ID: ' + str(id) + ' ------ ERROR term not found')
            count_i = 1
            avg_rel = 0
        else:
            avg_rel = sum_i / count_i
            #avg_rel = math.exp(sum_i / count_i)
        
        if flag_rel ==0 and avg_rel > 0:
            avg_rel = 1 - avg_rel
        elif flag_rel ==1 and avg_rel > 0:
            avg_rel = 1 + avg_rel

        if avg_rel < 0:
            avg_rel=0
            print('set down --------')

        id = id + 1
        txt_out = txt_out + ' ' + str(round(avg_rel,10)) + ' Anserini\n'
        
        fn_run.write(txt_out)


f.close()
fn_run.close()


#order rank ----------------------------------------------------------------------------
xx = []
with open(file_newrun, encoding='utf8') as f:
    for line in f:
        xx.append(line.split())
f.close()


sref= -1   
top_n = 1000
i = 0
xo = []
ixo = 0
rankn=0
offset = 0
while offset < len(xx):
    while rankn < top_n:
        while i+offset < top_n+offset:
            sin = xx[i+offset][4]
            if float(sin)>sref:
                sref=float(sin)
                ixo=i+offset
            i = i +1
        rankn = rankn+1
        xx[ixo][4] = -1
        sref = -1
        i=0
        xo.append(ixo)
    rankn = 0
    offset = offset + top_n



xx = []
with open(file_newrun, encoding='utf8') as f:
    for line in f:
        xx.append(line.split())
f.close()

fn_run = open(file_newrun, 'w')
i=0
rankn = 1
while i < len(xo):
    txt_out = xx[xo[i]][0] + ' ' + xx[xo[i]][1] + ' ' + xx[xo[i]][2] + ' ' + str(rankn) + ' ' + xx[xo[i]][4] + ' ' + xx[xo[i]][5] + '\n'
    fn_run.write(txt_out)
    rankn = rankn +1
    if rankn > 1000:
        rankn = 1
    i = i +1

fn_run.close()

print()
print('-------------------------------------------------------------------------')
print('-------------------------------------------------------------------------')
print('-------------------------------------------------------------------------')
print()
#generate score
os.system('python -m pyserini.eval.trec_eval -m all_trec rerankgpt3-1k/qrels.dl20-passage.txt ' + file_newrun)
