import random, time, os
import kahootDefs as kDefs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

kahootPin, totalBotCount = '', ''
genRandomUsernames, randomCharacters = False, 4
URL = 'https://www.kahoot.it/'

def clear():
    os.system('cls')

def switchTab(tabID):
    driver.switch_to.window(allTabs[tabID])

while True:
    clear()
    if genRandomUsernames == False:
        mainMenuInput = input(f'''---= Kahoot Spammer V2.0 =---
1) Pin :: {kahootPin}
2) Bot Count :: {totalBotCount}
3) Username Generator :: From File


9) Launch Attack
q) Exit Program

> ''')

    else:
         mainMenuInput = input(f'''---= Kahoot Spammer V2.0 =---
1) Pin :: {kahootPin}
2) Bot Count :: {totalBotCount}
3) Username Generator :: Random
4) Character Count :: {randomCharacters}

9) Launch Attack
q) Exit Program

> ''')  

    if mainMenuInput == '1':
        kahootPin = ''
        clear()
        while type(kahootPin) != type(0):
            kahootPin = input('---= Kahoot Spammer V2.0 =---\n1) Pin :: ')
            clear()
            try:
                kahootPin = int(kahootPin)
                if len(str(kahootPin)) < 5:
                    raise Exception
            except Exception:
                kahootPin = ''
                print('Error, Unsupported/Incorrect Input\n')

    elif mainMenuInput == '2':
        totalBotCount = ''
        clear()
        while type(totalBotCount) != type(0):
            totalBotCount = input(f'---= Kahoot Spammer V2.0 =---\n1) Pin :: {kahootPin}\n2) Bot Count :: ')
            clear()
            try:
                totalBotCount = int(totalBotCount)
            except Exception:
                print('Error, Unsupported Input.\n')

    elif mainMenuInput == '3':
        genRandomUsernames = True if genRandomUsernames == False else False

    elif mainMenuInput == '4' and genRandomUsernames == True:
        randomCharacters = ''
        clear()
        while type(randomCharacters) != type(0):
            randomCharacters = input(f'''---= Kahoot Spammer V2.0 =---
1) Pin :: {kahootPin}
2) Bot Count :: {totalBotCount}
3) Username Generator :: Random
4) Character Count :: ''')
            clear()
            try:
                randomCharacters = int(randomCharacters)
                if randomCharacters < 3 or randomCharacters > 15:
                    raise Exception
            except Exception:
                randomCharacters = ''
                print('Error, Unsupported/Incorrect Input\n')

    elif mainMenuInput == '9' and totalBotCount != '' and kahootPin != '':
            break
    
    elif mainMenuInput == 'q':
        exit()

clear()

if genRandomUsernames == False:
    with open('usernames.txt', 'r') as file:
        usernameList = [line.replace('\n', '') for line in file]
        random.shuffle(usernameList)
else:
    usernameList = [kDefs.genRandomUsernames(randomCharacters) for i in range(totalBotCount)]

# DRIVER OPTIONS
options = Options()
options.add_argument("-incognito --headless")

# START DRIVER
driver = webdriver.Chrome(options=options)
driver.get(URL)

print('\nOpening Bot Instances\n')

# OPEN WINDOWS
for _ in range(totalBotCount - 1):
    driver.execute_script(f"window.open('{URL}');")
allTabs = driver.window_handles


class badPin(Exception):
    pass

# Start Bots
try:
    # ENTER PIN
    for tabID in range(totalBotCount):
        switchTab(tabID)
        driver.find_element_by_id('game-input').send_keys(kahootPin)
        driver.find_element_by_class_name('enter-button__EnterButton-sc-1o9b9va-0').click()

        if tabID == 0:
            print('Checking Pin.\n')
            try:
                time.sleep(3)
                driver.find_element_by_id('nickname')
                print('Confirmed Valid Pin.\n')
            except:
                raise badPin
                break

        print(f'BOT ID {tabID + 1}\t::\tStarting')
    print()

    # ENTER USERNAME
    botUsernames = []
    for tabID in range(totalBotCount):
        switchTab(tabID)
        botUsernames.append(usernameList.pop())

        time.sleep(0.25)

        driver.find_element_by_id('nickname').send_keys(botUsernames[tabID])
        driver.find_element_by_class_name('enter-button__EnterButton-sc-1o9b9va-0').click()

        print(f'BOT ID {tabID + 1}\t:: {botUsernames[tabID]} >> Joined')

except badPin:
    print(f"Invalid Pin :: '{kahootPin}'")
    driver.quit()

switchTab(0)
tempPAGE = driver.current_url
print()

tempScore, totalScore = [0 for _ in range(totalBotCount)], [0 for _ in range(totalBotCount)]

while True:
    if tempPAGE != driver.current_url:
        if driver.current_url == "https://kahoot.it/v2/gameblock":
            questionCounter = driver.find_element_by_class_name('question-top-bar__QuestionNumber-sc-1pwisow-3').text
            for tabID in range(totalBotCount):
                switchTab(tabID)
                viableAnswers = kDefs.findViableAnswers(driver)
                kDefs.pickAnswer(viableAnswers)

                try:
                    driver.find_element_by_class_name('quiz-board__SubmitButton-sc-1vv00zg-4').click()
                except Exception:
                    pass

                print(f'BOT ID {tabID + 1}\t:: {botUsernames[tabID]} >> Q {questionCounter} >> Answered.')

            switchTab(0)
            tempPAGE = driver.current_url
            print()

        elif driver.current_url == "https://kahoot.it/v2/answer/result":
            for tabID in range(totalBotCount):
                switchTab(tabID)
                time.sleep(0.15)
                try:
                    totalScore[tabID] = int(driver.find_element_by_class_name('result-top-bar__Score-sc-11jv73d-4').text)
                except:
                    try:
                        totalScore[tabID] = int(driver.find_element_by_class_name('result-bottom-bar__Score-sc-193ouyp-2').text)
                    except:
                        totalScore[tabID] = 0

                scoreDiff = totalScore[tabID] - tempScore[tabID]

                print(
                    f'BOT ID {tabID + 1}\t:: {botUsernames[tabID]} >> Q {questionCounter} >> Current Score >> {totalScore[tabID]} (+{scoreDiff})')
                tempScore[tabID] = totalScore[tabID]

            switchTab(0)
            tempPAGE = driver.current_url
            print()

        elif driver.current_url == "https://kahoot.it/v2/ranking":
            print(f'Game Finshed. Closing All Bots.')
            driver.quit()
            break

input()
