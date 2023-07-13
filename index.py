# Написать программу, которая удаляет из списка все элементы, стоящие на четных позициях.
def delEvenElFromArray(arr):
    newArr = []
    for index in range(len(arr)):
        if index % 2 == 0:
            newArr.append(arr[index])
    return newArr

# print(delEvenElFromArray([11,2,3,2,1,2,4,2,3]))

# =====================================================================================================================

# Написать программу, которая считывает список слов и находит слова, содержащие более трех гласных букв.
def findStrWithThreeVowelsFromArray(arrOfStr):
    arrayOfStrWithThreeVowels = []
    vovels = ["а", "е", "ё", "и", "о", "у", "ы", "э", "ю", "я"]
    for arrOfStrEl in arrOfStr:
        vowelscCounter = 0
        for strEl in arrOfStrEl:
            if strEl in vovels:
                vowelscCounter += 1
        if vowelscCounter >= 3:
            arrayOfStrWithThreeVowels.append(arrOfStrEl)
    return(arrayOfStrWithThreeVowels)

# print(findStrWithThreeVowelsFromArray(['Написать',
#  'программу,',
#  'которая',
#  'считывает',
#  'список',
#  'слов',
#  'и',
#  'находит',
#  'слова,',
#  'содержащие',
#  'более',
#  'трех',
#  'гласных',
#  'букв']))

# =====================================================================================================================

# Написать программу, которая находит второй по величине элемент в списке.
def findSeсondMaxElFromArray(arrOfInt):
    maxInt=arrOfInt[0]
    secondMaxInt=0
    temp=0
    for intFromArray in arrOfInt:
        if intFromArray > maxInt:
            temp = maxInt
            maxInt = intFromArray
        if temp > secondMaxInt:
            secondMaxInt = temp
        if maxInt > intFromArray > secondMaxInt:
            secondMaxInt = intFromArray
    return(secondMaxInt)

# print(findSeсondMaxElFromArray([36,35,8,11,5,13,21,4,4,21,20, 33, 33, 34]))

# =====================================================================================================================

# Написать программу, которая удаляет из списка все дубликаты.
def delAllDuplicate(arr):
    newArr = []
    for el in arr:
        if el not in newArr:
            newArr.append(el)
    return newArr

# print(delAllDuplicate([1, 5,'a','3',1 ,5 ,'a','3',1 ,5 ,'a','3', 33, 43, 1, 5,'a','33']))

# =====================================================================================================================

# Написать программу, которая считывает данные из CSV-файла и создает словарь,
# где ключами являются значения в столбце «Name», а значениями — соответствующие им словари с информацией о поле,
# возрасте и зарплате.
import csv
def createDictFromCSV2(path):
    with open(path, 'r', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ";")
        dictOfDicts = {}
        colNames = []
        counter = 0
        for row in spamreader:
            if counter == 0:
                colNames = row
            else:
                personInfoDict = {}
                for index in range(len(row)):
                    if index != 0:
                        personInfoDict.update({colNames[index]: row[index]})
                dictOfDicts.update({row[0]:personInfoDict})
            counter +=1
    return dictOfDicts

# print(createDictFromCSV2('salary.csv'))

# =====================================================================================================================

# Написать программу, которая запрашивает у пользователя строку и выводит на экран все
# ее подстроки длиной не менее трех символов.

def filterInputStr():
    inputStr = input('Введите строку: ')
    arrOfStr = inputStr.split()
    newArr = []
    for strEl in arrOfStr:
        if len(strEl) >= 3:
            newArr.append(strEl)
    return ' '.join(newArr)

# print(filterInputStr())