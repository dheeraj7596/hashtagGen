import pickle
from summarizer import Summarizer
import random


def get_content(news, inds, thresh=5):
    temp = news.ix[inds]
    arr = list(temp.news)
    random.shuffle(arr)
    return " ".join(arr[:thresh])


if __name__ == "__main__":
    data_path = "/data4/dheeraj/hashtag/"
    news_match = pickle.load(open(data_path + "news_match_final.pkl", "rb"))
    news = pickle.load(open(data_path + "df_news_lowercase.pkl", "rb"))
    model = Summarizer()

    summarized_contents = []

    for i, row in news_match.iterrows():
        print(i)
        content = get_content(news, row["news_index"], thresh=3)
        summary = model(content, ratio=0.1)
        summarized_contents.append(summary)

    news_match["summarized content"] = summarized_contents
    pickle.dump(news_match, open(data_path + "news_match_summary.pkl", "wb"))
    pass
