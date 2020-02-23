import pandas as pd
import re
from nltk.corpus import stopwords
import pickle
import wordninja

stop_words = set()
stop_words.add("rt")
stop_words.add("RT")


def tokenizer(doc):
    # get letter language
    x1 = [c.lower() for c in doc.split() if not (re.match('^#|^@', c) or c in stop_words)]
    # x2 = [re.sub(r'\W+|https?://[a-zA-z./\d]*', '', w) for w in x1]
    x2 = [re.sub(r'https?://[a-zA-z./\d]*', '', w) for w in x1]
    filtrate = re.compile(u'[^\u0020-\u007F]')  # non-Latin unicode range
    x3 = [filtrate.sub(r'', w) for w in x2]  # remove all non-Latin characters
    context = [c for c in x3 if c and not (re.match('^http', c))]
    return " ".join(context)


def handle_tweets(df_tweets):
    texts = list(df_tweets["text"])
    f = open(data_path + "abs_tweets.txt", "w")
    hashtags = []
    clean_tweets = []
    for t in texts:
        hashes = []
        for i, str in enumerate(t.split()):
            if str.startswith('#'):
                segmented_hash = ' '.join(wordninja.split(str))
                hashes.append(segmented_hash)
        tweet = tokenizer(t)
        clean_tweets.append(tweet)
        hashtags.append(';'.join(hashes))
        f.write(tweet)
        f.write("\n")
    f.close()
    return clean_tweets, hashtags


def handle_news(df_news):
    f = open(data_path + "abs_news.txt", "w")
    for i, row in df_news.iterrows():
        f.write(row["title"])
        f.write("\n")
    f.close()


if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset

    df_tweets = pd.read_csv(data_path + "tweets.csv", encoding="utf-8", error_bad_lines=False)
    df_news = pd.read_csv(data_path + "news.csv", encoding="utf-8", error_bad_lines=False)
    df_news = df_news.dropna(subset=['title'])
    df_news = df_news.reset_index(drop=True)

    clean_tweets, hashtags = handle_tweets(df_tweets)
    handle_news(df_news)
    df_tweets["Clean Tweets"] = clean_tweets
    df_tweets["Hashtags"] = hashtags

    pickle.dump(df_tweets, open(data_path + "df_tweets.pkl", "wb"))
    pickle.dump(df_news, open(data_path + "df_news.pkl", "wb"))
