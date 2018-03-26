# -*- encode: utf-8 -*-

with open('stopwords_raw.txt', 'r', encoding='utf-8') as f:
    stopwords = []
    for line in f:
        line = f.readline().strip()
        print(line)
        stopwords.append(line)

    if stopwords:
        stopwords = set(stopwords)
        with open('stopwords.txt', 'w', encoding='utf-8') as fileStopwords:
            for word in stopwords:
                fileStopwords.write(word + "\n")

print("Done.")
