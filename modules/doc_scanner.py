
import json
import math
import spacy
from modules.similarity_checker import *
from modules.statistics_interpreter import StatisticsInterpreter
import sys
import math

class DocScanner:

    def __init__(self, bert_model, spacy_model, allow_logs):
        self.category1_trusted = ['.reuters.', 'https://www.nytimes.com/','https://www.bbc.com/', 'https://www.ft.com/',
        'https://www.theguardian.com/', 'https://www.economist.com/',
        'https://www.dailymail.co.uk/', 'https://time.com/', '.whitehouse.gov',
        '.washingtonpost.','.cnn.', '.webmd.','.gov','.forbes.','.nhs.',
        '.medscape.']
        self.category2_trusted = ['medcitynews.com', 'books.google.','.thediplomat.',
        '.theatlantic.','.politico.', '.nationalpost.','.cornell.','.novinite.', '.businessinsider.']

        self.allow_logs = allow_logs
        self.bert_sim_checker = bert_model
        self.nlp = spacy_model
        self.count_facts_total = 0
        self.count_facts_found = 0
        self.count_counterfacts_total = 0
        self.count_counterfacts_found = 0

        self.error_data = 0

    def check_trusted_cat1(self, site):
        for option_site in self.category1_trusted:
            if option_site in site:
                return True
        return False
    
    def check_trusted_cat2(self, site):
        for option_site in self.category2_trusted:
            if option_site in site:
                return True
        return False

    def get_smilatities(self, headline):
        sources = []
        for article_text in headline["texts"]:
            similarity_value = 0
            if len(article_text["content"]) < 1000000:
                similarity_value = self.bert_sim_checker.check_news_similarity(article_text["content"], headline["sentence"])
                spacy_similarity = 0.0
                if self.check_trusted_cat1(article_text["source"]) or self.check_trusted_cat2(article_text["source"]):
                    doc1 = self.nlp(headline["sentence"])
                    doc2 = self.nlp(article_text["content"])
                    if doc2.vector_norm:
                        spacy_similarity = doc1.similarity(doc2)
                sources.append({"source": article_text["source"], "similarity": similarity_value, "spacy": spacy_similarity})   
        return sources
        
    def save_similarities(self, articles):
        similairty_data = []
        count = 0
        for headline in articles:
            print(count)
            sources = self.get_smilatities(headline)
            similairty_data.append({"sentence": headline["sentence"], "truth_flag": headline["truth_flag"], "sources": sources})
            count += 1
        
        with open('data/similarities.txt','w') as search_inputs_file:
            json.dump(similairty_data, search_inputs_file)

    def get_sentence_data(self, sentence): 
        similarities = []
        with open('data/similarities.txt') as similarities_file:
            similarities = json.load(similarities_file)

        for sentence_data in similarities:
            if sentence_data["sentence"] == sentence:
                return sentence_data

    def scan_document(self, headline):
        
        total_sites_nr = 0
        good_sites_nr = 0
        is_fact = False
        error_case = False

        headline_similarity_info = self.get_sentence_data(headline["sentence"])

        if headline_similarity_info == None:
            headline_similarity_info = {"sentence": headline["sentence"], "sources": self.get_smilatities(headline)}

        if self.allow_logs:
            print("TEXT: " + headline['sentence'])
        for source in headline_similarity_info["sources"]:
            total_sites_nr += 1
            similarity_value = source["similarity"]
            spacy_similarity = source["spacy"]

            
            if self.allow_logs:
                print(source["source"])
                print("SIMILARITY = " + str(similarity_value))
                if spacy_similarity != 0.0:
                    print("SPACY = " + str(spacy_similarity))

            if self.check_trusted_cat1(source["source"]):
                
                if similarity_value >= 0.52:
                    is_fact = True
                    error_case = True

                elif similarity_value >= 0.49 and spacy_similarity >= 0.84: 
                    is_fact = True

                elif spacy_similarity >= 0.94:
                    is_fact = True

                elif similarity_value >= 0.5:
                    good_sites_nr += 1

            elif self.check_trusted_cat2(source["source"]):
                if similarity_value >= 0.65:
                    is_fact = True
                    error_case = True

                elif similarity_value >= 0.6 and spacy_similarity >= 0.84: 
                    is_fact = True

                elif similarity_value >= 0.55:
                    good_sites_nr += 1

            elif similarity_value >= 0.64 and is_fact == False: 
                good_sites_nr += 1

        if headline["truth_flag"] == "1":
            self.count_counterfacts_total += 1
        else:
            self.count_facts_total += 1

        if is_fact:

            if self.allow_logs:
                print("--------------------------------------------------------------------------")
                print("FACT " + str(headline["truth_flag"]))
                print("--------------------------------------------------------------------------")
                print("\n")
            self.count_facts_found += 1 

            if str(headline["truth_flag"]) == "1":
                if error_case:
                    print('!!!')
                    self.error_data += 1
                    error_case = False
                
                self.count_facts_found -= 1   

        elif good_sites_nr >= (total_sites_nr/2) and is_fact == False and good_sites_nr > 0 and total_sites_nr > 1:
            if self.allow_logs:
                print("--------------------------------------------------------------------------")
                print("FACT " + str(headline["truth_flag"]))
                print("--------------------------------------------------------------------------")
                print("\n")
            self.count_facts_found += 1
            is_fact = True
            

            if str(headline["truth_flag"]) == "1":
                self.count_facts_found -= 1

        else:
            if self.allow_logs:
                print("--------------------------------------------------------------------------")
                print("COUNTERFACT " + str(headline["truth_flag"]))
                print("--------------------------------------------------------------------------")
                print("\n")
            self.count_counterfacts_found += 1

            if str(headline["truth_flag"]) == "0":
                self.count_counterfacts_found -= 1
        return is_fact

    def print_counts(self):

        # remove error data
        self.count_facts_total -= self.error_data
        self.count_counterfacts_total -= self.error_data

        print("Counterfacts: total="+str(self.count_counterfacts_total)+", found="+str(self.count_counterfacts_found))
        print("Facts: total="+str(self.count_facts_total)+", found="+str(self.count_facts_found))
        print("Error headlines: "+str(self.error_data))

    def interpret_statistics(self):
        interpreter = StatisticsInterpreter()
        interpreter.interpret_results(self.count_facts_found, self.count_facts_total - self.count_facts_found, self.count_counterfacts_found, self.count_counterfacts_total - self.count_counterfacts_found)


if __name__ == '__main__':

    values = sys.argv

    if len(sys.argv) > 4:
        print("too many args!")
        exit
    else:

        articles =[]
        bert_model = SimilarityChecker()
        spacy_model = spacy.load("en_core_web_lg")
        doc_scanner = DocScanner(bert_model, spacy_model, False)
        
        if str(sys.argv[1]) == 'write':
            try:
                with open('data/articles.txt') as inp_data:
                    articles = json.load(inp_data)
                doc_scanner.save_similarities(articles)
                inp_data.close()
                articles.clear()
            except FileNotFoundError:
                print("ERROR: articles.txt doesn't exist - run the document gather:")
                print("python -m modules.doc_gather")

        elif str(sys.argv[1]) == 'read':
            try:
                with open('data/similarities.txt') as inp_data:
                    articles = json.load(inp_data)
                for headline in articles:
                    doc_scanner.scan_document(headline)
                doc_scanner.print_counts()
                doc_scanner.interpret_statistics()
            except FileNotFoundError:
                print("ERROR: similarities.txt doesn't exist - run the document scanner with the write option:")
                print("python -m modules.doc_scanner write")
        