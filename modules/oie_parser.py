from allennlp.predictors import Predictor 
from allennlp.models.archival import load_archive
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize



class OIEParser:
    def __init__(self):
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, '../oie parsing resources/openie-model.2020.03.26.tar.gz')
        self.predictor = Predictor.from_path(filename)


    def _run_predictor_sentence(self, sentence):
        value = self.predictor.predict(sentence)
        return value

    def remove_with_nltk(self, sentence):
        stop_words = set(stopwords.words('english')) 
        input_tokens = word_tokenize(sentence) 
        nltk_sentence = [w for w in input_tokens if not w in stop_words] 
        nltk_sentence = [] 
        for w in input_tokens: 
            if w not in stop_words: 
                nltk_sentence.append(w) 
        result_sentence = ""
        for f in nltk_sentence:
            result_sentence += f + " "
        return result_sentence

    def parse_sentence(self, sentence, nr_predicates = 0):
        tokenized_sentence = self._run_predictor_sentence(sentence)
        result_vector = []
        for word in tokenized_sentence["words"]:
            result_vector.append("")
        nr_verbs = 0
        if nr_predicates == 0:
            nr_verbs = len(tokenized_sentence["verbs"])
        else:
            nr_verbs = nr_predicates
        for i in range(nr_verbs):
            verb = tokenized_sentence['verbs'][i]
            tags = verb["tags"]
            t_count = 0
            for t in tags:
                if t != "O":
                    if result_vector[t_count] == "" :

                        result_vector[t_count] = tokenized_sentence["words"][t_count]
                t_count += 1
        final_string = ""
        for word in result_vector:
            if word != "" and word[0] != "'":
                final_string = final_string + word + " " 
        
        final_string = self.remove_with_nltk(final_string)
        return final_string

if __name__ == '__main__':

    nltk.download('stopwords')
    parser = OIEParser()
    res = parser.parse_sentence("Spain began to loosen its lockdown this week, but Phase 1 will include a considerable easing of measures that will allow people to move around their province as well as attend concerts and go to the theatre. Gatherings of up to 10 people will be allowed. ")
    print(res)