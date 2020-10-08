import random
import time
import kahootDefs as kDefs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

totalKahootBots = input('Kahoot Bots To Summon\n> ')
try:
    totalKahootBots = int(totalKahootBots)
    print()
except:
    print('Error, Unsupported Input. Default (3)\n')
    totalKahootBots = 3

kahootPin = ''
while type(kahootPin) != type(0):
    kahootPin = input('Kahoot Pin\n> ')
    try:
        kahootPin = int(kahootPin)
    except:
        print('\nUnsupported Input')

URL = 'https://www.kahoot.it/'


def switchTab(tabID):
    driver.switch_to.window(allTabs[tabID])


with open('usernames.txt', 'r') as file:
    usernameList = [line.replace('\n', '') for line in file]
    random.shuffle(usernameList)

# DRIVER OPTIONS
options = Options()
options.add_argument("-incognito --headless")

# START DRIVER
driver = webdriver.Chrome(options=options)
driver.get(URL)

# OPEN WINDOWS
for _ in range(totalKahootBots - 1):
    driver.execute_script(f"window.open('{URL}');")
allTabs = driver.window_handles


class badPin(Exception):
    pass


# Start Bots
try:
    # ENTER PIN
    for tabID in range(totalKahootBots):
        switchTab(tabID)
        driver.find_element_by_id('game-input').send_keys(kahootPin)
        driver.find_element_by_class_name('enter-button__EnterButton-sc-1o9b9va-0').click()

        if tabID == 0:
            try:
                time.sleep(1)
                driver.find_element_by_id('nickname')
            except:
                raise badPin
                break

        print(f'BOT ID {tabID + 1}\t::\tStarting')

    print()

    # ENTER USERNAME
    botUsernames = []
    for tabID in range(totalKahootBots):
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

tempScore, totalScore = [0 for _ in range(totalKahootBots)], [0 for _ in range(totalKahootBots)]

while True:
    if tempPAGE != driver.current_url:
        if driver.current_url == "https://kahoot.it/v2/gameblock":
            questionCounter = driver.find_element_by_class_name('question-top-bar__QuestionNumber-sc-1pwisow-3').text
            for tabID in range(totalKahootBots):
                switchTab(tabID)
                viableAnswers = kDefs.findViableAnswers(driver)
                kDefs.pickAnswer(viableAnswers)

                try:
                    driver.find_element_by_class_name('quiz-board__SubmitButton-sc-1vv00zg-4').click()
                except:
                    pass

                print(f'BOT ID {tabID + 1}\t:: {botUsernames[tabID]} >> Q {questionCounter} >> Answered.')

            switchTab(0)
            tempPAGE = driver.current_url
            print()

        elif driver.current_url == "https://kahoot.it/v2/answer/result":
            for tabID in range(totalKahootBots):
                switchTab(tabID)
                time.sleep(0.25)
                totalScore[tabID] = int(driver.find_element_by_class_name('result-bottom-bar__Score-sc-193ouyp-2').text)
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
