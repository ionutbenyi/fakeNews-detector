from sentence_transformers import SentenceTransformer
import scipy.spatial

class SimilarityChecker:

    def __init__(self):
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')

    def check_news_similarity(self, article_text, sentence):
        sentence_l = [sentence]
        article_l = [article_text]
        text_embeddings = self.model.encode(article_l)
        sentence_embeddings = self.model.encode(sentence_l)

        distance = scipy.spatial.distance.cdist(sentence_embeddings, text_embeddings, "cosine")[0]
        results = zip(range(len(distance)), distance)
       
        results = sorted(results, key=lambda x: x[1])
       
        max_similarity = 1 - results[0][1]
        return max_similarity

if __name__ == '__main__':
    cheker = SimilarityChecker()
    sent1 = "Angela Merkel told Britain they would lose out if it left the EU."
    sent2 = "The German Chancellor told the UK it would lose if it were to leave the EU."
    sent3 = "Angela Merkel told Britain they would lose out if it left the EU. The quick brown fox jumps over the lazy dog."

    sim1 = cheker.check_news_similarity(sent1, sent2)
    sim2 = cheker.check_news_similarity(sent1, sent3)

    print("sim1 = "+ str(sim1))
    print("sim2 = "+ str(sim2))