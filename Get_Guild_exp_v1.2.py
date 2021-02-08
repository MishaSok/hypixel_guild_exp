import sys, requests, datetime, pyautogui, time, getpass, os
from termcolor import colored
from colorama import init
from datetime import datetime, date

start_message = 'Write "start" for start the program'
main_message = 'update - update all members information\ninactive - set inactive number of Guild Exp\n' \
               'start day - set the number of days in which the program will not kick newbies in the guild\n' \
               'top - show top members in guild'

try:
    with open('API_KEY') as inf:
        api_key = inf.read()
except FileNotFoundError:
    api_key = input("Please enter your API key: ")
    with open('API_KEY', 'w') as outf:
        outf.write(api_key)

Mass = []
rank1 = 10000
rank2 = 70000
rank3 = 150000
start_days = ''

adminlist = ["Guild Master", "Helper", "Admin"]
Ranked = ['Member', 'Active', 'Old']


def getcollor(N):
    try:
        N = int(N.replace(",", ""))
    except Exception:
        pass
    if N <= rank1:
        return 'red'
    elif N > rank1:
        return 'green'


def gettime(ts):
    ts = ts / 1000
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d')


def TopforGXP():
    Mass.sort(key=lambda i: i[1], reverse=True)
    Counter = 0
    for i in Mass:
        Counter += 1
        N = i[0].ljust(17, ' ')
        a = gettime(i[3]).split('-')
        aa = date(int(a[0]), int(a[1]), int(a[2]))
        bb = date.today()
        JoinDate = str((bb - aa).days)
        print(colored(f"№{str(Counter).rjust(3, '0')} {N}got {'{:,}'.format(i[1])} GXP  (join {JoinDate} days ago)",
                      getcollor(i[1])))


def update():
    global Mass
    Mass = []
    N = len(g['guild']['members'])
    for i in range(len(g['guild']['members'])):
        uuid = g['guild']['members'][i]['uuid']
        x = requests.get("https://playerdb.co/api/player/minecraft/" + uuid)
        x = x.json()
        name = x['data']['player']['username']
        expHistory = g['guild']['members'][i]['expHistory']
        time = g['guild']['members'][i]['joined']
        rank = g['guild']['members'][i]['rank']
        expHistory = sum(expHistory.values())
        expHistory = "{:,}".format(sum(g['guild']['members'][i]['expHistory'].values()))
        Mass.append([name, int(expHistory.replace(',', '')), rank, time, g['guild']['members'][i]['expHistory']])
        print(colored(f'[{guild} guild] Getting info: {i + 1}/{N}', 'blue'))
    print(colored(f'[{guild} guild] Update complete successfully', 'green'))


def get_inactive_num():
    while True:
        global rank1
        try:
            rank1 = int(input('Write inactive num: '))
            break
        except ValueError:
            print(colored('Syntax Error', 'red'))
            continue


def Autospam():
    print(colored('Auto promote start in 5 seconds!', 'red'))
    time.sleep(5)
    print(colored('Auto promote start!!!!', 'red'))
    for i in Mass:
        if i[2] != getrank(i[1]):
            if i[2] != "Guild Master" and i[2] != "Helper" and i[2] != "Admin":
                a = gettime(i[3]).split('-')
                aa = date(int(a[0]), int(a[1]), int(a[2]))
                bb = date.today()
                JoinDate = str((bb - aa).days)
                if getrank(i[1]) == "kicked" and int(JoinDate) >= 10:
                    pyautogui.hotkey("t")
                    time.sleep(0.2)
                    pyautogui.write(f"/g kick {i[0]} Inactive")
                    time.sleep(0.5)
                    pyautogui.hotkey("enter")
                    time.sleep(0.3)
                else:
                    if getrank(i[1]) != 'kicked':
                        pyautogui.hotkey("t")
                        time.sleep(0.2)
                        pyautogui.write(f"/g setrank {i[0]} {getrank(i[1])}")
                        time.sleep(0.5)
                        pyautogui.hotkey("enter")
                        time.sleep(0.3)


def getrank(N):
    try:
        N = int(N.replace(",", ""))
    except Exception:
        pass
    if N <= rank1:
        return "kicked"


def get_start_day():
    while True:
        global start_days
        try:
            start_days = int(input('Write inactive num: '))
            break
        except ValueError:
            print(colored('Syntax Error', 'red'))
            continue


time.sleep(1)
guild = input(colored("ENTER A GUILD NAME: ", 'red'))

g = requests.get("https://api.hypixel.net/guild?key=" + api_key + "&name=" + guild)
g = g.json()

print(colored(start_message, 'red'))
command = input(colored('Write start: ', 'red')).lower()
while True:
    if command != 'start':
        print(colored('Wrong command', 'red'))
        command = input(colored('Write start: ', 'red')).lower()
    else:
        print(colored('Successful', 'green'))
        time.sleep(0.5)
        update()
        break

while True:
    print(colored('=====================================', 'cyan'))
    print(colored('List of available commands:', 'blue'))
    print(colored(main_message, 'yellow'))
    print(colored('=====================================', 'cyan'))
    command = input(colored('Command: ', 'blue')).lower()
    if command == 'update':
        update()
        time.sleep(1)
    elif command == 'top':
        TopforGXP()
        time.sleep(1)
    elif command == 'inactive':
        get_inactive_num()
        time.sleep(1)
    elif command == 'start day' or command == 'start days':
        get_start_day()
        time.sleep(1)


