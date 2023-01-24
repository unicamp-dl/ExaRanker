#gera os N samples a partir do MSMARCO triples train
from base64 import encode
import csv
from random import seed
from random import randint
import os
os.system('clear')


# parameters
#num_samples_ds = 3
num_samples_ds = 20000

datafile = "ds/triples.train.small.tsv" #not available in this repo - extract from web
outfile = "ds/dsgpt3.tsv"


#random parameters
#num_samples_msmarco = 100
num_samples_msmarco = 39780811

seed(2)
rand_step = 10
class_rel = 0

with open(outfile, "w", newline='') as record_file:
    tsv_writer = csv.writer(record_file, delimiter="\t")
    with open(datafile, encoding='utf-8') as file:
        
        tsv_file = csv.reader(file, delimiter="\t")
        
        rand_offset = randint(0, rand_step)
        i = 0
        csamples= 0
        
        for line in tsv_file:
            if i == rand_offset:
                print(i)
                if class_rel == 1:
                    #print('Relevant ----')
                    #print(line[0])
                    #print(line[1])
                    #print()
                    tsv_writer.writerow([str(class_rel),line[0],line[1]])
                    class_rel =0
                    
                else:
                    #print('Not Relevant ----')
                    #print(line[0])
                    #print(line[2])
                    #print()    
                    tsv_writer.writerow([str(class_rel),line[0],line[2]])
                    class_rel =1
                    
                
                print()
                csamples = csamples + 1
                rand_offset = i + randint(1, rand_step)
            
            if csamples == num_samples_ds:
                break

            i = i +1    
        
        
            
