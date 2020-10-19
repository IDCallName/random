from graph import *
from math import fabs

import random
import datetime

dt = datetime.time()
random.seed(dt.microsecond)

amount = 120
ill_amount = 2
healthy = amount - ill_amount
players = []
illness_percent = 21

graph_pos = 0

def drawGraph(number):
    if number%20 == 0:
        penColor("black")
        brushColor("red")
        coordinates = (250 + 4*(number//20),
        580 - ill_amount//2,
        (254 + 4*(number//20)),
        580
        )
        rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

class Person:
    size = 5

class Player: # Да-да, теперь у нас всё серьезно
    # Функция, которая вызывается при создании экземпляра класса
    def __init__(self, x, y, is_impostor, box):
        # Координаты игрока
        self.x = x
        self.y = y

        # Логическая переменная
        self.is_impostor = is_impostor

        #  Точка назначения
        self.destination_x = random.choice(range(0, 500 - Person.size, Person.size))
        self.destination_y = random.choice(range(0, 500 - Person.size, Person.size))

        # Привязанный квадратик
        self.box = box

def initWorld():
    penColor('black')
    brushColor("lightgray")

    rectangle(0, 0, 500, 500)

def initPlayers(amount, is_impostor): 
    for person in range(amount):
        x = random.choice(range(0, 500 - Person.size, Person.size))
        y = random.choice(range(0, 500 - Person.size, Person.size))
        penColor("black")

        if is_impostor:
            brushColor("red")
        else:
            brushColor("white")

        box = rectangle(x, y, x + Person.size, y + Person.size)
        players.append(Player(x, y, is_impostor, box))

def spread():
    global ill_amount

    for player1 in players:
        for player2 in players:
            # Проверка расстояния между человечками и наличия больного
            ill_check = (player1.is_impostor or player2.is_impostor) and not (player1.is_impostor and player2.is_impostor)
            
            if (fabs(player1.x - player2.x) <= Person.size and fabs(player1.y - player2.y) <= Person.size) and ill_check:
                # Бьём вслепую
                changeFillColor(player1.box, "red")
                changeFillColor(player2.box, "red")
                player1.is_impostor = True
                player2.is_impostor = True
                    
                ill_amount += 1

def drawLabel(ill_amount):
    if str(ill_amount)[-1] == '1' and str(ill_amount)[-2] != '1':
        ill_txt = ' больной'
    else:
        ill_txt = ' больных'
    ill_indicator = label(str(ill_amount) + ill_txt, 20, 530, font=("Arial", 28))

def movePlayers():
    for player in players:
        old_x = player.x
        old_y = player.y

        # Извлекаем данные о направлении движения
        dest_x = player.destination_x
        dest_y = player.destination_y

        # Ведём игрока к точке назначения
        if old_x == dest_x and old_y == dest_y:
            player.destination_x = random.choice(range(0, 500 - Person.size, Person.size))
            player.destination_y = random.choice(range(0, 500 - Person.size, Person.size))

            change_x = 0
            change_y = 0
        elif old_x == dest_x:
            change_y = fabs(dest_y-old_y) / (dest_y-old_y) # fabs - это модуль числа, если что. Если координата точки назначения меньше координаты человека, то его смещение должно равняться -1, что тут и делается. Я не хочу использовать if-конструкции, они будут слишком большими и их будет очень много.
            change_x = 0
        elif old_y == dest_y:
            change_x = fabs(dest_x-old_x) / (dest_x-old_x)
            change_y = 0
        else:
            change_x = fabs(dest_x-old_x) / (dest_x-old_x)
            change_y = fabs(dest_y-old_y) / (dest_y-old_y)

            # Сохраняем каноничное движение только в одной оси координат за шаг при помощи классического броска монетки :3
            coin_toss = random.choice([True, False])

            if coin_toss:
                change_x = 0
            else:
                change_y = 0

        # Двигаем коробку
        player.x = old_x + change_x
        player.y = old_y + change_y

        moveObjectTo(player.box, player.x, player.y) # Точка назначения не должна выходить за рамки, так что пусть пока будет без проверки пересечения границ игрового поля.

def update():
    global graph_pos
    graph_pos += 1
    drawGraph(graph_pos)
    movePlayers()
    spread()
    drawLabel(ill_amount)

onTimer(update, 50)

initWorld()
initPlayers(healthy, False)
initPlayers(ill_amount, True)
run()
