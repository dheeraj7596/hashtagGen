from nltk.corpus import stopwords
import sys

if __name__ == "__main__":
    filepath = sys.argv[1]
    outpath = sys.argv[2]

    f = open(filepath, "r")
    lines = f.readlines()
    f.close()

    f = open(outpath, "w")

    stop_words = set(stopwords.words('english'))
    stop_words.add('would')

    for line in lines:
        word_list = line.strip().split()
        filtered_words = [word for word in word_list if word not in stop_words]
        clean_line = " ".join(filtered_words)
        if len(clean_line) > 0:
            f.write(clean_line)
        f.write("\n")

    f.close()
