# coding=utf-8
"""敏感词处理"""
import os


class SensitiveWords(object):
    __slots__ = ['_words']

    def __init__(self):
        self._words = set()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'dicts', 'words.txt'), 'r', encoding='utf-8') as f:
            for row in f:
                self._words.add(row.strip())

    def has(self, content):
        """判断是否包含敏感词
        :param content:
        :return: boolean
        """
        for word in self._words:
            if content.find(word) > -1:
                return True

        return False

    def filter(self, content, replace_char='*'):
        """过滤敏感词
        :param content: 内容
        :param replace_char: 替换的字符
        :return: string 过滤后的内容
        """
        if content:
            for word in self.parse(content):
                content = content.replace(word, replace_char * len(word))

        return content

    def parse(self, content):
        words = set()
        if content:
            for word in self._words:
                if content.find(word) > -1:
                    words.add(word)

        return words


if __name__ == '__main__':
    sensitive_words = []
    sw = SensitiveWords()
    words = ['中国', '共产党', '中华人民共和国', '六合彩', '工信处女职工', '计算机开发', 'sex', 'porn']
    for word in words:
        if sw.has(word):
            sensitive_words.append(word)

    if len(sensitive_words):
        print(sensitive_words)
    else:
        print('OK')

    content = """
中国zf严控六合彩彩票
    """
    print(sw.parse(content))
    print(content.strip() + " => " + sw.filter(content).strip())
    sw = SensitiveWords()
    print(content.strip() + " => " + sw.filter(content).strip())
