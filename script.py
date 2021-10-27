# Became a sigma by doing everything at terminal
# Please star project on github to get notified on new update
# https://github.com/NathanApple/Upload-Binus-SOCS-From-Terminal
# Usage : python script.py [filename] [cid]

# Default file extension for Cpp : Cpp11 and py : Python3
# Config file : config.ini

# Please customize the code as your heart content.
# TODO : Global config path [ Priority ]
# TODO : Access program from anywhere ( using bin as env variable )
#       sys.argv will need to be changed when that happen
# TODO : Simplify repetitive code. I have no idea how the program should flow
# TODO : Accept input from all path

import requests
import sys
from bs4 import BeautifulSoup
from configparser import ConfigParser
from os import path
from time import sleep
import getpass
# import itertools
# import threading

language = {}
phpsessid = ""
domjudge_cid = ""
CONSTANT_CONFIG_PATH = "socs_config.ini"
done = False
folderPath = ""

def main():
    get_config()
    # check_file_path()
    # exit()
    
    # wait_result()
    # exit()
    # print(language, phpsessid, domjudge_cid)
    lenArgv = len(sys.argv)
    # print(lenArgv)
    if lenArgv == 1:
        pass
    elif lenArgv == 2:
        _,filepath = sys.argv
        if (filepath == "?"):
            # TODO next
            pass
        folderPath, filename = check_file_path(filepath)
        prob, lang = get_problem_and_language(filename)
        cookies={"domjudge_cid": domjudge_cid,"PHPSESSID": phpsessid}

        res = requests.get("https://socs1.binus.ac.id/quiz/team/index.php", cookies=cookies)
        probList = get_problem_list(res.text)
        # sendRequest()
        probId = find_id_by_problem(probList, prob)

        print(send_file_to_server((folderPath+"\\"+filename), lang, probId, domjudge_cid))
        # Too Lazy to do some verification. :)
        # print("Success")
        wait_result()
        
    elif lenArgv == 3:
        # Argument : [filename] [cid]
        # cid could have reset as argument which will show all avaible cid
        _,filepath,cid = sys.argv
        if (cid == "reset" or cid == "idk" or cid == "?"):
            cid = input_cid()
        
        folderPath, filename = check_file_path(filepath)
        prob, lang = get_problem_and_language(filename)
        cookies={"domjudge_cid": cid,"PHPSESSID": phpsessid}

        res = requests.get("https://socs1.binus.ac.id/quiz/team/index.php", cookies=cookies)
        probList = get_problem_list(res.text)
        # sendRequest()
        probId = find_id_by_problem(probList, prob)

        print(send_file_to_server((folderPath+"\\"+filename), lang, probId, domjudge_cid))

        # Too Lazy to do some verification. :)
        # print("Success")
        wait_result()
        

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# def animate():
#     for c in itertools.cycle(['|', '/', '-', '\\']):
#         if done:
#             break
#         sys.stdout.write('\rloading ' + c)
#         sys.stdout.flush()
#         sleep(0.1)
#     sys.stdout.write('\rDone!     ')

def get_config():
    global language, phpsessid, domjudge_cid, folderPath
    if not path.isfile(CONSTANT_CONFIG_PATH):
        create_config()
    
    config = ConfigParser()
    # config.sections()
    config.read(CONSTANT_CONFIG_PATH)
    try:
        language = {x[0]:x[1] for x in config.items('LANGUAGE')}
        phpsessid = config['CREDENTIAL']['PHPSESSID']
        domjudge_cid = config['CREDENTIAL']['domjudge_cid']
        folderPath = config['PATH']['FOLDER_PATH']
    except:
        print("Config is incomplete.")
        # print("Config Path is incomplete. Please try again")
        create_config()
        print("Config completed, please try again")
        exit()
        

