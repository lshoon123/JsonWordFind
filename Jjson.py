import json
import pymongo
import string
import re


#setting mongoDB
with open('ea-thesaurus-lower.json') as normsf:
    norms = json.load(normsf)

client = pymongo.MongoClient()

db = client['JSONWORD']
c = db['word']

def openfile(Upload_Folder, filename):
    #setting file read
    fopen = open(Upload_Folder + '/' + filename, "r", encoding='utf8', errors='ignore')
    #fopen = open("trump.txt", "r",encoding='utf8')
    data = fopen.read()
    #change lowercase
    data = data.lower()
    #delete every special character
    data = data.replace('\n', ' ')
    data = re.sub("[^0-9a-zA-Z\\s]",'', data)
    #string to list
    data = data.split(" ")
    #remove blank // select all word
    for x in data:
        if x == '':
            data.remove(x)
    for x in data:
        if x == '':
            data.remove(x)
    #print(data)
    dummydata = list(set(data))
    #print(dummydata)
    nodata = []
    sortedData = {}
    worddata = {}
    wordlist = []
    for x in dummydata:
        wordcount = data.count(x)
        sortedData[x] = wordcount
    for x in dummydata:
        if x in norms:
            #print(x+'(' + str(sortedData[x]) + ')' + str(norms[x][:3]))
            worddata = {'word': x, 'number': sortedData[x], 'Json': norms[x][:3]}
            wordlist.append(worddata)
            #print(worddata)
        else:
            nodata.append(x)
    for x in nodata:
        worddata = {'word': x, 'number': sortedData[x], 'Json': "was not found in the associations list"}
        wordlist.append(worddata)
       #print(x + '(' + str(sortedData[x]) + ')' + "was not found in the associations list")
    #datab = data.translate(None, ".#/?:$}")
    #print(datab)
    return wordlist
