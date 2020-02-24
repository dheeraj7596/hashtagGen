from bs4 import BeautifulSoup
import bleach
import pickle

if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset
    df_tweets = pickle.load(open(data_path + "df_tweets.pkl", "rb"))
    df_news = pickle.load(open(data_path + "df_news.pkl", "rb"))
    out_tweets_path = data_path + "segmentation_tweets.txt"
    # out_news_path = data_path + "segmentation_news.txt"

    f = open(out_tweets_path, "r")
    tweet_lines = f.readlines()
    f.close()
    #
    # f = open(out_news_path, "r")
    # news_lines = f.readlines()
    # f.close()

    tweet_phrase_dict = {}
    for i, line in enumerate(tweet_lines):
        line = line.lower()
        soup = BeautifulSoup(line)
        phrases = set()
        for p in soup.findAll("phrase"):
            phrase = p.string
            phrases.add(phrase)
        if len(phrases) > 0:
            temp_str = bleach.clean(str(soup), tags=[], strip=True)
            tweet_phrase_dict[i] = {"tweet": temp_str, "phrase": phrases}

    news_phrase_dict = {}
    for i, line in enumerate(list(df_news.title)):
        line = line.lower()
        news_phrase_dict[i] = {"news": line, "phrase": set(line.strip().split())}
        # soup = BeautifulSoup(line)
        # phrases = set()
        # for p in soup.findAll("phrase"):
        #     phrase = p.string
        #     phrases.add(phrase)
        # if len(phrases) > 0:
        #     temp_str = bleach.clean(str(soup), tags=[], strip=True)
        #     news_phrase_dict[i] = {"news": temp_str, "phrase": phrases}

    tweet_news_map = {}
    for j in news_phrase_dict:
        title = news_phrase_dict[j]["news"]
        for i in tweet_phrase_dict:
            count = 0
            tweet_phrases = tweet_phrase_dict[i]["phrase"]
            for ph in tweet_phrases:
                if ph in title:
                    count += 1
            if count >= 2:
                try:
                    tweet_news_map[i].append(j)
                except:
                    tweet_news_map[i] = [j]

    print("Final number of tweets: ", len(tweet_news_map))
    pickle.dump(tweet_news_map, open(data_path + "tweet_news_map.pkl", "wb"))
    pickle.dump(news_phrase_dict, open(data_path + "news_phrase_dict.pkl", "wb"))
    pickle.dump(tweet_phrase_dict, open(data_path + "tweet_phrase_dict.pkl", "wb"))
