import turtle,random,math,time
from functools import partial

g_screen = None
g_snake = None
g_monster = None
g_snake_sz = 5 #Initial body size
g_snake_speed = 200
g_intro = None #Store the introduction words before game starts:'Click anywhere to start the game'
g_keypressed = None
g_status = None 
g_paused = False
win = 'pending'
g_elapsed_time = 0
g_last_time = 0 #Time of the last direction change.
g_snake_body = []
food_list = []
contact = 0
monsterStop = False

BORDER_LEFT = -250
BORDER_RIGHT = 250
BORDER_TOP = 210
BORDER_BOTTOM = -290

COLOR_BODY = ("blue", "black")
COLOR_HEAD = "red"
COLOR_MONSTER = "purple"
FONT = ("Arial",16,"normal")

KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, KEY_SPACE = \
       "Up", "Down", "Left", "Right", "space"

HEADING_BY_KEY = {KEY_UP:90, KEY_DOWN:270, KEY_LEFT:180, KEY_RIGHT:0}

def configurePlayArea():

    # motion border
    m = createTurtle(0,0,"","black")
    m.shapesize(25,25,5)
    m.goto(0,-40)  # shift down half the status

    # status border 
    s = createTurtle(0,0,"","black")
    s.shapesize(4,25,5)
    s.goto(0,250)  # shift up half the motion

    # introduction
    intro = createTurtle(-200,150)
    intro.hideturtle()
    intro.write("Click anywhere to start the game .....", font=("Arial",16,"normal"))
    
    # statuses
    status = createTurtle(0,0,"","black")
    status.hideturtle()
    status.goto(-200,s.ycor()) 

    return intro, status

def configScreen():
    s = turtle.Screen()
    s.tracer(0)    # disable auto screen refresh, 0=disable, 1=enable
    s.title("Snake game")
    s.setup(500+120, 500+120+80)
    s.mode("standard")
    return s

def createTurtle(x, y, color="red", border="black", textcolor="black"):
    t = turtle.Turtle("square")
    t.color(border, color)
    t.up()
    t.goto(x, y)
    t.textcolor = textcolor 
    return t


