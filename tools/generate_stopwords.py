# -*- encode: utf-8 -*-

with open('stopwords_raw.txt', 'r', encoding='utf-8') as f:
    stopwords = set()
    for line in f:
        line = f.readline().strip()
        stopwords.add(line)

    if stopwords:
        stopwords = set(stopwords)
        with open('stopwords.txt', 'w', encoding='utf-8') as fileStopwords:
            for word in stopwords:
                fileStopwords.write(word + "\n")

if __name__ == '__main__':
    input_words = {'你们', '我们', '中国', '就要'}
    print("测试的数据: ", input_words)
    with open('stopwords.txt', 'r', encoding='utf-8') as f:
        stopwords = set(map(lambda s: s.strip(), f.readlines()))
        if stopwords:
            input_words = set(input_words.difference(stopwords))

    print("修正后的数据: ", input_words)
