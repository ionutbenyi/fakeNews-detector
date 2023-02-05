import json
import os
import re
from modules.oie_parser import OIEParser
import sys


class KeywordSelector:

    def __init__(self, oie_parser, allow_logs):
        self.parser = oie_parser
        self.allow_logs = allow_logs

    def split_into_keywords(self, sentence, truth_flag = 0):
        if len(sentence) > 100:
            split_string = self.parser.parse_sentence(sentence)
        else: 
            # print('len not grater than 160')
            split_string = sentence

        if self.allow_logs:
            print(split_string)
        split_json = {"search": split_string, "original": sentence, "truth_flag": truth_flag}
        return split_json

    def sentence_reduction(self, lower_limit, upper_limit):
         # read the data from text json
        input_train_data=[]
        try:
            with open('data/train_json.txt') as input_json_set:
                input_train_data = json.load(input_json_set)
        except FileNotFoundError:
                print("ERROR: train_json.txt doesn't exist - run the dataset reader:")
                print("python -m modules.dataset_reader")
                return
        
        search_strings = []
        count = 0

        if upper_limit != -1:
            for i in range(upper_limit):
                if i >= lower_limit:
                    input_json = input_train_data[i]
                    print(count)
                    
                    final_string = self.split_into_keywords(input_json['sentence'], input_json["truth_flag"])
                    print("O: "+ input_json['sentence'])
                    print("S:"+ final_string["search"])
                    search_strings.append(final_string)
                
                count += 1
        else:
            for input_json in input_train_data:
                print(count)
                final_string = self.split_into_keywords(input_json['sentence'], input_json["truth_flag"])
                print("O: "+ input_json['sentence'])
                print("S:"+ final_string["search"])
                search_strings.append(final_string)
                count += 1

        with open('data/search_inputs.txt','w') as search_inputs_file:
            json.dump(search_strings, search_inputs_file)


if __name__ == '__main__':

    values = sys.argv

    lower_limit = 0
    upper_limit = 0

    if len(values) == 3:
        lower_limit = int(values[1])
        upper_limit = int(values[2])
    else:
        upper_limit = -1

    parser = OIEParser()
    keywd_selector = KeywordSelector(parser, True)
    keywd_selector.sentence_reduction(lower_limit, upper_limit)
   