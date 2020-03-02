import pandas as pd

def write_to_file(file_path, entities):
    f = open(file_path, "w", encoding="utf-8")
    for t in entities:
        f.write(t)
        f.write("\n")
    f.close()



if __name__ == '__main__':
    without_news_tgt_path = 'C:/Users/xw/Downloads/without_news_innews.txt'
    with_news_tgt_path = 'C:/Users/xw/Downloads/with_news_innews.txt'
    tgt_path = 'C:/Users/xw/PycharmProjects/hashtagGen/data/Twitter/innews/test_tag.txt'
    tweet_path = './data/Twitter/innews/test_post.txt'
    news_path = './data/Twitter/innews/test_conv.txt'
    wo_news_target_lines = open(without_news_tgt_path, encoding='utf-8').readlines()
    with_news_target_lines = open(with_news_tgt_path, encoding='utf-8').readlines()
    tgt_lines = open(tgt_path, encoding='utf-8').readlines()
    tweets = open(tweet_path, encoding='utf-8').readlines()
    news = open(news_path, encoding='utf-8').readlines()

    # the number of examples should be the same
    assert len(tgt_lines) == len(with_news_target_lines)

    with_news_correct_index = []
    not_with_news_correct_index = []
    news_help_tweets = [["processed_tweet", "news", "hashtags", "with_news_predictions", "without_news_predictions"]]
    news_not_help_tweets = [["processed_tweet", "news", "hashtags", "with_news_predictions", "without_news_predictions"]]

    for i in range(len(tgt_lines)):
        w_pred = with_news_target_lines[i]
        wo_pred = wo_news_target_lines[i]
        tgt =  tgt_lines[i]
        wo_preds = wo_pred.split(';')
        w_preds = w_pred.split(';')
        tgts = tgt.split(';')
        wo_preds = [t.strip() for t in wo_preds if t.strip()]
        w_preds = [t.strip() for t in w_preds if t.strip()]
        tgts = [t.strip() for t in tgts if t.strip()]
        top_wo_preds = wo_preds[:5]
        top_w_preds = w_preds[:5]
        wo_exist = False
        w_exist = False
        for tag in tgts:
            if tag in top_wo_preds:
                wo_exist = True
                break
        for tag in tgts:
            if tag in top_w_preds:
                w_exist = True
                break
        if wo_exist and not w_exist:
            news_not_help_tweets.append([tweets[i], news[i], tgt_lines[i], ';'.join(top_w_preds), ';'.join(top_wo_preds)])
        elif w_exist and not wo_exist:
            news_help_tweets.append([tweets[i], news[i], tgt_lines[i], ';'.join(top_w_preds), ';'.join(top_wo_preds)])
    df_news_help = pd.DataFrame(news_help_tweets[1:], columns=news_help_tweets[0])
    df_news_not_help = pd.DataFrame(news_not_help_tweets[1:], columns=news_not_help_tweets[0])

    df_news_help.to_csv('news_help.csv')
    df_news_not_help.to_csv('news_not_help.csv')


