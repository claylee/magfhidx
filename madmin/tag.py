import jieba
import json
import codecs

class tag(object):
    """docstring for tag."""
    stopwords = {}

    def __init__(self):
        self.stopwords = self.loadStopwords()
        pass

    def loadStopwords(self):
        sw = {}
        stopfiles = ['chineseStopWords.txt','chineseStopWords_1893.txt','englishStopWords.txt',
        'englishstopword_600.txt','englishStopWords_mysql.txt','stop-words_japanese_1_ja.txt',
        'stop-words_russian_1_ru.txt','stopWords_ext.txt','myextentions.txt']
        for filename in stopfiles:
            f = codecs.open(filename, 'r',encoding='utf-8')
            for w in f:
                #print(w, w.find('\n'),w.find(' '))
                w = w.replace('\r\n','')
                if not w in sw:
                    sw[w] = w
        return sw

    def gettags(self, word, filter = False):
        wordcuts = jieba.cut_for_search(word)
        tags = []

        for c in wordcuts:
            if not c.lower() in self.stopwords:
                tags.append(c)
        return tags


class AllCuts:
    allcuts = []

    @classmethod
    def savegroup(cls):
        file = codecs.open('allcuts.json', 'w',encoding='utf-8')
        file.write(json.dumps(group,ensure_ascii=False))

    @classmethod
    def loadgroup(cls):
        file = codecs.open('allcuts.json', 'r',encoding='utf-8')
        #file.write(json.dumps(group,ensure_ascii=False))
        return json.loads(file.read())

    @classmethod
    def loadStopwords(cls):
        sw = []
        stopfiles = ['madmin/chineseStopWords.txt','madmin/englishStopWords.txt']
        for filename in stopfiles:
            f = codecs.open(filename, 'r',encoding='utf-8')
            for w in f:
                #print(w, w.find('\n'),w.find(' '))
                sw.append(w.strip().replace('\r\n',''))
        return sw

    @classmethod
    def filtercuts(cls):
        newCuts = []
        c = cls.loadgroup()
        stopw = cls.loadStopwords()
        print(len(stopw))
        file = codecs.open('allcutsfilter.json', 'w',encoding='utf-8')
        i = 0
        for w in c:
            i += 1
            if i % 3000 == 0:
                print(i)
            if w in stopw:
                #print(" - ",w)
                continue
            if w in newCuts:
                continue
            newCuts.append(w)
        file.write(json.dumps(newCuts,ensure_ascii=False))
