if __name__ == "__main__":
    base_path = "/data4/dheeraj/hashtag/all/Twitter/"

    f_tweets = open(base_path + "train_post.txt", "r")
    f_tags = open(base_path + "train_tag.txt", "r")
    tweets = f_tweets.readlines()
    tags = f_tags.readlines()
    f_tags.close()
    f_tweets.close()
    tweets = tweets[:100]
    tags = tags[:100]

    final_tweets = []
    final_tags = []

    for i, tag in enumerate(tags):
        all_tags = tag.split(';')
        for t in all_tags:
            final_tweets.append(tweets[i])
            final_tags.append(t.strip())

    for i, tweet in enumerate(final_tweets):
        tag = final_tags[i]
        with open(base_path + "data/" + str(i) + ".txt", "w") as f:
            f.write(tweet.strip())
            f.write("\n")
            f.write(tag.strip())
