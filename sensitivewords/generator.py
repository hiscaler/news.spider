# coding=utf-8
"""生成敏感词
"""
import os

if __name__ == '__main__':
    dict_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dicts')
    words = set()
    files = os.listdir(dict_dir)
    for file in files:
        file_path = os.path.join(dict_dir, file)
        if file == 'words.txt' or os.path.isdir(file_path):
            continue

        with open(file_path) as f:
            for word in f:
                word = word.strip()
                if word:
                    words.add(word)

    if words:
        with open(os.path.join(dict_dir, 'words.txt'), 'w+', encoding='utf-8') as f:
            for word in words:
                f.write(word + '\n')

            print("Done")
    else:
        print("Nothing")
