import pandas as pd
import re
from nltk.corpus import stopwords

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


if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset

    df_tweets = pd.read_csv(data_path + "tweets.csv", encoding="utf-8", error_bad_lines=False)
    df_news = pd.read_csv(data_path + "news.csv", encoding="utf-8", error_bad_lines=False)

    texts = list(df_tweets["text"])
    f = open(data_path + "abs_tweets.txt", "w")
    hashtags = []
    clean_tweets = []
    for t in texts:
        hashes = []
        for i, str in enumerate(t.split()):
            if str.startswith('#'):
                hashes.append(str)
        tweet = tokenizer(t)
        clean_tweets.append(tweet)
        f.write(tweet)
        f.write("\n")
    f.close()
    pass
