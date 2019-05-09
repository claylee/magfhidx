
def loadjson(path, filename):
    jsonpath = os.path.join(path,filename)
    file = codecs.open(jsonpath, 'r',encoding='utf-8')
    return json.loads(file.read())
