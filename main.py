from graph import *
from PIL import Image

image = Image.open('yarik.bmp')
WIDTH = image.size[0]
HEIGHT = image.size[1]
pix = image.load()

SIZE = 10

DEF_GRAPH_WIDTH = WIDTH
DEF_GRAPH_HEIGHT = HEIGHT
SIZE = 8
windowSize(SIZE*WIDTH, SIZE*HEIGHT)
canvasSize(SIZE*WIDTH, SIZE*HEIGHT)

def drawOneRect(x, y, rotated):
    global SIZE

    if rotated:
        polygon([
                (x, y),
                (x, y + SIZE),
                (x + SIZE, y),
                (x + SIZE, y + SIZE)
            ])
    else:
        polygon([
                (x, y),
                (x + SIZE, y),
                (x, y + SIZE),
                (x + SIZE, y + SIZE)
            ])

def draw(level, amount):
    rotated = False
    for i in range(level):
        for j in range(amount):
            red = pix[i, j][0]
            green = pix[i, j][1]
            blue = pix[i, j][2]

            penColor(red, green, blue)
            brushColor(red, green, blue)

            drawOneRect(SIZE * i, SIZE * j, rotated)
            rotated = not rotated
        rotated = not rotated

draw(WIDTH, HEIGHT)
run()
