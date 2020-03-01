import pickle
import re
import spacy
from nltk.corpus import stopwords
from nltk import stem
from rank_bm25 import BM25Okapi
import pandas as pd


nlp = spacy.load('en_core_web_md')
stemmer = stem.PorterStemmer()
stop_words = set(stopwords.words('english'))


def tokenizer(doc):
    # get letter language
    x1 = [c.lower() for c in doc.split() if c not in stop_words]
    x2 = [re.sub(r'\W+|https?://[a-zA-z./\d]*', '', w) for w in x1]
    filtrate = re.compile(u'[^\u0020-\u007F]')  # non-Latin unicode range
    x3 = [filtrate.sub(r'', w) for w in x2]  # remove all non-Latin characters
    context = [stemmer.stem(c) for c in x3 if c and not (re.match('^http', c))]
    return context


def is_in_news(htags, top_news):
    for ht in htags.split(";"):
        sequence = ht.split()
        raw_ht = ''.join(sequence)
        for n in top_news:
            if raw_ht in n or any(word in n for word in sequence):
                exist = True
                break
        if exist:
            break


def match(datapath):
    df_tweets = pickle.load(open(datapath+"df_tweets.pkl", "rb"))
    df_news = pickle.load(open(datapath+"df_news.pkl", "rb"))
    tweets = df_tweets["Clean Tweets"]
    hashtags = df_tweets["Hashtags"]
    raw_tweets = df_tweets["text"]
    news = list(df_news["title"])
    tokenized_tweets = [tokenizer(tweet) for tweet in list(tweets)]
    tokenized_news = [tokenizer(n) for n in news]
    processed_news = [' '.join(i) for i in tokenized_news]
    bm25 = BM25Okapi(tokenized_news)
    print("finished loading")
    ht_in_news = [["raw_tweet", "processed_tweet", "news", "hashtags"]]
    ht_not_in_news = [["raw_tweet", "processed_tweet", "news", "hashtags"]]
    for i, t in enumerate(tokenized_tweets):
        if i%500 == 0:
            print("************processed" + str(i) + "**************")
        # doc_scores = bm25.get_scores(t)
        # get the indices of top 5 matches news
        # res = sorted(range(len(doc_scores)), key=lambda sub: doc_scores[sub], reverse=True)[:5]
        matched_news = bm25.get_top_n(t, processed_news, n=5)
        hashes = hashtags[i]
        raw = raw_tweets[i]
        exist = is_in_news(hashes, matched_news)
        if exist:
            ht_in_news.append([raw, ' '.join(t), ';'.join(matched_news), hashes])
        else:
            ht_not_in_news.append([raw, ' '.join(t), ';'.join(matched_news), hashes])

    df_ht_not_in_news = pd.DataFrame(ht_not_in_news[1:], columns=ht_not_in_news[0])
    df_ht_in_news = pd.DataFrame(ht_in_news[1:], columns=ht_in_news[0])
    print("ht in news: " + str(len(ht_in_news)-1))
    print("ht not in news: " + str(len(ht_not_in_news)-1))
    df_ht_in_news.to_pickle(datapath+"ht_in_news.pkl")
    df_ht_not_in_news.to_pickle(datapath+"ht_not_in_news.pkl")


if __name__ == '__main__':
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset
    match(data_path)












