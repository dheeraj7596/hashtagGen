def repeat(data):
    new_src = []
    new_conv = []
    new_tag = []
    new_score  = []
    for i in data:
        tag_list = i[2].split(";")
        for j in range(len(tag_list)):
            new_src.append(i[0])
            new_conv.append(i[1])
            if len(i) == 4:
               new_score.append(i[-1])
        new_tag += tag_list
    assert len(new_conv) == len(new_src) == len(new_tag)
    print("size after repeat: " + str(len(new_src)))
    return new_src, new_conv, new_tag, new_score


def write_to_file(file_path, entities):
    f = open(file_path, "w", encoding='utf-8')
    for t in entities:
        f.write(t)
        f.write("\n")
    f.close()


def read_file(file_path):
    f = open(file_path, "r", encoding='utf-8')
    lines = f.readlines()
    f.close()
    return [l.rstrip("\n") for l in lines]


if __name__ == '__main__':
    key = "train"
    base_path = "/data1/xiuwen/twitter/match-using-entity/modified-bm25/"
    src_path = base_path + key + "_post.txt"
    conv_path = base_path + key + "_conv.txt"
    score_path = base_path + key + "_score.txt"
    tag_path = base_path + key + "_tag.txt"
    srcs = read_file(src_path)
    convs = read_file(conv_path)
    scores = read_file(score_path)
    tags = read_file(tag_path)
    new_data = repeat(zip(srcs, convs, tags, scores))
    # new_data = repeat(zip(srcs, convs, tags))
    write_to_file(base_path + key + "_repeat_post.txt", new_data[0])
    write_to_file(base_path + key + "_repeat_conv.txt", new_data[1])
    write_to_file(base_path + key + "_repeat_tag.txt", new_data[2])
    # write_to_file(base_path + key + "_repeat_score.txt", new_data[3])

