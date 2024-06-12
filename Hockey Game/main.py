from graphics import Canvas
import time
    
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400

def main():
    x_velocity = 5
    y_velocity = 5
    delay = 0.05
    player_1_score = 0
    player_2_score = 0

    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    # background
    canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT,"blue")
    #score
    score_display = canvas.create_text(5, 185,text = "SCORE",font = 'Arial', font_size = 30, color ='white')
    player_1_score_display = canvas.create_text(45, 80,text = str(player_1_score),font = 'Arial', font_size = 50, color ='white')
    player_2_score_display = canvas.create_text(45, 275,text = str(player_2_score),font = 'Arial', font_size = 50, color ='white')
    # controls
    player_1_display = canvas.create_text(30, 10, text = 'Player 1', font = 'Arial', font_size = 15, color = 'white')
    player_1_controls = canvas.create_text(20, 27, text = '"Q" <  > "W"', font = 'Arial', font_size = 15, color = 'white')
    player_2_display = canvas.create_text(30, CANVAS_HEIGHT -42, text = 'Player 2', font = 'Arial', font_size = 15, color = 'white')
    player_2_controls = canvas.create_text(20, CANVAS_HEIGHT -25, text = '"O" <  > "P"', font = 'Arial', font_size = 15, color = 'white')
    # field
    field_left_x = 120
    field_top_y = 10
    field_right_x = CANVAS_WIDTH - 10
    field_bottom_y = CANVAS_HEIGHT - 10 
    canvas.create_rectangle(field_left_x,field_top_y,field_right_x,field_bottom_y,"white", "black")
    #line
    canvas.create_line(120, CANVAS_HEIGHT/2 - 2, CANVAS_WIDTH - 10, CANVAS_HEIGHT/2 + 2,"black")
    #goal display
    goal_text = canvas.create_text(210, 170,text = "GOAL!!!",font = 'Arial', font_size = 30, color ='red')
    canvas.set_hidden(goal_text, True)
    # goals
    canvas.create_rectangle(215, 0, 215 + 80, 10,"white")
    canvas.create_rectangle(215, CANVAS_HEIGHT -10, 215 + 80, CANVAS_HEIGHT,"white")
    # paddles and puck
    bar_width = 60
    bar_height = 10
    bar1 = canvas.create_rectangle(225, 15, 225 + bar_width, 15 + bar_height,"orange")
    bar2 = canvas.create_rectangle(225, CANVAS_HEIGHT - 25, 225 + 60, CANVAS_HEIGHT - 15,"orange")

    puck_left_x = 250
    puck_top_y = 195
    puck_half_diameter = 10
    puck_right_x = puck_left_x + puck_half_diameter
    puck_bottom_y = puck_top_y + puck_half_diameter
    puck = canvas.create_oval(puck_left_x,puck_top_y,puck_right_x,puck_bottom_y)
    
    while True:
        # move bars 1 and 2
        movement_bar(canvas,bar1,bar2, field_left_x, field_right_x)
        # bouncing from field walls
        if (puck_left_x <= field_left_x) or (puck_right_x >= field_right_x):
            x_velocity = -x_velocity
        if (puck_top_y < field_top_y) or (puck_bottom_y >= field_bottom_y):
            y_velocity = -y_velocity
        # bouncing from bars, increasing speed.
        if touched(canvas,bar1,bar2,bar_height, bar_width) == True:
            y_velocity = -y_velocity
            delay -= 0.005
        # Checking goal player 2
        if scored(canvas) == 2:
            canvas.set_hidden(goal_text, False)
            time.sleep(0.5)
            canvas.set_hidden(goal_text, True)
            player_2_score += 1
            canvas.change_text(player_2_score_display, str(player_2_score))
            delay = 0.05
            puck_left_x = 250
            puck_top_y = 195
            puck_right_x = puck_left_x + puck_half_diameter
            puck_bottom_y = puck_top_y + puck_half_diameter
        # Checking goal player 1
        if scored(canvas) == 1:
            canvas.set_hidden(goal_text, False)
            time.sleep(0.5)
            canvas.set_hidden(goal_text, True)
            player_1_score += 1
            canvas.change_text(player_1_score_display, str(player_1_score))
            delay = 0.05
            puck_left_x = 250
            puck_top_y = 195
            puck_right_x = puck_left_x + puck_half_diameter
            puck_bottom_y = puck_top_y + puck_half_diameter
        # winning condition
        if player_1_score == 5:
            canvas.create_text(195, 170,text = "PLAYER 1",font = 'Arial', font_size = 30, color ='red')
            canvas.create_text(210, 210,text = "WINS!!!",font = 'Arial', font_size = 30, color ='red')
            break
        if player_2_score == 5:
            canvas.create_text(195, 170,text = "PLAYER 2",font = 'Arial', font_size = 30, color ='red')
            canvas.create_text(210, 210,text = "WINS!!!",font = 'Arial', font_size = 30, color ='red')
            break
        puck_left_x += x_velocity
        puck_top_y += y_velocity
        puck_right_x += x_velocity
        puck_bottom_y += y_velocity
        canvas.moveto(puck, puck_left_x, puck_top_y)
        time.sleep(delay)
        
        



