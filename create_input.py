import pickle
import re
from sklearn.model_selection import train_test_split

stop_words = set()
stop_words.add("rt")
stop_words.add("RT")


def tokenizer(doc):
    # get letter language
    x1 = [c.lower() for c in doc.split() if not (re.match('^#|^@', c) or c in stop_words)]
    x2 = [re.sub(r'\W+|https?://[a-zA-z./\d]*', '', w) for w in x1]
    # x2 = [re.sub(r'https?://[a-zA-z./\d]*', '', w) for w in x1]
    filtrate = re.compile(u'[^\u0020-\u007F]')  # non-Latin unicode range
    x3 = [filtrate.sub(r'', w) for w in x2]  # remove all non-Latin characters
    context = [c for c in x3 if c and not (re.match('^http', c))]
    return " ".join(context)


def write_to_file(file_path, entities):
    f = open(file_path, "w")
    for t in entities:
        f.write(t)
        f.write("\n")
    f.close()


if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset

    tweet_news_map = pickle.load(open(data_path + "tweet_news_map.pkl", "rb"))
    news_phrase_dict = pickle.load(open(data_path + "news_phrase_dict.pkl", "rb"))
    tweet_phrase_dict = pickle.load(open(data_path + "tweet_phrase_dict.pkl", "rb"))
    df_tweets = pickle.load(open(data_path + "df_tweets.pkl", "rb"))
    df_news = pickle.load(open(data_path + "df_news.pkl", "rb"))

    all_tweets = []
    all_news = []
    all_tags = []

    for tweet_id in tweet_news_map:
        tweet = tweet_phrase_dict[tweet_id]["tweet"]
        clean_tweet = tokenizer(tweet).lower()
        all_tweets.append(clean_tweet)
        all_tags.append(df_tweets.iloc[tweet_id]["Hashtags"])

        clean_news_total = ""
        for news_id in tweet_news_map[tweet_id]:
            news = news_phrase_dict[news_id]["news"]
            clean_news = tokenizer(news).lower()
            clean_news_total = clean_news_total + " " + clean_news
        all_news.append(clean_news_total)

    tweets_train, tweets_test, news_train, news_test, tags_train, tags_test = train_test_split(all_tweets, all_news,
                                                                                               all_tags, test_size=0.1,
                                                                                               random_state=42)
    tweets_train, tweets_val, news_train, news_val, tags_train, tags_val = train_test_split(tweets_train, news_train,
                                                                                            tags_train, test_size=0.1,
                                                                                            random_state=42)

    write_to_file(data_path + "train_post.txt", tweets_train)
    write_to_file(data_path + "train_conv.txt", news_train)
    write_to_file(data_path + "train_tag.txt", tags_train)

    write_to_file(data_path + "valid_post.txt", tweets_val)
    write_to_file(data_path + "valid_conv.txt", news_val)
    write_to_file(data_path + "valid_tag.txt", tags_val)

    write_to_file(data_path + "test_post.txt", tweets_test)
    write_to_file(data_path + "test_conv.txt", news_test)
    write_to_file(data_path + "test_tag.txt", tags_test)
