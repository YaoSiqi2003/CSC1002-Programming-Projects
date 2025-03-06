import turtle

#Initialize gameboard
def initBoard():
    global gameBoard,tokenBoard,winner
    gameBoard = [] #Record the status of the chessboard
    tokenBoard = [] #Record the tokens that have been put
    winner = None

    for _ in range(8):
        gameBoard.append([0] * 8)
        tokenBoard.append([None] * 8)
        #0 stands for an empty place on the chessboard. The 2 players are labled 0,1 and their tokens are labeled 
        #1,2 respectively


#Initialize game
def createGame(canvas):
    global rectangleWidth,rectangleHeight
    rectangleWidth,rectangleHeight = 60,20
    
    # Set up the turtle graphics window
    canvas.setup(width=1.0, height=1.0, startx=None, starty=None)#Set width and height to 1.0 s.t. the canvas covers the whole screen
    
    #Set the coordinates of the lower left corner and the top right corner of the window 
    canvas.setworldcoordinates(-canvas.window_width() / 2, -canvas.window_height() / 2,
                               canvas.window_width() / 2, canvas.window_height() / 2)

    #Create 8 turtle objects to represent 8 column trackers
    global rectangleTurtles
    rectangleTurtles = []
    toLeftMargin = 375 #The distance of the leftmost rectangle from the left margin
    gap = (canvas.window_width() - 2 * toLeftMargin - 7 * rectangleWidth) / 7#Calculate the distance between each column tracker
    for i in range(8):
        rectangle = turtle.Turtle()
        rectangle.hideturtle()
        rectangle.penup()
        rectangle.goto(-canvas.window_width() / 2 + toLeftMargin + i * (rectangleWidth + gap), \
                       -canvas.window_height() / 2 + 100 + 0.5 * rectangleHeight)
        rectangle.color("black")
        rectangle.shape("square")
        rectangle.shapesize(1,3)
        rectangle.fillcolor("black")
        rectangle.showturtle()
        rectangleTurtles.append(rectangle)


#This function determines whether there is empty space in the specified column to place a token
def searchRow(table,column):
    rowNum = 8 #The rows of the table are labled as 0 to 7 from up to down
    for row in table[::-1]: #Start searching from the last row labeled 7
        rowNum -= 1
        try:
            if row[column] == 0:#An empty space 
                return rowNum
        except:
            pass


#Generate a token
def createToken(x, y, color):
    token = turtle.Turtle()
    token.hideturtle()
    token.penup()
    token.goto(x, y)
    token.color(color)
    token.shape("circle")
    token.shapesize(3,3)
    token.showturtle()
    return token


#Check whether the game is won after a new token is placed
def checkWinner(column, row):
    global gameBoard, winner
    directions = [(-1, 0), (0, 1), (-1, 1), (1, 1)]
    player = gameBoard[row][column]#The player which the new token stands for
    for direction in directions:
        count = 1 #Records the number of consecutive same-colored tokens
        winningTokens = [(row, column)]
        for i in range(1, 4):#Traverse the four directions, each time goingin the positive direction first,then in the opposite direction
            newRow,newCol = row + direction[1] * i,column + direction[0] * i
            if 0 <= newRow < 8 and 0 <= newCol < 8 and gameBoard[newRow][newCol] == player:
                count += 1
                winningTokens.append((newRow, newCol))
            else:
                break #Exit the loop once an odd-colored token (discontinuity) is found

        for i in range(1, 4):
            newRow,newCol = row - direction[1] * i,column - direction[0] * i
            if 0 <= newRow < 8 and 0 <= newCol < 8 and gameBoard[newRow][newCol] == player:
                count += 1
                winningTokens.append((newRow, newCol))
            else:
                break 

        if count >= 4:#If the are at least 4 consecutive same-colored tokens
            winner = player
            highlightWinningTokens(winningTokens)
            return


def checkTie(table):
    if 0 not in table[0]:
        return True

