from modules.web_query import WebQuery
import requests
from bs4 import BeautifulSoup
import html2text
from requests.exceptions import Timeout
import urllib

import json
import re


class DocGatherer:

    def __init__(self, allow_logs):
        self.allow_logs = allow_logs

    def check_bad_sites(self,url):
        bad_urls = ['bit.ly', 'PDF', 'fuck', 'viewcontent.cgi', 'pdf', '.pdf', '.ashx',
        '/pdf/', 'send_file', 'article_list.pl', '.jsp', 'youtube.com']
        for u in bad_urls:
            if u in url:
                return False
        return True

    def get_encoding(self,soup):
        if soup and soup.meta:
            encoding = soup.meta.get('charset')
            if encoding == None:
                encoding = soup.meta.get('content-type')
                if encoding == None:
                    content = soup.meta.get('content')
                    match = re.search('charset=(.*)', content)
                    if match:
                        encoding = match.group(1)
                    else:
                        raise ValueError('unable to find encoding')
        else:
            raise ValueError('unable to find encoding')
        return encoding

    def check_articles(self, keyword_sentence, original_sentence, link_scraper):
        # print('enter function')
        total_sites_nr = 0
        uls=[]
        try:
            url_list = link_scraper.search_for_link(keyword_sentence)
            # print('done search')
        except urllib.error.URLError:
            print('URL error, returning')
            return
        for u in url_list:
            if self.check_bad_sites(u):
                uls.append(u)
        articles = []
        if self.allow_logs:
            print(keyword_sentence)
        for i in range(len(uls)):
            if total_sites_nr < 5:
                if self.allow_logs:
                    print(uls[i])
                article_text=""
                try:
                    r=None
                    try:
                        r = requests.get(uls[i], timeout=3.5)
                    except requests.exceptions.HTTPError:
                        continue
                    except requests.exceptions.TooManyRedirects:
                        continue
                    except requests.exceptions.RequestException:
                        continue
                    except requests.exceptions.Timeout:
                        print('The request timed out')
                        continue
                    except urllib.error.URLError:
                        print('Error on URL article, skipping')
                        continue
                    soup = BeautifulSoup(r.content, 'html5lib')

                    try:
                        encd = self.get_encoding(soup)
                    except:
                        encd = ""
                    if encd == 'utf-8' or encd == 'UTF-8' or encd == "":
                        table = soup.findAll('p', attrs={})
                        h = html2text.HTML2Text()
                        h.ignore_links = True

                        if table:
                            for row in table:
                                str_row = str(row)
                                #article text per paragraphs
                                row_text = h.handle(str_row)
                                if not '**Contact us** at editors@time.com.' in row_text:
                                    article_text += row_text
                                article_text = article_text.replace("\n\n\n\n","\n")
                            total_sites_nr += 1
                            
                            articles.append({"source":uls[i], "content":article_text})
                            
                except:
                    continue

        return articles

    def gather_articles_for_sentence(self, sentence, keyword_sentence, link_scraper):
        articles = self.check_articles(keyword_sentence, sentence, link_scraper)
        articles_json = {"sentence": sentence, "truth_flag":0, "texts": articles}
        return articles_json


if __name__ == '__main__':

    doc_gatherer = DocGatherer(True)
    input_train_data=[]
    count_facts_total = 0
    count_facts_found = 0
    count_counterfacts_total = 0
    count_counterfacts_found = 0

    try:
        with open('data/search_inputs.txt') as input_json_set:
            input_train_data = json.load(input_json_set)
    except FileNotFoundError:
        print("ERROR: search_inputs.txt doesn't exist - run the keyword selector:")
        print("python -m modules.keyword_selector lower_limit upper_limit")
        print("If you want the full dataset to be read, do not add lower_limit and upper_limit")
        exit

    art_final = []
    count = 1
    link_scraper = WebQuery()
    for train_sentence in input_train_data:
        print(count)
        article_texts = []
        try:
            article_texts = doc_gatherer.check_articles(train_sentence["search"], train_sentence["original"], link_scraper)
        except requests.exceptions.Timeout:
            print('The request timed out')
            continue
        except urllib.error.URLError:

            try:
                article_texts = doc_gatherer.check_articles(train_sentence["search"], train_sentence["original"], link_scraper)
            except urllib.error.URLError:
                print('Error on URL, skipping')
                print('On: '+ train_sentence['search'])
                print('Original: '+ train_sentence['original'])
                count += 1
                continue
        
        art_final.append({"sentence": train_sentence["original"], "truth_flag":train_sentence["truth_flag"], "texts":article_texts})
        count += 1

    with open('data/articles.txt','w') as outp_data:
        json.dump(art_final, outp_data)