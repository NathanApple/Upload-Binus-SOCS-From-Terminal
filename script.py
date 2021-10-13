# https://github.com/NathanApple
# Default file extension for Cpp : C++11 and py : Python3
# Please customize the config.ini file as much as you can.

import requests
import sys
from bs4 import BeautifulSoup
from configparser import ConfigParser
from os import path

language = {}
phpsessid = ""
domjudge_cid = ""

def main():
    getConfig()
    # print(language, phpsessid, domjudge_cid)
    lenArgv = len(sys.argv)
    # print(lenArgv)
    if lenArgv == 1:
        pass
    elif lenArgv == 2:
        pass
    elif lenArgv == 3:
        # Argument : [filename] [cid]
        # cid could have reset as argument which will show all avaible cid
        _,filename,cid = sys.argv
        if (cid == "reset" or cid == "idk"):
            pass
        
        prob, lang = getProblemAndLanguage(filename)
        cookies={"domjudge_cid": cid,"PHPSESSID": phpsessid}

        res = requests.get("https://socs1.binus.ac.id/quiz/team/index.php", cookies=cookies)
        probList = getProblemList(res.text)
        # sendRequest()
        probId = findIdByProblem(probList, prob)

        print(sendFileToServer(filename, lang, probId, cid).text[-100:])
        # Too Lazy to do some verification. :)
        print("Success")

def getConfig():
    global language, phpsessid, domjudge_cid
    if not path.isfile('config.ini'):
        createConfig()
    
    config = ConfigParser()
    config.sections()
    config.read('config.ini')
    language = {x[0]:x[1] for x in config.items('LANGUAGE')}
    phpsessid = config['CREDENTIAL']['PHPSESSID']
    domjudge_cid = config['CREDENTIAL']['domjudge_cid']

def createConfig():
    config = ConfigParser()
    config['LANGUAGE'] = {'c': 'c',
                        'cpp': 'cpp11',
                        'py': 'py3'}

    config['CREDENTIAL'] = {}
    config['CREDENTIAL']['PHPSESSID'] = ''
    config['CREDENTIAL']['domjudge_cid'] = ''
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def findIdByProblem(probDict, problem):
    return probDict[problem]

def getProblemList(text):
    soup = BeautifulSoup(text, "html.parser")
    # probId = soup.find("select", {"id": "probid"})
    probDict = {x.text.lower():x.get("value") for x in soup.find("select", {"id": "probid"}).findChildren()}
    return probDict

def getCid(text):
    soup = BeautifulSoup(text, "html.parser")
    cid = {x.get("value"):x.text for x in soup.find("select", {"id": "cid"}).findChildren()}
    return cid

def getProblemAndLanguage(text):
    filename = text.split(".")
    if (len(filename) == 2):
        prob, lang = filename
    elif (len(filename) == 3):
        _,prob, lang = filename
        prob = prob[1:]
    newLang = language[lang]
    return prob,newLang
    
def sendFileToServer(filename, language, probId, cid):
    print(filename, language, probId, cid)
    url = "https://socs1.binus.ac.id/quiz/team/upload.php"
    cookies={"domjudge_cid": cid,"PHPSESSID": phpsessid}
    files = {'code[]': open(filename,'rb')}
    values = {'probid': probId, 
            'langid': language, 
            'submit': 'submit'}
    response = requests.post(url, files=files, data=values, cookies=cookies)
    # print(r.text)
    return response

if __name__ == "__main__":
    main()