# check it touches bar
def touched(canvas,bar1,bar2,bar_height, bar_width):
    bar1_left_x, bar1_top_y = canvas.coords(bar1)
    bar1_right_x = bar1_left_x + bar_width
    bar1_bottom_y = bar1_top_y + bar_height
    bar1_sensor = canvas.find_overlapping(bar1_left_x,bar1_top_y,bar1_right_x,bar1_bottom_y)

    bar2_left_x, bar2_top_y = canvas.coords(bar2)
    bar2_right_x = bar2_left_x + bar_width
    bar2_bottom_y = bar2_top_y + bar_height
    bar2_sensor = canvas.find_overlapping(bar2_left_x,bar2_top_y,bar2_right_x,bar2_bottom_y)

    if "shape_15" in bar1_sensor or "shape_15" in bar2_sensor:
        return True
    return False
      
# scored
def scored(canvas):
    goal1_sensor = canvas.find_overlapping(217,0,293,15)
    goal2_sensor = canvas.find_overlapping(217,CANVAS_HEIGHT-15,293,CANVAS_HEIGHT)
    if "shape_15" in goal1_sensor: 
        return 2
    if "shape_15" in goal2_sensor: 
        return 1

#puck = moving_puck(canvas)
def moving_puck(canvas, puck, puck_left_x, puck_top_y, puck_right_x, puck_bottom_y, field_left_x, field_top_y, field_right_x, field_bottom_y, x_velocity, y_velocity):
        if (puck_left_x <= field_left_x) or (puck_right_x >= field_right_x):
            x_velocity = -x_velocity
        if (puck_top_y < field_top_y) or (puck_bottom_y >= field_bottom_y):
            y_velocity = -y_velocity
        puck_left_x += x_velocity
        puck_top_y += y_velocity
        canvas.moveto(puck, puck_left_x, puck_top_y)
        time.sleep(0.05)

# moving bar 
def movement_bar(canvas, bar1, bar2, field_left_x, field_right_x):
    key = canvas.get_last_key_press()
    bar1_x, bar1_y = canvas.coords(bar1)
    bar2_x, bar2_y = canvas.coords(bar2)

    if key == "p":
        if bar2_x + 60 < field_right_x:
            canvas.move(bar2, 5, 0)
    if key == "o":
        if bar2_x > field_left_x:
            canvas.move(bar2, -5, 0)
    if key == "w":
        if bar1_x + 60 < field_right_x:
            canvas.move(bar1, 5, 0)
    if key == "q":
        if bar1_x > field_left_x:
            canvas.move(bar1, -5, 0)  


if __name__ == '__main__':
    main()