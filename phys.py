from graph import *

radius = 10
start_point_X = radius/2 
start_point_Y = 0
acceleration_Y = 3
acceleration_X = 0.1
velocity_X = 10
velocity_Y = 0

started = False

brushColor("blue")
rectangle(0, 0, 500, 600)

brushColor("yellow")
penColor("yellow")
arrow = polygon([
        (start_point_X, start_point_Y),
        (start_point_X + 20, start_point_Y + radius),
        (start_point_X, start_point_Y + 2*radius),
        ])

ball = circle(start_point_X - radius - 10, start_point_Y + radius, radius)

def getCoordinates_X(old_X):
    global velocity_X
    if old_X + velocity_X >= 500 - radius:
        velocity_X = -velocity_X
        return old_X + velocity_X
    else:
        return old_X + velocity_X


def getCoordinates_Y(old_Y):
    global velocity_Y
    global velocity_X
    if old_Y + velocity_Y <= 500 - radius:    
        velocity_Y += acceleration_Y
        return old_Y + velocity_Y
    else:
        velocity_Y = -velocity_Y
        '''
        if velocity_X > 0:
            velocity_X -= acceleration_X
        elif velocity_X < 0:
            velocity_X += acceleration_X
        '''
        velocity_Y += acceleration_Y
        return old_Y + velocity_Y


def keyPressed(event):
    global started
    global start_point_Y
    global start_point_X
    if not started:
        if event.keycode == VK_DOWN:
            if start_point_Y < 500 - radius:
                start_point_Y += 2*radius
                choose(start_point_Y)

        if event.keycode == VK_UP:
            if start_point_Y > radius:
                start_point_Y -= 2*radius
                choose(start_point_Y)

        if event.keycode == VK_RETURN:
            started = True
            deleteObject(arrow)
    else:
        if event.keycode == VK_ESCAPE:
            close()
def choose(start_point_Y):
    global ball
    penColor("yellow")
    brushColor("yellow")
    moveObjectTo(arrow, start_point_X, start_point_Y)
    deleteObject(ball)
    ball = circle(start_point_X - radius - 10, start_point_Y + radius, radius)

def moveBall():
    if started:
        old_X = xCoord(ball) + radius
        old_Y = yCoord(ball) + radius
        new_X = getCoordinates_X(old_X)
        new_Y = getCoordinates_Y(old_Y)
        moveObjectTo(ball, new_X, new_Y)

onTimer(moveBall, 30)
onKey(keyPressed)
run()