#Draw red margins for winning tokens
def highlightWinningTokens(winningTokens):
    global tokenBoard
    for row, column in winningTokens:
        token = tokenBoard[row][column]
        token.shapesize(3,3,5)
        token.pencolor('red')

    canvas.title(f'Player {3-winner} has won')
    canvas.update()


def updateGameBoard(column, row):
    global gameBoard
    gameBoard[row][column] = currentPlayer + 1


DELAY = 100 # Time delayed in milliseconds
timerTriggered = False
#Call onMouse function after a certain time s.t. the mouse won't seem too sensitive
def delayedOnMouse(x):
    global timerTriggered
    if not timerTriggered:
        timerTriggered = True #Set timeTriggered to True s.t. only one event can be executed at a time
        turtle.ontimer(lambda:onMouse(x), DELAY)


onMouseExecuted = False #Judge whether mouse click can be performed
def onMouse(x):
    global timerTriggered,onMouseExecuted,winner
    timerTriggered = False
    #Freeze the screen when the game is won
    if winner is not None:
        return
    i = -1
    for rectangle in rectangleTurtles:#Check each column tracker (rectangle) from left to right and see if the mouse is within its range.
        i += 1 #Columns are labeled from 0 to 7, i starts from 0
        if abs(rectangle.xcor() - x) <= 30 :#Judge whethermouse's horizontal coordinate is between the left and right vertical edges of the rectangle
            rectangle.shapesize(1,3,5) #Set margin size of the rectangle to 5 pixels
            if currentPlayer == 0:
                rectangle.color(color1,'black')
            else:
                rectangle.color(color2,'black')

            canvas.update()
            onMouseExecuted = True #Mouse click can be performed
            column = i #Record the column tracker that had been highlighted 
        else:
            rectangle.shapesize(1,3,1)#If the mouse is not within its range, change its margin to black as before
            rectangle.color('black','black')
            canvas.update()
    try:
        return column
    except:
        pass
        
    
def onclick(x):
    global onMouseExecuted,currentPlayer,winner
    #Freeze the screen when the game is won
    if winner is not None:
        return
    if onMouseExecuted:#If mouse click can be performed
        column = onMouse(x)#The column to drop token and the row which token can be placed
        row = searchRow(gameBoard,column)
        if row != None:
            if currentPlayer == 0:
                token = createToken(rectangleTurtles[column].xcor(),rectangleTurtles[column].ycor() + (8 - row) * 65,color1)
                currentPlayer = 1 #Switch player     
            else:
                token = createToken(rectangleTurtles[column].xcor(),rectangleTurtles[column].ycor() + (8 - row) * 65,color2)
                currentPlayer = 0
            
            canvas.update()
            updateGameBoard(column, row)
            tokenBoard[row][column] = token
            checkWinner(column,row)
            
            #Check tie
            if winner is None and checkTie(gameBoard):
                canvas.title('Tie!')
                return
            onMouseExecuted = False
        else:
            pass


def motionEventHandler(event):
    global currentPlayer
    canvas_width = turtle.getcanvas().winfo_width()
    x= turtle.getcanvas().winfo_pointerx() #Retrieve mouse coordinates
    x -= canvas_width // 2 #Convert absolute coordinates to turtle coordinates
    delayedOnMouse(x)


def __main__():
    global color1,color2
    color1,color2 = 'blue','purple'

    #Set current player to the first player. The 2 players are labled 0,1
    global currentPlayer
    currentPlayer = 0

    global canvas
    canvas = turtle.Screen()
    canvas.title('Connect-4 game')
    canvas.tracer(0)

    initBoard()
    createGame(canvas)
    
    turtle.Screen().getcanvas().bind("<Motion>",motionEventHandler)
    turtle.Screen().getcanvas().bind("<Button-1>", lambda event: onclick(event.x - canvas.window_width() // 2))
   
    turtle.mainloop()

__main__()