import io
import json
from pprint import pprint

def findList(data, id):
        for myList in data["lists"]:
            if  myList["id"] == id:
                return myList["name"]

def setFinishedQuality(myVar, myDate):
    #Start at 2016-09-26
    myCuttingTime = 160926
    if int(myDate) < myCuttingTime:
        
        myVar = myVar.replace("null,","'Sim',")
        myVar = myVar.replace(',null',',7')
    return myVar



def findCustomFields(data):

    isFinished = "8uBtoloi-5Oh5zM"
    qualitySet = "8uBtoloi-PO7G52"
    strOutcome = ""

    for myCustomFields in data:
        mystr =  myCustomFields["value"]
        if mystr.find(isFinished) > 0:
            if int(mystr[mystr.index(isFinished) + len(isFinished) + 2 : mystr.index(isFinished) + len(isFinished) +3])==1:
                strOutcome =  strOutcome +  "'Sim',"
            else:
                strOutcome =  strOutcome +  "'Nao',"
        else:
            strOutcome =  strOutcome +  'null,'
        if mystr.find(qualitySet) > 0:
            strOutcome =  strOutcome + str(int(mystr[mystr.index(qualitySet) + len(qualitySet) + 2 : mystr.index(qualitySet) + len(qualitySet) +3]) * 2)
        else:
            strOutcome =  strOutcome +  'null'

    if strOutcome =='':
        strOutcome = 'null,null'
    return strOutcome


def listMember(data, id):
    membersInitials =""
    for myMember in data["members"]:
        if id == myMember["id"]:
            membersInitials = myMember["initials"]
    return membersInitials


with open('gaq2016-prod.json') as data_file:
    data = json.load(data_file)


myString ="Recurso,Sprint,Ano,Mes,Card,Prazo,Qualidade,Descricao,url,Count \n"
myDataSetOutput = "function fn1 () { \n var data = [ \n"
FinishedQuality = ""
mySprint = ""

for myTrelloBoard in data["cards"]:
    if findList(data, myTrelloBoard["idList"])[0:3] != 'S16':
        continue
    if len(myTrelloBoard["idMembers"]) > 0:
        for oneMember in xrange(len(myTrelloBoard["idMembers"])):
            if (myTrelloBoard["name"][0:3] == '000') or (myTrelloBoard["closed"] == True):
                continue

            mySprint = findList(data, myTrelloBoard["idList"])[1:7]
            FinishedQuality = setFinishedQuality(findCustomFields(myTrelloBoard["pluginData"]), mySprint)
            myString = myString + listMember(data,myTrelloBoard["idMembers"][oneMember]) + ',' + mySprint + ',20' + findList(data, myTrelloBoard["idList"])[1:3] + ',' + findList(data, myTrelloBoard["idList"])[3:5] + ',' +  myTrelloBoard["id"] + ',' +  FinishedQuality + ',"' +  myTrelloBoard["name"] + '",' +   myTrelloBoard["shortUrl"] + ',1 \n'
            myDataSetOutput = myDataSetOutput + "['" + listMember(data,myTrelloBoard["idMembers"][oneMember]) + "','" + mySprint +  "','20"  + findList(data, myTrelloBoard["idList"])[1:3] + "','" + findList(data, myTrelloBoard["idList"])[3:5] + "'," + FinishedQuality.replace(";","',") + ",1], \n"
    else:
        if (myTrelloBoard["name"][0:3] == '000') or (myTrelloBoard["closed"] == True):
                continue

        mySprint = findList(data, myTrelloBoard["idList"])[1:7]
        FinishedQuality = setFinishedQuality(findCustomFields(myTrelloBoard["pluginData"]), mySprint)
        myString = myString + 'NULL,' + mySprint + ',20' + findList(data, myTrelloBoard["idList"])[1:3] + ',' + findList(data, myTrelloBoard["idList"])[3:5] + ',' +  myTrelloBoard["id"]  + ',' +  FinishedQuality + ',"' +  myTrelloBoard["name"] + '",' +   myTrelloBoard["shortUrl"] + ',1 \n'
        myDataSetOutput = myDataSetOutput + "['NULL','" + mySprint +  "','20"  + findList(data, myTrelloBoard["idList"])[1:3] + "','" + findList(data, myTrelloBoard["idList"])[3:5] + "'," + FinishedQuality.replace(";","',") + ",1], \n"

#print myString
myString = myString.replace("'Sim'","Sim") 
myString = myString.replace("'Nao'","Nao")

with io.open('dump-trello.csv','w',encoding='utf8') as f:
    f.write(myString)

myDataSetOutput = myDataSetOutput[0:len(myDataSetOutput)-3] + ' ];\n  return data;\n }'

with io.open('data.js','w',encoding='utf8') as f:
    f.write(myDataSetOutput)

