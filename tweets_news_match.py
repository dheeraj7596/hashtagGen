import pickle
import re
import spacy
from nltk.corpus import stopwords
from nltk import stem
from rank_bm25 import BM25Okapi
import pandas as pd
import numpy as np
from process_tweets import tokenizer

nlp = spacy.load('en_core_web_md')
stemmer = stem.PorterStemmer()
stop_words = set(stopwords.words('english'))


# def tokenizer(doc):
#     # get letter language
#     x1 = [c.lower() for c in doc.split() if c not in stop_words]
#     x2 = [re.sub(r'\W+|https?://[a-zA-z./\d]*', '', w) for w in x1]
#     filtrate = re.compile(u'[^\u0020-\u007F]')  # non-Latin unicode range
#     x3 = [filtrate.sub(r'', w) for w in x2]  # remove all non-Latin characters
#     context = [stemmer.stem(c) for c in x3 if c and not (re.match('^http', c))]
#     return context


def match(datapath):
    df_tweets = pickle.load(open(datapath+"df_tweets.pkl", "rb"))
    df_news = pickle.load(open(datapath+"df_news.pkl", "rb"))
    tweets = list(df_tweets["Clean Tweets"])[:10]
    hashtags = list(df_tweets["Hashtags"])[:10]
    # raw_tweets = df_tweets["text"]
    news = list(df_news["title"])
    tokenized_tweets = [[stemmer.stem(c) for c in tweet.split()] for tweet in tweets]
    processed_news =  [tokenizer(n) for n in news]
    tokenized_news = [[stemmer.stem(c) for c in n.split()] for n in processed_news]
    # processed_news = [' '.join(i) for i in tokenized_news]
    bm25 = BM25Okapi(tokenized_news)
    print("finished loading")
    dataset = [["processed tweets", "news_index", "scores", "hashtags"]]
    # ht_not_in_news = [["raw_tweet", "processed_tweet", "news", "hashtags"]]
    # df_matched_news = pd.DataFrame(columns=["score"])
    for i, t in enumerate(tokenized_tweets):
        if i%500 == 0:
            print("************processed" + str(i) + "**************")
        # doc_scores = bm25.get_scores(t)
        # get the indices of top 5 matches news
        # res = sorted(range(len(doc_scores)), key=lambda sub: doc_scores[sub], reverse=True)[:5]
        # check = bm25.get_top_n(t, processed_news, n=5)
        news_scores = bm25.get_scores(t)
        ind = np.argpartition(news_scores, -20)[-20:]
        sorted_ind = ind[np.argsort(np.array(news_scores)[ind])][::-1]
        # matched_news = [processed_news[i] for i in sorted_ind]
        # news_string = ' '.join(matched_news)
        top_scores = [news_scores[i] for i in sorted_ind]
        dataset.append([tweets[i], sorted_ind, top_scores, hashtags[i]])

    #     hashes = hashtags[i]
    #     raw = raw_tweets[i]
    #     if is_in_news(hashes, matched_news):
    #         ht_in_news.append([raw, ' '.join(t), ';'.join(matched_news), hashes])
    #     else:
    #         ht_not_in_news.append([raw, ' '.join(t), ';'.join(matched_news), hashes])
    #
    df_news_match = pd.DataFrame(dataset[1:], columns=dataset[0])
    df_news_match.to_pickle(datapath+"news_match.pkl")
    df_news_match.to_csv(datapath+"news_match.csv")
    # df_ht_in_news = pd.DataFrame(ht_in_news[1:], columns=ht_in_news[0])
    # print("ht in news: " + str(len(ht_in_news)-1))
    # print("ht not in news: " + str(len(ht_not_in_news)-1))
    # df_ht_in_news.to_pickle(datapath+"ht_in_news.pkl")
    # df_ht_not_in_news.to_pickle(datapath+"ht_not_in_news.pkl")


if __name__ == '__main__':
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset
    match(data_path)