def createFood():
    for i in range(1, 6):
        #Use '//20' and 'y+10' s.t. food items are aligned to match to the center position of the snake  
        x = random.randint((BORDER_LEFT + 30) // 20, (BORDER_RIGHT - 30) // 20) * 20
        y = random.randint((BORDER_BOTTOM + 30) // 20, (BORDER_TOP - 30) // 20) * 20

        food = createTurtle(x, y+10, color="", border="", textcolor="black")
        food.num = i  
        food.is_written = True  
        food.color(food.textcolor) 
        food.write(i, font=("Arial", 16, "bold"),align = 'center')
        food.color("", "") 
        food.hideturtle()
        food_list.append(food)


def updateStatus():
    global food_list,g_elapsed_time,contact,g_monster
    g_status.clear()

    # Update the position of 'motion' text
    g_status.goto(50, g_status.ycor()) 
    if g_paused == True:
        g_status.write(f'Motion:paused', font=('arial',15,'bold'))
    else:
        g_status.write(f'Motion:{g_keypressed}', font=('arial',15,'bold'))
    
    # Update the position of 'timer' text
    g_status.goto(-50, g_status.ycor())
    g_status.write(f"Time: {g_elapsed_time}", font=('arial', 15, 'bold'))

    # Update the position of 'contact' text
    g_status.goto(-200, g_status.ycor())
    g_status.write(f"Contact: {contact}", font=('arial', 15, 'bold'))

    g_screen.update()


def checkContact():
    global contact, g_monster, g_status
    if monsterStop == False and win != 'Won':
        #Use try-except to avoid possible errors
        try:
            for body in g_snake_body:
                if (g_monster.xcor() - body[0]) ** 2 + (g_monster.ycor() - body[1]) ** 2 <= 400:
                    contact += 1    
        except:
            pass
       
    updateStatus()
    g_screen.ontimer(checkContact, 1000)


#Function to randomly hide and unhide food items
def toggleFoodVisibility():
    if not monsterStop and not g_paused:
        if len(food_list) > 0:
            food = random.choice(food_list)
            if food.is_written:  # If food is visible, hide it
                food.clear()  
                food.is_written = False
            else:
                food.color(food.textcolor)
                food.write(food.num, font=("Arial", 16, "bold"))  # Unhide number
                food.color("", "")  
                food.is_written = True

        g_screen.update()
        g_screen.ontimer(toggleFoodVisibility, random.randint(1000,5000))  # 1 to 5 seconds


def setSnakeHeading(key):
    global g_keypressed, g_last_time, g_paused

    current_time = time.time()
    # Set the threshold to 100 milliseconds to avoid frequent direction changes.
    if current_time - g_last_time < 0.1:  
        return

    if key in HEADING_BY_KEY.keys():
        new_heading = HEADING_BY_KEY[key]
        
        # Limit the snake to move only in the direction perpendicular to the current direction.
        if abs(new_heading - g_snake.heading()) != 180:
            g_snake.setheading(new_heading)

            # Calculate the expected movement position
            next_x = g_snake.xcor() + 20 * math.cos(math.radians(new_heading))
            next_y = g_snake.ycor() + 20 * math.sin(math.radians(new_heading))

            # Check whether the border has been crossed
            if BORDER_LEFT <= next_x <= BORDER_RIGHT and BORDER_BOTTOM <= next_y <= BORDER_TOP:
                g_keypressed = key
                updateStatus()

                # Update time of the last direction change.
                g_last_time = current_time
        else:
            g_paused = True


def onArrowKeyPressed(key):
    global g_keypressed,g_paused

    if key == KEY_SPACE:
        g_paused = not g_paused

    # While paused, pressing any of the four arrow keys will un-pause
    elif g_paused and key != KEY_SPACE:
        g_keypressed = key
        setSnakeHeading(key)
        updateStatus()
        g_paused = not g_paused

    else:
        g_keypressed = key
        setSnakeHeading(key)
        updateStatus()




def checkCollision():
    global g_snake_speed,g_snake_sz,food_list,win,slow
    for food in food_list:
        if g_snake.distance(food) < 15 and food.is_written:  # Food can only be consumed if it is visible
            food.clear()
            food_list.remove(food)
            g_snake_sz += food.num
            g_snake_speed = 250 #Slow down snake speed when eating
            break

    if len(g_snake_body) >= 20: #If won
        g_snake.color(COLOR_HEAD)
        g_snake.write("Winner!!", font=("Arial", 16, "bold"), align='left')

        g_screen.update()  
        win = 'Won'
        turtle.mainloop()  # Freeze screen


def onTimerSnake():
    global g_snake_speed,g_snake_body,g_paused,g_elapsed_time,g_start_time,win,monsterStop,contact

    if win == 'pending':# If haven't won
        if g_snake.distance(g_monster) < 20:
            #Use another turtle to write s.t. words won't be covered by snake head
            writeTurtle = turtle.Turtle()
            writeTurtle.penup()
            writeTurtle.hideturtle()
            writeTurtle.color('purple')
            writeTurtle.goto(g_monster.xcor() - 30,g_monster.ycor() + 20)
            writeTurtle.write("Game Over!!", font=("Arial", 16, "bold"), align='left')

            monsterStop = True
            contact += 1
            turtle.done()
            return
 
        if not g_paused:
            if g_keypressed == None:
                g_screen.ontimer(onTimerSnake, g_snake_speed)
                return

            next_x = round(g_snake.xcor() + 20 * math.cos(math.radians(g_snake.heading())))
            next_y = round(g_snake.ycor() + 20 * math.sin(math.radians(g_snake.heading())))
            next_pos = (next_x, next_y)

            
            if next_pos in g_snake_body:
                # Head collides with its body and cannot move in that direction
                # Set a new timer to keep the snake still in place
                g_screen.ontimer(onTimerSnake, g_snake_speed)  
                return

            if BORDER_LEFT <= next_x <= BORDER_RIGHT and BORDER_BOTTOM <= next_y <= BORDER_TOP:
                # Clone the head as body
                g_snake.color(*COLOR_BODY)
                g_snake.stamp()
                g_snake_body.append((round(g_snake.xcor()), round(g_snake.ycor())))


                g_snake.color(COLOR_HEAD)

                # Advance snake
                g_snake.forward(20)

                # Shifting or extending the tail.
                # Remove the last square on Shifting.
                while len(g_snake.stampItems) > g_snake_sz:
                    try:
                        g_snake_speed = 200
                        g_snake_body.pop(0)
                    except:
                        pass
                    g_snake.clearstamps(1)

            else:
                # Stops moving when hits the boundary.Waits for a direction change operation
                pass

            checkCollision()
            g_screen.update()
        g_screen.ontimer(onTimerSnake, g_snake_speed)



def onTimerMonster():
    if monsterStop == False and win != 'Won':
        snake_head_pos = (round(g_snake.xcor()), round(g_snake.ycor()))# Use 'round' to avoid errors
        monster_pos = (round(g_monster.xcor()), round(g_monster.ycor()))

        # The monster moves towards the snake in horizontal/vertical directions
        dx, dy = snake_head_pos[0] - monster_pos[0], snake_head_pos[1] - monster_pos[1]
        if abs(dx) >= abs(dy):
            heading = 0 if dx > 0 else 180
        else:
            heading = 90 if dy > 0 else 270

        original_y = g_monster.ycor()

        next_x = g_monster.xcor() + 20 * math.cos(math.radians(heading))
        next_y = g_monster.ycor() + 20 * math.sin(math.radians(heading))

        if BORDER_LEFT <= next_x <= BORDER_RIGHT and BORDER_BOTTOM <= next_y <= BORDER_TOP:
            # First moves horizontally then moves vertically
            g_monster.goto(next_x,original_y)
            g_monster.goto(g_monster.xcor(),next_y)
            
        g_screen.update()
        
        monster_speed = random.randint(270,400)  # Randomize monster speed
        g_screen.ontimer(onTimerMonster, monster_speed)

#Initial monster position
def randomMonsterPosition():
    while True:
        x = random.randint((BORDER_LEFT + 30) // 20, (BORDER_RIGHT - 30) // 20) * 20
        y = random.randint((BORDER_BOTTOM + 30) // 20, (BORDER_TOP - 30) // 20) * 20
        if abs(x - g_snake.xcor()) >= 100 and abs(y - g_snake.ycor()) >= 100: # Monster has to be in fair distance
            # with snake head
            return x, y


def updateElapsedTime():
    global g_elapsed_time, g_start_time
    if win == 'pending':
        g_elapsed_time = int(time.time() - g_start_time)
        updateStatus()
        if monsterStop == True:
            return
        g_screen.ontimer(updateElapsedTime, 100)  # Update once 100 milliseconds


def startGame(x,y):
    global g_start_time
    g_start_time = time.time()
    g_screen.ontimer(updateElapsedTime, 100)
    g_screen.onscreenclick(None) #We no longer need to response to screen clicks, so set to None
    g_intro.clear()
    createFood()
    toggleFoodVisibility()


    g_screen.onkey(partial(onArrowKeyPressed,KEY_UP), KEY_UP)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_DOWN), KEY_DOWN)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_LEFT), KEY_LEFT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_RIGHT), KEY_RIGHT)
    g_screen.onkey(partial(onArrowKeyPressed,KEY_SPACE), KEY_SPACE)

    g_screen.ontimer(onTimerSnake, 100)
    g_screen.ontimer(onTimerMonster, 1000)

if __name__ == "__main__":
    g_screen = configScreen()
    g_intro, g_status = configurePlayArea()

    
    updateStatus()
    checkContact()

    g_snake = createTurtle(0,0,"red", "black")

    #Set the monster at a random position with a fair distance from the snake before the game starts
    monster_x, monster_y = randomMonsterPosition()
    g_monster = createTurtle(monster_x + 10,monster_y + 10,"purple", "black")

    

    g_screen.onscreenclick(startGame)

    g_screen.update()
    g_screen.listen()
    g_screen.mainloop()