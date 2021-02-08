import sys, requests, datetime, pyautogui, time, getpass, os
from termcolor import colored
from colorama import init
from datetime import datetime, date

start_message = 'Write "start" for start the program'

try:
    with open('API_KEY') as inf:
        api_key = inf.read()
except FileNotFoundError:
    api_key = input("Please enter your API key: ")
    with open('API_KEY', 'w') as outf:
        outf.write(api_key)

Mass = []
rank1 = 25000
rank2 = 70000
rank3 = 150000

adminlist = ["Guild Master", "Helper", "Admin"]
Ranked = ['Member', 'Active', 'Old']

def getcollor(N):
    try:
        N = int(N.replace(",", ""))
    except Exception:
        pass
    if N <= rank1:
        return 'red'
    elif rank1 < N <= rank2:
        return 'yellow'
    elif rank2 < N <= rank3:
        return 'green'
    elif N > rank3:
        return 'cyan'

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
        print(f'[LOG] Complite {i + 1}/{N}')
    print(f'[LOG] Update complite successfully')


time.sleep(1)
guild = input("ENTER A GUILD NAME: ")

g = requests.get("https://api.hypixel.net/guild?key=" + api_key + "&name=" + guild)
g = g.json()

print(start_message)
command = input('Write start: ').lower()
while True:
    if command != 'start':
        print('Wrong command')
        command = input('Write start: ')
    else:
        print('Successful')
        time.sleep(0.5)
        update()
        break
TopforGXP()