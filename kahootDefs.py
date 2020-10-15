import random
import string


def findViableAnswers(driver):
    viableAnswers = []
    try:
        global triangleButton
        triangleButton = driver.find_element_by_id('triangle-button')
        viableAnswers.append('Triangle')
    except:
        pass
    try:
        global diamondButton
        diamondButton = driver.find_element_by_id('diamond-button')
        viableAnswers.append('Diamond')
    except:
        pass
    try:
        global circleButton
        circleButton = driver.find_element_by_id('circle-button')
        viableAnswers.append('Circle')
    except:
        pass
    try:
        global squareButton
        squareButton = driver.find_element_by_id('square-button')
        viableAnswers.append('Square')
    except:
        pass
    return viableAnswers


def pickAnswer(viableAnswers):
    answerChoice = random.choice(viableAnswers)
    if answerChoice == 'Triangle':
        triangleButton.click()
    elif answerChoice == 'Diamond':
        diamondButton.click()
    elif answerChoice == 'Circle':
        circleButton.click()
    elif answerChoice == 'Square':
        squareButton.click()

def genRandomUsernames(nameLen):
    nameString = ''
    for i in range(nameLen):
        letterList = list(string.ascii_letters)
        random.shuffle(letterList)
        nameString += letterList.pop()
    return nameString