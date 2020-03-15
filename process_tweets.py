import pandas as pd
import re
from nltk.corpus import stopwords
import pickle
import wordninja
import ekphrasis
import numpy as np
from ekphrasis.classes.segmenter import Segmenter

stop_words = set()
stop_words.add("rt")
stop_words.add("RT")


def tokenizer(doc):
    # get letter language
    x1 = [c.lower() for c in doc.split() if c not in stop_words]
    x2 = [re.sub(r'\W+|https?://[a-zA-z./\d]*', '', w) for w in x1]
    # x2 = [re.sub(r'https?://[a-zA-z./\d]*', '', w) for w in x1]
    filtrate = re.compile(u'[^\u0020-\u007F]')  # non-Latin unicode range
    x3 = [filtrate.sub(r'', w) for w in x2]  # remove all non-Latin characters
    context = [c for c in x3 if c and not (re.match('^http', c))]
    return ' '.join(context)


def handle_tweets(df_tweets):
    seg_eng = Segmenter(corpus="english")
    texts = list(df_tweets["text"])
    #f = open(data_path + "abs_tweets.txt", "w")
    hashtags = []
    clean_tweets = []
    for t in texts:
        pattern = r'#\w+|#\w+$'
        remove = re.compile(pattern)
        removed_t = remove.sub(r'', t)
        matches = re.findall(pattern, t)
        hashes = [seg_eng.segment(i.lstrip('#').lower()) for i in matches]
        tweet = tokenizer(removed_t)
        clean_tweets.append(tweet)
        hashtags.append(hashes)
    #   f.write(tweet)
    #  f.write("\n")
    #f.close()
    return clean_tweets, hashtags


def handle_news(df_news):
    f = open(data_path + "abs_news.txt", "w")
    for i, row in df_news.iterrows():
        f.write(row["title"])
        f.write("\n")
    f.close()


def is_in_tweets(htags, tweet):
    exist = False
    for ht in htags:
        sequence = ht.split()
        raw_ht = ''.join(sequence)
        if raw_ht in tweet or any(word in tweet for word in sequence):
            exist = True
        if exist:
            break
    return exist


if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset

    df_tweets = pd.read_csv(data_path + "tweets.csv", encoding="utf-8", error_bad_lines=False)
    df_news = pd.read_csv(data_path + "news.csv", encoding="utf-8", error_bad_lines=False)
    df_news = df_news.dropna(subset=['title'])
    df_news = df_news.reset_index(drop=True)
    ht_in_tweet_idx = []
    ht_not_in_tweet_idx = []

    clean_tweets, hashtags = handle_tweets(df_tweets)
    # handle_news(df_news)
    # for i in range(len(df_tweets)):
    #     if is_in_tweets(hashtags[i], clean_tweets[i]):
    #         ht_in_tweet_idx.append(i)
    #     else:
    #         ht_not_in_tweet_idx.append(i)

    # clean_tweets = np.array([' '.join(t) for t in clean_tweets])
    hashtags = np.array([';'.join(t) for t in hashtags])
    df_tweets["Clean Tweets"] = clean_tweets
    df_tweets["Hashtags"] = hashtags

    # df_ht_in_tweets = df_tweets.iloc[ht_in_tweet_idx]
    # df_ht_not_intweets = df_tweets.iloc[ht_not_in_tweet_idx]

    pickle.dump(df_tweets, open(data_path + "df_tweets.pkl", "wb"))
    pickle.dump(df_news, open(data_path + "df_news.pkl", "wb"))

    # t = "this is a test tweet#sandiego #UnitedStates"
    # pattern = r'#\S+[ \t\n]|#\S+$'
    # remove = re.compile(pattern)
    # removed_t = remove.sub(r' ', t)
    # matches = re.findall(pattern, t)
    # hashes = [' '.join(wordninja.split(i)).lower() for i in matches]
    # print(removed_t)
    # print(hashes)
