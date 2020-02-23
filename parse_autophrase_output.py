from bs4 import BeautifulSoup
import bleach
import pickle

if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset
    out_tweets_path = data_path + "segmentation_tweets.txt"
    out_news_path = data_path + "segmentation_news.txt"

    f = open(out_tweets_path, "r")
    tweet_lines = f.readlines()
    f.close()

    f = open(out_news_path, "r")
    news_lines = f.readlines()
    f.close()

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
    for i, line in enumerate(news_lines):
        line = line.lower()
        soup = BeautifulSoup(line)
        phrases = set()
        for p in soup.findAll("phrase"):
            phrase = p.string
            phrases.add(phrase)
        if len(phrases) > 0:
            temp_str = bleach.clean(str(soup), tags=[], strip=True)
            news_phrase_dict[i] = {"news": temp_str, "phrase": phrases}

    tweet_news_map = {}
    for i in tweet_phrase_dict:
        maxi = -1
        max_len = 0
        tweet_phrases = tweet_phrase_dict[i]["phrase"]
        for j in news_phrase_dict:
            temp_var = len(tweet_phrases.intersection(news_phrase_dict[j]["phrase"]))
            if temp_var >= 2 and temp_var > max_len:
                # todo tune this min. frequency limit
                max_len = temp_var
                maxi = j
        if maxi == -1:
            continue
        tweet_news_map[i] = maxi

    print("Final number of tweets: ", len(tweet_news_map))
    pickle.dump(tweet_news_map, open(data_path + "tweet_news_map.pkl", "wb"))
    pickle.dump(news_phrase_dict, open(data_path + "news_phrase_dict.pkl", "wb"))
    pickle.dump(tweet_phrase_dict, open(data_path + "tweet_phrase_dict.pkl", "wb"))
