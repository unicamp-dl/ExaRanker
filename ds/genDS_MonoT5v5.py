# generate N samples from DS MSMARCO+GPT3
import os
import csv
import json

os.system('clear')


#control flags
#run verbose
verbose = 0

#demo
demo = 0

if demo==1:
    file_run = "ds/dsgpt3demo.tsv"
    outfile = "ds/dsMonoT5v5.tsv"
else:
    file_run = "ds/dsgpt3.tsv"
    outfile = "ds/dsMonoT5v5.tsv"


id = 0


with open(outfile, "w", newline='') as record_file:
    tsv_writer = csv.writer(record_file, delimiter="\t")
    with open(file_run, encoding='utf8') as filein:
        f = csv.reader(filein, delimiter="\t")
        tsv_writer.writerow(['label','input','output'])    
        for line in f:
            label = line[0]
            if label =='0':
                labeltxt = "false. "
            else:
                labeltxt = "true. "

            query = line[1]
            doc = line[2]
            
            fname = 'ds/out_gpt3/output'+ str(id) + '.json'

            
            with open(fname) as json_file:
                dict = json.load(json_file) 
            json_file.close()

            input = "Is the question: \"" + query + "\" answered by the document: \"" + doc + "\"? Give an explanation."
            
            output = labeltxt + "Explanation:" + dict["text"].replace("\n", "")

            if verbose ==1:
                print('### ' + str(id) + ' ---------------------------------')
                print('### LABEL: ' + label)
                print('### INPUT:')
                print(input)
                print('### OUTPUT:')
                print(output)
                print()
            id = id+1
            tsv_writer.writerow([label,input,output])




