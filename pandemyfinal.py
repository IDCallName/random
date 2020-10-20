from graph import *
from math import fabs

import random
import datetime

dt = datetime.time()
random.seed()

amount = 120
ill_amount = 4
ded_amount = 0
healthy = amount - ill_amount
players = []
workzones = []
illness_percent = 21

ill_indicator = label(str(ill_amount) + "больных", 15, 510, font=("Arial", 28))
dead_indicator = label(" ", 25, 550, font=("Arial", 18))


graph_pos = 0

def drawGraph(number):
    if number%500 == 0:
        penColor("black")
        brushColor("red")
        coordinates = (250 + 4*(number//500),
        580 - ill_amount//2,
        (254 + 4*(number//500)),
        580
        )
        rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

        if ded_amount > 1:
            brushColor("black")
            coordinates = (250 + 4*(number//500),
            580 - ded_amount//2,
            (254 + 4*(number//500)),
            580
            )
            rectangle(coordinates[0], coordinates[1], coordinates[2], coordinates[3])

class Person:
    size = 5

class Workzone:
    def __init__(self, x, y, size_x, size_y, box):
        # Координаты рабочей территории
        self.x = x
        self.y = y

        # Индекс рабочей территории
        self.index = random.randrange(1, 65535)

        # Размеры рабочей территории
        self.size_x = size_x
        self.size_y = size_y

        # Работники
        self.workers = []

        # Коробка
        self.box = box
        
        # Взаимодействие с пандеминей
        self.disease_friendly = random.choice([True, False])
        self.goverment = random.choice([True, False, False])

        # Работают ли люди
        self.workday_started = False

        # Эмм, закрыто ли рабочее место?
        self.knockout = False
        
class Player: # Да-да, теперь у нас всё серьезно
    # Функция, которая вызывается при создании экземпляра класса
    def __init__(self, x, y, is_impostor, box, index):
        # Индекс игрока в списке
        self.index = index
        
        # Координаты игрока
        self.x = x
        self.y = y

        # Координаты дома игрока
        placeable = False

        while not placeable:
            placeable = True
            
            self.house_x = random.choice(range(0, 50))
            self.house_y = random.choice(range(0, 50))

            if self.house_x > 5 and self.house_x < 45 and self.house_y > 5 and self.house_y < 45:
                live_dice = random.choice(range(0, 50)) == 0

                if not live_dice:
                    placeable = False
            
            if self.house_x > 10 and self.house_x < 40 and self.house_y > 10 and self.house_y < 40:
                placeable = False

            for player in players:
                if self.house_x == player.house_x and self.house_y == player.house_y:
                    live_dice = random.choice(range(0, 4)) == 0

                    if not live_dice:
                        placeable = False
                        break
                        

        # Логическая переменная
        self.is_impostor = is_impostor
        self.is_dead = False
        
        self.is_standing = False
        self.is_hurry = False
        self.is_working = False
        self.is_avoiding = False

        self.is_isolating = False
        self.is_pandemy = False

        # Место работы
        if random.choice(range(0, 10000)) == 0:
            self.workzone = 0
        else:
            workzone = random.choice(workzones)
            
            self.workzone = workzone.index
            
            workzone.workers.append(index)

        # Индивидуальные параметры игрока
        self.is_dumb = random.choice([True, False])
        self.hurry_speed = random.choice([3, 4, 5])
        self.standing_cooldown = random.choice(range(10, 200))
        self.immunity = random.choice([0.5, 0.5, 0.75, 0.75, 0.75, 1, 1, 1, 1, 1, 1, 1.5, 1.5, 1.5, 2])
        self.temp_immunity = 0

        # Таймер остановки
        self.cooldown_counter = 0

        #  Точка назначения
        self.destination_x = random.choice(range(x-100, x+100))
        self.destination_y = random.choice(range(y-100, y+100))

        while self.destination_x < 0 or self.destination_x > 500-Person.size or self.destination_y < 0 or self.destination_y > 500-Person.size:
            self.destination_x = random.choice(range(x-100, x+100))
            self.destination_y = random.choice(range(y-100, y+100))

        # Привязанный квадратик
        self.box = box

def initWorld():
    penColor('black')
    brushColor("lightgray")

    rectangle(0, 0, 500, 500)

def initPlayers(amount, is_impostor):
    index = 0
    
    for person in range(amount):
        penColor("black")

        in_scary = True

        while in_scary:
            in_scary = False

            x = random.choice(range(0, 500 - Person.size, Person.size))
            y = random.choice(range(0, 500 - Person.size, Person.size))
            
            for workzone in workzones:
                overlap_x = (x >= workzone.x and x <= workzone.x + workzone.size_x) or (x+Person.size >= workzone.x and x+Person.size <= workzone.x + workzone.size_x)
                overlap_y = (y >= workzone.y and y <= workzone.y + workzone.size_y) or (y+Person.size >= workzone.y and y+Person.size <= workzone.y + workzone.size_y)
                    
                if overlap_x and overlap_y:
                    in_scary = True
                    break
        
        if is_impostor:
            brushColor("red")
        else:
            brushColor("white")

        box = rectangle(x, y, x + Person.size, y + Person.size)
        players.append(Player(x, y, is_impostor, box, index))

        index += 1

def initWorkzones():
    workzone_count = random.choice(range(2, 10))

    for i in range(workzone_count):
        placeable = False

        while not placeable:
            placeable = True
            
            size_x = random.choice(range(20, 200))
            size_y = random.choice(range(20, 200))
                
            x = random.choice(range(0, 500-size_x))
            y = random.choice(range(0, 500-size_y))

            for workzone in workzones:
                overlap_x = ((x >= workzone.x) and x <= (workzone.x + workzone.size_x)) or ((x + size_x >= workzone.x) and (x + size_x <= (workzone.x + workzone.size_x)))
                overlap_y = ((y >= workzone.y) and y <= (workzone.y + workzone.size_y)) or ((y + size_y >= workzone.y) and (y + size_y <= (workzone.y + workzone.size_y)))

                outrange_x = (x <= workzone.x) and x+size_x >= (workzone.x + workzone.size_x)
                outrange_y = (y <= workzone.y) and y+size_y >= (workzone.y + workzone.size_y)

                if (overlap_x or outrange_x) and (overlap_y or outrange_y):
                    placeable = False

        penColor("white")

        box = rectangle(x, y, x + size_x, y + size_y)
        workzones.append(Workzone(x, y, size_x, size_y, box))

def spread():
    global ill_amount

    for player1 in players:
        for player2 in players:
            # Если кто-то из двух умер, то бесполезно что-либо запускать
            dead_check = (player1.is_dead or player2.is_dead)

            if not dead_check:
                # Проверка двух условий и наличия больного
                ill_check = player1.is_impostor and not player2.is_impostor

                standing_check = (player1.is_standing or player2.is_standing) and not (player1.is_standing and player2.is_standing)
                hurry_check = (player1.is_hurry or player2.is_hurry) and not (player1.is_hurry and player2.is_hurry)
                cooldown_check = (player1.cooldown_counter > 0 or player2.cooldown_counter > 0)

                if player1.is_isolating:
                    ill_dice = random.choice(range(0, int(1500*(player2.immunity + player2.temp_immunity/10000)))) == 0
                else:
                    ill_dice = random.choice(range(0, int(150*(player2.immunity + player2.temp_immunity/10000)))) == 0
                    
                communication_ill_dice = random.choice(range(0, int(3*(player2.immunity + player2.temp_immunity/10000)))) == 0
                
                standing_dice = random.choice(range(0, 10)) == 0

                if (fabs(player1.x - player2.x) <= Person.size*2 and fabs(player1.y - player2.y) <= Person.size*2) and ill_check and ill_dice:
                    # Бьём вслепую
                    changeFillColor(player1.box, "red")
                    changeFillColor(player2.box, "red")
                    player1.is_impostor = True
                    player2.is_impostor = True
                    
                    ill_amount += 1

                # Давайте добавим взаимодействие между людьми
                if (fabs(player1.x - player2.x) <= 3 * Person.size and fabs(player1.y - player2.y) <= 3 * Person.size) and not hurry_check and not cooldown_check and standing_check and standing_dice:
                    player1.is_standing = True
                    player2.is_standing = True

                    # Не здоровайтесь за руки
                    if ill_check and communication_ill_dice:
                        changeFillColor(player1.box, "red")
                        changeFillColor(player2.box, "red")
                        player1.is_impostor = True
                        player2.is_impostor = True
                        
                        ill_amount += 1

def drawLabel(ill_amount, ded_amount):
    global ill_indicator, dead_indicator
    
    if (str(ill_amount)[-1] == '1' and (len(str(ill_amount)) > 1 and str(ill_amount)[-2] != '1')) or ill_amount == 1:
        ill_txt = ' больной'
    else:
        ill_txt = ' больных'

    if (str(ded_amount)[-1] == '1' and (len(str(ded_amount)) > 1 and str(ded_amount)[-2] != '1')) or ded_amount == 1:
        ded_txt = ' погибший'
    else:
        ded_txt = ' погибших'
    
    if ded_amount == 0:
        ill_indicator['text'] = (str(ill_amount) + ill_txt)
    else:
        ill_indicator['text'] = (str(ill_amount) + ill_txt)
        dead_indicator['text'] = (str(ded_amount) + ded_txt)

def updatePlayers():
    global ded_amount, ill_amount

    for player in players:
        player.cooldown_counter -= 1

        if (player.x >= player.house_x*10 and player.x < player.house_x*10+10-Person.size) and (player.y >= player.house_y*10 and player.y < player.house_y*10+10-Person.size) and player.is_isolating:
            if not player.is_impostor:
                changeFillColor(player.box, "lime")
            else:
                changeFillColor(player.box, "orange")
        else:
            if not player.is_impostor:
                changeFillColor(player.box, "white")
            else:
                changeFillColor(player.box, "red")
        
        
        if player.temp_immunity > 0:
            player.temp_immunity -= 1

        if player.is_impostor:
            cure_dice = random.choice(range(0, int(20000/(player.immunity + player.temp_immunity/10000)))) == 0

            if cure_dice:
                changeFillColor(player.box, "white")
                player.is_impostor = False

                if not player.is_pandemy:
                    player.is_isolating = False

                player.temp_immunity = player.immunity*20000

                ill_amount -= 1
            
            death_dice = random.choice(range(0, int(30000*(player.immunity + player.temp_immunity/10000)))) == 0

            if death_dice:
                changeFillColor(player.box, "black")
                player.is_dead = True
                player.is_standing = False
                player.is_impostor = False

                ded_amount += 1


            if not player.is_dumb:
                isolation_dice = random.choice(range(0, 500)) == 0

                if isolation_dice:
                    player.is_isolating = True
                    player.is_hurry = False

                

def workzoneTick():
    for workzone in workzones:
        if not workzone.knockout:
            # Проверка рабочих
            worker_count = len(workzone.workers)
            impostor_count = 0
            dead_count = 0
            
            for player_id in workzone.workers:
                player = players [player_id]
                
                if player.is_impostor or player.is_dead:
                    impostor_count += 1
                if player.is_dead:
                    dead_count += 1

            close_condition_1 = workzone.disease_friendly and not workzone.goverment and ((impostor_count / worker_count) > 0.5)
            close_condition_2 = not workzone.disease_friendly and not workzone.goverment and ((dead_count / worker_count) > 0.5)
            close_condition_3 = workzone.goverment and (worker_count == dead_count)

            if close_condition_1 or close_condition_2 or close_condition_3:
                changePenColor(workzone.box, "red")
                workzone.knockout = True
                workzone.workday_started = False

                for player_id in workzone.workers:
                    worker = players[player_id]

                    if not worker.is_dumb:
                        player.is_hurry = False
                        
                        worker.is_isolating = True
                        worker.is_pandemy = True
            
            # Рабочий день
            workday_dice = random.choice(range(0, 400)) == 0

            if workday_dice:
                if not workzone.workday_started:
                    workzone.workday_started = True
                    changePenColor(workzone.box, "green")
                else:
                    workzone.workday_started = False
                    changePenColor(workzone.box, "white")

            
            if workzone.workday_started:
                for player_id in workzone.workers:
                    worker = players[player_id]

                    worker.is_hurry = False

                    if (worker.destination_x < workzone.x or (worker.destination_x > workzone.x + workzone.size_x)) and not player.is_isolating:
                        worker.destination_x = random.choice(range(workzone.x, workzone.x + workzone.size_x))

                    if (worker.destination_y < workzone.y or (worker.destination_y > workzone.y + workzone.size_y)) and not player.is_isolating:
                        worker.destination_y = random.choice(range(workzone.y, workzone.y + workzone.size_y))
            
            

def movePlayers():
    for player in players:
        if not player.is_dead:
            if not player.is_standing:
                old_x = player.x
                old_y = player.y
    
                # Извлекаем данные о направлении движения
                dest_x = player.destination_x
                dest_y = player.destination_y

                # Ведём игрока к точке назначения
                if old_x == dest_x and old_y == dest_y:
                    if not player.is_working:
                        if random.choice(range(0, 10)) == 0 and not player.is_isolating:
                            player.is_hurry = True
                            
                            player.destination_x = random.choice(range(0, 500 - Person.size, player.hurry_speed)) + player.x % player.hurry_speed
                            player.destination_y = random.choice(range(0, 500 - Person.size, player.hurry_speed)) + player.y % player.hurry_speed
                        else:
                            if not player.is_isolating:
                                player.is_hurry = False
                                
                                player.destination_x = random.choice(range(int(player.x)-100, int(player.x)+100))
                                player.destination_y = random.choice(range(int(player.y)-100, int(player.y)+100))
        
                                while player.destination_x < 0 or player.destination_x > 500-Person.size or player.destination_y < 0 or player.destination_y > 500-Person.size:
                                    player.destination_x = random.choice(range(int(player.x-100), int(player.x+100)))
                                    player.destination_y = random.choice(range(int(player.y-100), int(player.y+100)))

                            else:
                                is_hurry = False
                                
                                player.destination_x = random.choice(range(player.house_x*10, int(player.house_x*10+10-Person.size)))
                                player.destination_y = random.choice(range(player.house_y*10, int(player.house_y*10+10-Person.size)))
    
                        if random.choice(range(0, 4)) == 0 and player.cooldown_counter <= 0:
                            player.is_standing = True

                        change_x = 0
                        change_y = 0
                    else:
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
            else:
                if random.choice(range(0, 50)) == 0:
                    player.is_standing = False
                    player.cooldown_counter = player.standing_cooldown
            
                old_x = player.x
                old_y = player.y

                change_x = 0
                change_y = 0

            # Двигаем коробку

            if player.is_hurry == True:
                change_x *= player.hurry_speed
                change_y *= player.hurry_speed

            player.x = old_x + change_x
            player.y = old_y + change_y

            moveObjectTo(player.box, player.x, player.y) # Точка назначения не должна выходить за рамки, так что пусть пока будет без проверки пересечения границ игрового поля.

def update():
    global graph_pos
    graph_pos += 1
    drawGraph(graph_pos)

    workzoneTick()
    updatePlayers()
    movePlayers()
    spread()
    
    drawLabel(ill_amount, ded_amount)

onTimer(update, 10)

initWorld()
initWorkzones()
initPlayers(healthy, False)
initPlayers(ill_amount, True)
run()
