import pickle
import numpy as np
#from sklearn.model_selection import train_test_split



def write_to_file(file_path, entities):
    f = open(file_path, "w", encoding="utf-8")
    for t in entities:
        f.write(t)
        f.write("\n")
    f.close()


def creat_input_from_matching(df, data_path):
    all_tweets = []
    all_news = []
    all_tags = []
    for ind in df.index:
        if len(df['hashtags'][ind]) == 0 or len(df['processed_tweet'][ind]) == 0 or len(df['news'][ind]) == 0:
            continue
        all_tweets.append(df["processed_tweet"][ind])
        all_tags.append(df['hashtags'][ind])
        clean_news_total = ' '.join(df['news'][ind].split(';'))
        all_news.append(clean_news_total)
    index = np.arange(len(all_tweets))
    np.random.shuffle(index)
    all_tweets = np.array(all_tweets)
    all_tags = np.array(all_tags)
    all_news = np.array(all_news)
    train_index = index[:int(len(all_tweets)*0.8)]
    valid_index = index[int(len(all_tweets)*0.8):int(len(all_tweets)*0.9)]
    test_index = index[int(len(all_tweets)*0.9):]
    tweets_train, tweets_val, tweets_test = all_tweets[train_index], all_tweets[valid_index], all_tweets[test_index]
    news_train, news_val, news_test = all_news[train_index], all_news[valid_index], all_news[test_index]
    tags_train, tags_val, tags_test = all_tags[train_index], all_tags[valid_index], all_tags[test_index]

    # tweets_train, tweets_test, news_train, news_test, tags_train, tags_test = train_test_split(all_tweets, all_news,
    #                                                                                            all_tags, test_size=0.1,
    #                                                                                            random_state=42)
    # tweets_train, tweets_val, news_train, news_val, tags_train, tags_val = train_test_split(tweets_train, news_train,
    #                                                                                         tags_train, test_size=0.1,
    #                                                                                         random_state=42)

    write_to_file(data_path + "train_post.txt", tweets_train)
    write_to_file(data_path + "train_conv.txt", news_train)
    write_to_file(data_path + "train_tag.txt", tags_train)

    write_to_file(data_path + "valid_post.txt", tweets_val)
    write_to_file(data_path + "valid_conv.txt", news_val)
    write_to_file(data_path + "valid_tag.txt", tags_val)

    write_to_file(data_path + "test_post.txt", tweets_test)
    write_to_file(data_path + "test_conv.txt", news_test)
    write_to_file(data_path + "test_tag.txt", tags_test)



if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset

    ht_not_in_news = pickle.load(open(data_path + "ht_not_in_news.pkl", "rb"))
    ht_in_news = pickle.load(open(data_path + "ht_in_news.pkl", "rb"))


    creat_input_from_matching(ht_in_news, data_path+"innews/")
    creat_input_from_matching(ht_not_in_news, data_path+"notinnews/")





