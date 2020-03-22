from nltk.corpus import stopwords


def get_lines(path):
    f_in_conv = open(path, "r")
    lines_conv = f_in_conv.readlines()
    f_in_conv.close()
    return lines_conv


def func(base_path, type):
    post_path = base_path + type + "_post.txt"
    conv_path = base_path + type + "_conv.txt"
    tag_path = base_path + type + "_tag.txt"

    out_post_path = "./" + type + "_post_clean.txt"
    out_conv_path = "./" + type + "_conv_clean.txt"
    out_tag_path = "./" + type + "_tag_clean.txt"

    lines_post = get_lines(post_path)
    lines_conv = get_lines(conv_path)
    lines_tag = get_lines(tag_path)

    assert len(lines_conv) == len(lines_post) == len(lines_tag)

    f_post = open(out_post_path, "w")
    f_conv = open(out_conv_path, "w")
    f_tag = open(out_tag_path, "w")

    stop_words = set(stopwords.words('english'))
    stop_words.add('would')

    remove_inds = []
    for i, line in enumerate(lines_conv):
        word_list = line.strip().split()
        filtered_words = [word for word in word_list if word not in stop_words]
        clean_line = " ".join(filtered_words)
        if len(clean_line) > 0:
            f_conv.write(clean_line)
            f_conv.write("\n")
        else:
            remove_inds.append(i)

    remove_inds.reverse()

    for i in remove_inds:
        del lines_post[i]
        del lines_tag[i]

    for l in lines_post:
        f_post.write(l)

    for l in lines_tag:
        f_tag.write(l)

    f_post.close()
    f_conv.close()
    f_tag.close()
    assert len(lines_conv) - len(remove_inds) == len(lines_post) == len(lines_tag)


if __name__ == "__main__":
    base_path = "/data1/xiuwen/twitter/tweetnews/processeddata/"

    func(base_path, "train")
    func(base_path, "valid")
    func(base_path, "test")
