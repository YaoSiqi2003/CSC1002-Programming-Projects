import random

print('Prompt:The objective of the game is to re-arrange the tiles into a sequential order by their numbers \
(left to right, top to bottom) by repeatedly making sliding moves (left, right, up or down). At the \
starting point of the game,the player needs to repeatedly slide one adjacent tile, one at a time, to \
the unoccupied space (the empty space,represented by number 0) until all numbers appear sequentially\n')

#This function gets user input: puzzle size and the four letters used for directions 
def getInput():
    letter = input('Enter the four letters used for left, right, up, and down move:')
    letter_list = letter.split()
    letter_list2 = []
    for i in letter_list:
        if i not in letter_list2:
            letter_list2.append(i) #Put all distinct letters from letter_list into letter_list2
    
    #If the letters entered by user meet the standard, that is, there are only four distinct single letters,
    #then all four element s in letter_list2 has the attribute s.isalpha() = True and len(s) = 1.
    #If the input is invalid, user has to re-enter until the input is valid
    while not ([s.isalpha() and len(s) == 1 for s in letter_list2] == [True,True,True,True]):
        print('Invalid input! Enter exactly four distinct letters!')
        letter = input('Enter the four letters used for left, right, up, and down move:')
        letter_list = letter.split()
        letter_list2 = []
        for i in letter_list:
            if i not in letter_list2:
                letter_list2.append(i)

    while True:
        choose = input('Enter \'1\' for 8-puzzle, \'2\' for 15-puzzle or \'q\' to end the game:')
        if choose == '1':
            dim = 9 #Record dimension of the board
            break
        elif choose == '2':
            dim = 16
            break
        elif choose == 'q':
            print('Bye!')
            exit()
        else:
            print('Invalid input! Please enter again!')

    return letter_list2[0],letter_list2[1],letter_list2[2],letter_list2[3],dim #Return the four letters for directions
    # and dimension of the board


#This function obtains the number of inversions of a permutation
def getInverseNumber(numlist):
    count = 0 #Count the number of inversions
    for j in range(len(numlist)):
        for k in range(j):
            if numlist[k] > numlist[j]:#numlist[k] > numlist[j] mean that there is an inversion,the larger number is 
                #placed before a smaller number, e.g. 1 2 4 3, 4 (numlist[k]) is placed before 3 (numlist[j]).
                count += 1 #Add 1 to the number of inversions
    return count


#This function swaps the positions of two numbers in a list
def swapPositions(list,pos1,pos2):
    list[pos1],list[pos2] = list[pos2],list[pos1]
    return list


#This function generates a solvable sliding puzzle
def generatePuzzle(dim):
    numlist = []
    puzzleDict = {}#The data model for the puzzle

    for num in range(dim):
        numlist.append(num)#Generate an ordered number list([0,1,2,```8] or [0,1,2,```16])
    random.shuffle(numlist)#Shuffle the numbers and obtain a random permutation

    index = numlist.index(0)
    numlist[index] = ' '#Change the '0' into a space so that the space will be shown on the board instead of '0'

    #Determine whether the puzzle is solvable, and if not, adjust it to be solvable.
    if dim == 9:
        numlist2 = numlist
        numlist2.pop(index)#Remove the ' ' from numlist2 s.t. numlist2 only consists of numbers from 1 to 8
        if getInverseNumber(numlist2) % 2 != 0: #For 3*3 puzzle, if the inverse number of list 2 is odd then the 
            #puzzle is unsolvabe. To make the number of inversions even, it is necessary to swap the positions of 
            # two numbers.
            numlist2 = swapPositions(numlist2,0,1)

        numlist2.insert(index,' ')#Put the removed space back to its original place
        numlist = numlist2 #Puzzle is now solvable

    if dim == 16:
        puzzlelist = [numlist[:4],numlist[4:8],numlist[8:12],numlist[12:16]]
        for i in range(len(puzzlelist)):
                if ' ' in puzzlelist[i]:
                    record = i #Record the row index where the blank space is.

        numlist2 = numlist
        numlist2.pop(index)
        
        if getInverseNumber(numlist2) % 2 == 0:#For 4*4 puzzle, if the inverse number is even and the 
            #difference between the current row number of the blank space and the last row number of the 
            # blank space is odd, then puzzle is unsolvabe. So we have to exchange two rows
            if (record - 3) % 2 != 0:#Note that the index of last row is 3 instead of 4 since the index
                #starts from 0
                swapPositions(puzzlelist,record,1)#Exchange the row with the second row(index 1)

            numlist = []
            for i in puzzlelist:
                for j in i:
                    numlist.append(j) #Puzzle is now solvable

        elif getInverseNumber(numlist2) % 2 != 0:#For 4*4 puzzle, if the inverse number is odd and the 
            #difference between the current row number of the blank space and the initial row (the last row)
            # number of the blank space is even, then puzzle is unsolvabe. So row exchange is needed.
            if record == 1:#The only situation needed to be considered is the current row number is the second row
                #(index 1)
                swapPositions(puzzlelist,1,0)
            
            numlist = []
            for i in puzzlelist:
                for j in i:
                    numlist.append(j) #Puzzle is now solvable

    #Construct the data model for the puzzle using a dictionary.Note that the keys are 1 to 4 instead of 0 to 3
    puzzleDict[1] = numlist[:int(dim**(1/2))]#The first row of the board
    puzzleDict[2] = numlist[int(dim**(1/2)):int(2*dim**(1/2))]#The second row
    puzzleDict[3] = numlist[int(2*dim**(1/2)):int(3*dim**(1/2))]#The third row

    if dim == 16:
        puzzleDict[4] = numlist[int(3*dim**(1/2)):int(4*dim**(1/2))]#The fourth row
    
    return puzzleDict


