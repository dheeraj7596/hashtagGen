import pickle
import numpy as np
# from sklearn.model_selection import train_test_split
import pandas as pd
from process_tweets import tokenizer

def write_to_file(file_path, entities):
    f = open(file_path, "w", encoding="utf-8")
    for t in entities:
        f.write(t)
        f.write("\n")
    f.close()

def creat_input_from_matching(df, data_path):
    drop_index = []
    for ind in df.index:
        if len(df['hashtags'][ind]) == 0 or len(df['processed tweets'][ind]) == 0 or len(df['news'][ind]) == 0:
            drop_index.append(ind)
    df = df.drop(df.index[drop_index])
    train = df.sample(frac=0.8, random_state=200)  # random state is a seed value
    valid = df.drop(train.index)
    test = valid.sample(frac=0.5, random_state=200)
    valid = valid.drop(test.index)
    # index = np.arange(len(all_tweets))
    # np.random.shuffle(index)
    # all_tweets = np.array(all_tweets)
    # all_tags = np.array(all_tags)
    # all_news = np.array(all_news)
    # train_index = index[:int(len(all_tweets)*0.8)]
    # valid_index = index[int(len(all_tweets)*0.8):int(len(all_tweets)*0.9)]
    # test_index = index[int(len(all_tweets)*0.9):]
    # tweets_train, tweets_val, tweets_test = all_tweets[train_index], all_tweets[valid_index], all_tweets[test_index]
    # news_train, news_val, news_test = all_news[train_index], all_news[valid_index], all_news[test_index]
    # tags_train, tags_val, tags_test = all_tags[train_index], all_tags[valid_index], all_tags[test_index]

    # tweets_train, tweets_test, news_train, news_test, tags_train, tags_test = train_test_split(all_tweets, all_news,
    #                                                                                            all_tags, test_size=0.1,
    #                                                                                            random_state=42)
    # tweets_train, tweets_val, news_train, news_val, tags_train, tags_val = train_test_split(tweets_train, news_train,
    #                                                                                         tags_train, test_size=0.1,
    #                                                                                         random_state=42)
    test.to_pickle(data_path+"test.pkl")
    write_to_file(data_path + "train_post.txt", train['processed tweets'].tolist())
    write_to_file(data_path + "train_conv.txt", train['news'].tolist())
    write_to_file(data_path + "train_tag.txt", train['hashtags'].tolist())

    write_to_file(data_path + "valid_post.txt", valid['processed tweets'].tolist())
    write_to_file(data_path + "valid_conv.txt", valid['news'].tolist())
    write_to_file(data_path + "valid_tag.txt", valid['hashtags'].tolist())

    write_to_file(data_path + "test_post.txt", test['processed tweets'].tolist())
    write_to_file(data_path + "test_conv.txt", test['news'].tolist())
    write_to_file(data_path + "test_tag.txt", test['hashtags'].tolist())



if __name__ == "__main__":
    path = "./data/Twitter/"
    df_news_match = pickle.load(open(path + "news_match.pkl", "rb"))
    creat_input_from_matching(df_news_match, path)






