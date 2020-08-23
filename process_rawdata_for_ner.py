import pandas as pd
import re
from nltk.corpus import stopwords
import pickle
import ekphrasis
import numpy as np
from ekphrasis.classes.segmenter import Segmenter
from process_tweets import tokenizer

stop_words = set()
stop_words.add("rt")
stop_words.add("RT")
seg_eng = Segmenter(corpus="english")


# get only tweets with notinline hashtags, for inline hashtags it split into words, for not inline, it deleted
def get_inline_notinline_htags(list_words):
    end_wt_punc = re.compile(r'#\w+[^a-zA-Z\d\s]')
    all_letters = re.compile(r'\w+$')
    all_letters_wt_punc = re.compile(r'\w+$|\w+[:,.]$')
    end = -1
    inline_ht, not_inline_ht = [], []
    for i in range(len(list_words)):
        if i <= end or not list_words[i].startswith("#"):
            continue
        end = i
        previous_word = None
        next_word = None
        if i>0:
            previous_word = list_words[i-1]
        for j in range(i+1, len(list_words)):
            if list_words[j].startswith("#"):
                end = j
            else:
                next_word = list_words[j]
                break
        this_word = list_words[end]
        idx_range = [idx for idx in range(i, end+1)]
        if previous_word is not None and next_word is not None:
            if re.match(all_letters, previous_word) is not None or (re.match(end_wt_punc, this_word) is None and re.match(all_letters_wt_punc, next_word) is not None):
                inline_ht.extend(idx_range)
            else:
                not_inline_ht.extend(idx_range)
        elif previous_word is None and next_word is not None:
            if re.match(end_wt_punc, this_word) is not None or re.match(all_letters_wt_punc, next_word) is None:
                not_inline_ht.extend(idx_range)
            else:
                inline_ht.extend(idx_range)
        elif previous_word is not None:
            if re.match(all_letters, previous_word) is not None:
                inline_ht.extend(idx_range)
            else:
                not_inline_ht.extend(idx_range)
        else:
            not_inline_ht.extend(idx_range)
    if len(not_inline_ht) == 0:
        return None
    else:
        hashtags = []
        for i in range(len(list_words)):
            if i in not_inline_ht:
                hashes = seg_eng.segment(list_words[i].lstrip('#').lower())
                hashtags.append(hashes)
                list_words[i] = ""
            elif i in inline_ht:
                list_words[i] = seg_eng.segment(list_words[i].lstrip('#'))
        tweet_for_ner = " ".join([i for i in list_words if i is not ""])
        return tweet_for_ner, hashtags


def handle_tweets(df_tweets):
    dataset = [[ "text", "ner_tweets", "clean_tweets", "hashtags", "created_at"]]
    for index, row in df_tweets.iterrows():
        # pattern = r'#\w+|#\w+$'
        # remove = re.compile(pattern)
        # removed_t = remove.sub(r'', t)
        # matches = re.findall(pattern, t)
        tweet = row['text']
        tweet = re.sub(r'\s+', ' ', tweet)
        list_tweet = tweet.split(" ")
        temp = get_inline_notinline_htags(list_tweet)
        if temp is not None:
            tweet_for_ner, htags = temp
            dataset.append([ tweet, tweet_for_ner, tokenizer(tweet_for_ner), ";".join(htags), row['created_at']])

    #   f.write(tweet)
    #  f.write("\n")
    #f.close()
    return dataset

if __name__ == '__main__':
    data_path = "C:/Users/xw/Documents/Twitter-analysis/data/"
    df_tweets = pd.read_csv(data_path + "tweets.csv", encoding="utf-8", error_bad_lines=False)
    print(len(df_tweets))
    dataset = handle_tweets(df_tweets)
    df_processed_tweets = pd.DataFrame(dataset[1:], columns=dataset[0])
    df_processed_tweets['id'] = df_processed_tweets.index
    df_processed_tweets.to_pickle(data_path + "processedtweets.pkl")
    print(len(dataset))


    # df_news = pd.read_csv(data_path + "news.csv", encoding="utf-8", error_bad_lines=False)
    # df_news = df_news.dropna(subset=['index'])
    # df_news = df_news.reset_index(drop=True)
    # tweets_dataset = handle_tweets(df_tweets)

