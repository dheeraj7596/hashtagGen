import pickle
from sklearn.model_selection import train_test_split
from create_input import write_to_file


def creat_input_from_matching(df, data_path):
    all_tweets = []
    all_news = []
    all_tags = []
    for id in df:
        all_tweets.append(df[id]["processed_tweet"])
        all_tags.append(df[id]["hashtags"])
        clean_news_total = ' '.join(df[id]["news"].split(";"))
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



if __name__ == "__main__":
    base_path = "./data/"
    dataset = "Twitter/"
    data_path = base_path + dataset

    ht_not_in_news = pickle.load(open(data_path + "ht_not_in_news.pkl", "rb"))
    ht_in_news = pickle.load(open(data_path + "ht_in_news.pkl", "rb"))


    creat_input_from_matching(ht_in_news, data_path+"innews/")
    creat_input_from_matching(ht_not_in_news, data_path+"notinnews/")