#Print the game board
def displayPuzzle(puzzleDict):
    for value in puzzleDict.values():#Note that values of puzzleDict are lists
        for element in value:
            if len(str(element)) == 1:
                print(str(element)+' ',end = ' ')#If the number has only one digit, print an extra space s.t.
                #it is well aligned with two digit numbers
            else:
                print(element,end = ' ')
        print('\n')


#This function detects whether numbers adjacent to the space can move left/right/up/down
def detectPosition(puzzleDict):
    #Detect whether adjacent number can move left
    leftValid = False
    leftrow = 0
    for detect in puzzleDict.values():
        leftrow += 1 #Record the row where the space is located
        if ' ' in detect and (detect.index(' ') != (len(detect)-1)):#As long as the space is not located at the right
            #end of the row(the last position of row list), adjacent number can move left
            leftValid = True #Can move left
            break

    #Detect whether adjacent number can move right
    rightValid = False
    rightrow = 0
    for detect in puzzleDict.values():
        rightrow += 1
        if ' ' in detect and (detect.index(' ') != 0):#As long as the space is not located at the left
            #end of the row(the first position of row list), adjacent number can move right
            rightValid = True #Can move right
            break
        
    #Detect whether adjacent number can move up
    upValid = False
    uprow = 0
    for i in range(1,int(dim**(1/2))):
        if ' ' in puzzleDict[i]:#As long as the space is not located at the last row (the bottom of the board),
            #adjacent number can move up
            upValid = True
            uprow = i
            break

    #Detect whether adjacent number can move down
    downValid = False
    downrow = 0
    for i in range(2,int(dim**(1/2))+1):
        if ' ' in puzzleDict[i]:#As long as the space is not located at the first row (the top of the board),
            #adjacent number can move down
            downValid = True
            downrow = i
            break
    return leftValid,rightValid,upValid,downValid,leftrow,rightrow,uprow,downrow


#The function that performs operation on the board
def move(puzzleDict):
    leftValid,rightValid,upValid,downValid,leftrow,rightrow,uprow,downrow = detectPosition(puzzleDict)
    prompt = ''
    if leftValid:#If adjacent number can move left
        prompt += f' left-{left}'
    if rightValid:
        prompt += f' right-{right}'
    if upValid:
        prompt += f' up-{up}'
    if downValid:
        prompt += f' down-{down}'
    moveOper = input('Enter your move'+prompt+':').lower()

    try:
        if moveOper == left:#If user entered the letter for left
            newrow = puzzleDict[leftrow]#Obtain the row where the space is located
            index = newrow.index(' ')
            newrow[index],newrow[index+1] = newrow[index+1],' '#Exchange the positions of blank space and the number
            puzzleDict[leftrow] = newrow #The action is done
            displayPuzzle(puzzleDict)

        elif moveOper == right:
            newrow = puzzleDict[rightrow]
            index = newrow.index(' ')
            newrow[index],newrow[index-1] = newrow[index-1],' '
            puzzleDict[rightrow] = newrow
            displayPuzzle(puzzleDict)

        elif moveOper == up:
            newrow = puzzleDict[uprow]
            index = newrow.index(' ')
            nextrow = puzzleDict[uprow+1]
            newrow[index],nextrow[index] = nextrow[index],' '#Exchange the positions of blank space and the number below it
            puzzleDict[uprow] = newrow
            puzzleDict[uprow+1] = nextrow
            displayPuzzle(puzzleDict)

        elif moveOper == down:
            newrow = puzzleDict[downrow]
            index = newrow.index(' ')
            lastrow = puzzleDict[downrow-1]
            newrow[index],lastrow[index] = lastrow[index],' '
            puzzleDict[downrow] = newrow
            puzzleDict[downrow-1] = lastrow
            displayPuzzle(puzzleDict)
    except:
        print('Cannot move in this direction!')


left,right,up,down,dim = getInput()
puzzleDict = generatePuzzle(dim)
displayPuzzle(puzzleDict)


step = 0 #Record the number of steps required for the player to complete the game.
while True:
    move(puzzleDict)#Perform a move
    step += 1
    if (dim == 9 and puzzleDict == {1:[1,2,3],2:[4,5,6],3:[7,8,' ']}) or \
        (dim == 16 and puzzleDict == {1:[1,2,3,4],2:[5,6,7,8],3:[9,10,11,12],4:[13,14,15,' ']}):#Check whether the game
        #had been completed
        next = input(f'You\'ve won! Took {step} steps! Enter \'q\' for quit and \'new\' for another round:')
        if next == 'q':
            print('Bye')
            exit()
        elif next == 'new':
            print('New game will start.')
            left,right,up,down,dim = getInput()
            puzzleDict = generatePuzzle(dim)
            displayPuzzle(puzzleDict)
            step = 0