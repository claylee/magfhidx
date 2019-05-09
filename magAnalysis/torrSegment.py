import sqlite3
import jieba

def splitTag(sentence):
    cuts = jieba.cut(sentence)
    cutsList = list(cuts)

    if " " in cutsList:
        cutsList.remove(" ")
    return cutsList

def readMagDb():
    conn = sqlite3.connect("../data/infohash.db")
    #
    bcnt = 0
    try:
        cursor = conn.execute("SELECT * FROM SearchHash")
        keywords = dict()
        for l in cursor.fetchall():
            print(l[0],l[4],l[5])
            cutsList = splitTag(l.name)
            for c in cutsList:
                if c in keywords:
                    print(c,keywords[c])
                    keywords[c] += 1
                else:
                    keywords[c] = 1
                    print("new :",c)

    except Exception as Exp:
        print(Exp)
        pass
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    readMagDb()