def update_config(language={}, cid="", phpsessid="",folderPath=""):
    """Update Config

    Args:
        language (dict, optional): Language to be changed. Defaults to {}.
        cid (str, optional): Cid to be changed. Defaults to "".
        phpsessid (str, optional): phpsesssid to be changed. Defaults to "".
    """
    config = ConfigParser()
    config.read(CONSTANT_CONFIG_PATH)
    if language:
        config['LANGUAGE'] = language
    
    if cid:
        config['CREDENTIAL']['domjudge_cid'] = cid
    
    if phpsessid:
        config['CREDENTIAL']['PHPSESSID'] = phpsessid

    if folderPath:
        config['PATH']['FOLDER_PATH'] = folderPath
        
    with open(CONSTANT_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def create_config():
    config = ConfigParser()
    print(f"{bcolors.WARNING} Creating config{bcolors.ENDC}")
    inputcpp = input(f"{bcolors.WARNING} Choose language for .cpp ( {bcolors.HEADER}cpp{bcolors.WARNING} / {bcolors.HEADER}cpp11{bcolors.OKGREEN} [default]{bcolors.WARNING} ) {bcolors.ENDC}")
    inputpy = input(f"{bcolors.WARNING} Choose language for .py ( {bcolors.HEADER}py2{bcolors.WARNING} / {bcolors.HEADER}py3{bcolors.OKGREEN} [default]{bcolors.WARNING} ) {bcolors.ENDC}")
    
    cpp = "cpp11"
    py = "py3"
    if (inputcpp=="cpp"):
        cpp = "cpp"
    
    if inputpy == "py2":
        py = "py2"
    config['LANGUAGE'] = {'c': 'c',
                        'cpp':cpp,
                        'py': py}

    config['CREDENTIAL'] = {}
    config['CREDENTIAL']['PHPSESSID'] = login()
    config['CREDENTIAL']['domjudge_cid'] = ''
    
    config['PATH'] = {}
    config['PATH']['FOLDER_PATH'] = path.dirname(path.realpath(__file__))
    with open(CONSTANT_CONFIG_PATH, 'w') as configfile:
        config.write(configfile)

def input_cid():
    print(f"{bcolors.OKBLUE} List of current available CID {bcolors.ENDC}")
    
    cookies={"domjudge_cid": "1","PHPSESSID": phpsessid}
    resCid = requests.get("https://socs1.binus.ac.id/quiz/team/index.php", cookies=cookies)
    cidDict = get_cid(resCid.text)
    for x,y in cidDict.items():
        print(f" {bcolors.HEADER} {x} : {bcolors.OKCYAN} {y} {bcolors.ENDC}")                
    print(f"{bcolors.WARNING} Please input the {bcolors.HEADER}CID number! {bcolors.ENDC}")
    cid = input(" ")
    print(f"{bcolors.OKBLUE} Your current CID is {bcolors.HEADER}{cid}{bcolors.WARNING}, saving to config.ini {bcolors.ENDC}")
    update_config(cid=cid)
    
    return cid

def find_id_by_problem(probDict, problem):
    
    try:
        id = probDict[problem]
    except:
        print(f"{bcolors.FAIL} Error when find id by problem {bcolors.ENDC}")
        print(f"{bcolors.FAIL} Please use regular filename '{bcolors.WARNING}(problem).(extension){bcolors.FAIL}' {bcolors.ENDC}")
        print(f"{bcolors.FAIL} Please use correct CID  {bcolors.ENDC}")
        print(f"{bcolors.FAIL} Use '{bcolors.WARNING}python script.py filename ?{bcolors.FAIL}' to reset CID {bcolors.ENDC}")
        print(f"{bcolors.FAIL} Program Aborted {bcolors.ENDC}")
        print(f"{bcolors.FAIL} DEBUG {bcolors.ENDC}")
        print(probDict)
        print(problem)
        exit()
    return id

def get_problem_list(html):
    soup = BeautifulSoup(html, "html.parser")
    # probId = soup.find("select", {"id": "probid"})
    title = soup.title.text;
    check_login(title)
    probDict = {x.text.lower():x.get("value") for x in soup.find("select", {"id": "probid"}).findChildren()}
    return probDict

def get_cid(html):
    """Return CID Dict from SOCS HTML text

    Args:
        html (string): Prefer from response.text

    Returns:
        cidDict (dict {string:string} ): return dict
    """
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text;
    check_login(title)
    cidDict = {x.get("value"):x.text for x in soup.find("select", {"id": "cid"}).findChildren()}
    return cidDict

def get_problem_and_language(text):
    filename = text.split(".")
    if (len(filename) == 2):
        prob, lang = filename
    elif (len(filename) == 3):
        _,prob, lang = filename
        prob = prob[1:]
    newLang = language[lang]
    return prob,newLang
    
def send_file_to_server(filepath, language, probId, domjudge_cid):
    print(filepath, language, probId, domjudge_cid)
    url = "https://socs1.binus.ac.id/quiz/team/upload.php"
    cookies={"domjudge_cid": domjudge_cid,"PHPSESSID": phpsessid}
    files = {'code[]': open(filepath,'rb')}
    values = {'probid': probId, 
            'langid': language, 
            'submit': 'submit'}
    response = requests.post(url, files=files, data=values, cookies=cookies)
    title = BeautifulSoup(response.text, "html.parser").title.text;
    check_login(title)

    return title

def check_login(title):
    if title == "Not Authenticated":
        update_config(phpsessid=login())
        print(f"{bcolors.OKGREEN} Please retry the program {bcolors.ENDC}")
        exit()
    return True

def login():
    """Login to SOCS

    Returns:
        string: phpsessid
    """
    print(f"{bcolors.HEADER} Login Needed! {bcolors.ENDC}")
    print(f"{bcolors.FAIL} Note : Username and Password will not be saved {bcolors.ENDC}")
    print(f"{bcolors.FAIL} But Session Cookies from Login will be save in plain text {bcolors.ENDC}")
    while True:
        print(f"{bcolors.WARNING} ( Ctrl + C ) to exit the program {bcolors.ENDC}")
        
        print(f"{bcolors.WARNING} Please input your username!{bcolors.OKGREEN} [ex:user@binus.ac.id] {bcolors.ENDC}")
        username = input(" ")
        print(f"{bcolors.WARNING} Please input your password!{bcolors.OKGREEN} [Input Hidden] {bcolors.ENDC}")
        password = getpass.getpass(" ")
        print(f"{bcolors.WARNING} Please Wait {bcolors.ENDC}")
        
        params = {
            "cmd": "login",
            "login": username,
            "passwd": password,
        }
        req = requests.Session()
        r = req.get("https://socs1.binus.ac.id/quiz/public/login.php")
        r = req.post("https://socs1.binus.ac.id/quiz/public/login.php", data=params)

        title = BeautifulSoup(r.text, "html.parser").title.text;
        # print(params)
        if (title != "Login failed"):
            print(f"{bcolors.OKGREEN} Login Success {bcolors.ENDC}")
            print(f"{bcolors.OKGREEN} {title} {bcolors.ENDC}")
            return req.cookies["PHPSESSID"]
        else:
            print(f"{bcolors.FAIL} Login Failed {bcolors.ENDC}")
            print(f"{bcolors.FAIL} Error Info : {title} {bcolors.ENDC}")
                
def check_recent_result():
    """Check Answer
    This Program will access phpsessid and cid to work
    """
    url = "https://socs1.binus.ac.id/quiz/team/upload.php"
    cookies={"domjudge_cid": domjudge_cid,"PHPSESSID": phpsessid}
    response = requests.post(url, cookies=cookies)
    soup = BeautifulSoup(response.text, "html.parser") 
    row = soup.find("tr", {"class": "rowodd"})
    time = row.find("a").text
    probId = row.find("td", {"class": "probid"}).find("a").text
    langId = row.find("td", {"class": "langid"}).find("a").text
    # result may be have 1 result if currently is pending
    resultBox = row.find("td", {"class": "result"}).find("a").text
    if (resultBox == "pending"):
        result = resultBox
        point = 0
    else:
        result, point = resultBox.split(" ")
    # result, point = resultBox.text.split(" ")
    return time, probId, langId, result, point
    
def wait_result():
    dot = 0
    # print("Pending")
    print("")
    while True:
        time, probId, langId, result, point = check_recent_result()
        # I could create threading but not worth my time here
        dot = (dot+1) if dot < 5 else 1
        print("\033[A                                                                         \033[A")
        # print(point)
        if (result == "pending"):
            print(f"{bcolors.OKCYAN}{time}{bcolors.WARNING} | {probId} {langId} | {bcolors.ENDC}{result}",
                  ("."*dot))
        elif (result == "correct"):
            print(f"{bcolors.OKCYAN}{time}{bcolors.WARNING} | {probId} {langId} | ",
                  f"{bcolors.OKGREEN}{result} {point}{bcolors.ENDC}")
            break
        else:
            print(f"{bcolors.OKCYAN}{time}{bcolors.WARNING} | {probId} {langId} | ",
                  f"{bcolors.FAIL}{result} {point}{bcolors.ENDC}")
            break
        # print(point)
        # print(")
        sleep(0.5)

def check_file_path(filePath):
    """Check File Path

    Args:
        filePath (string): File Name or Path
        global folderPath may be needed to be accessed

    Returns:
        string: folderpath
        string: filePath
    """
    global folderPath
    if (":" in filePath):
        folderPath, filePath = filePath.rsplit('\\', 1)
        # print(folderPath)
        # print(path.dirname(path.realpath(__file__)))
        update_config(folderPath=folderPath)
        return folderPath, filePath
    else:
        return folderPath, filePath
    
    
if __name__ == "__main__":
    main()