import csv
import json
import sys

class DatasetReader:
    def read_input(self, filename):
        corpus_sentences=[]
        with open(filename, encoding="utf8") as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if(row[0]!=None and row[2] != "sentence"):  
                    corpus_sentences.append({"truth_flag":row[1], "sentence":row[2]})
        with open('data/train_json.txt','w') as train_out_file:
            json.dump(corpus_sentences, train_out_file)

if __name__ == '__main__':    
    
    values = sys.argv
    if len(values) < 2:
        print("Please input the corpus file name")
        exit
    else:
        corpus = values[1]
        reader = DatasetReader()
        reader.read_input(corpus)