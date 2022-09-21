import random

class Ocean:

    def __init__(self, width=10, height=10):
        self.ocean = [["~" for i in range(width)] for i in range(height)]

    def __getitem__(self, point):
        row, col = point
        return self.ocean[row][col]

    def __setitem__(self, point, value):
        row, col = point
        self.ocean[row][col] = value

    def view_ocean(self):
        for row in self.ocean:
            print(" ".join(row))


    def valid_col(self, row):
        try:
            self.ocean[row]
            return True
        except IndexError:
            return False

    def valid_row(self, col):
        try:
            self.ocean[0][col]
            return True
        except IndexError:
            return False


    def can_use_col(self, row, col, size):

        valid_coords = []

        for i in range(size):

            if self.valid_col(col) and self.valid_row(row):
                if self.ocean[row][col] == "~":
                    valid_coords.append((row, col))
                    col = col + 1
                else:
                    col = col + 1
            else:
                return False

        if size == len(valid_coords):
            return True
        else:
            return False

    def can_use_row(self, row, col, size):

        valid_coords = []

        for i in range(size):

            if self.valid_row(row) and self.valid_col(col):
                if self.ocean[row][col] == "~":
                    valid_coords.append((row, col))
                    row = row + 1
                else:
                    row = row + 1
            else:
                return False

        if size == len(valid_coords):
            return True
        else:
            return False


    def set_ship_col(self, row, col, size):
        for i in range(size):
            self.ocean[row][col] = "S"
            col = col + 1

    def set_ship_row(self, row, col, size):
        for i in range(size):
            self.ocean[row][col] = "S"
            row = row + 1

class Radar:

    def __init__(self, width=10, height=10):
        self.radar = [["." for i in range(width)] for i in range(height)]

    def __getitem__(self, point):
        row, col = point
        return self.radar[row][col]

    def __setitem__(self, point, value):
        row, col = point
        self.radar[row][col] = value

    def view_radar(self):
        for row in self.radar:
            print(" ".join(row))

class Ship:

    def __init__(self, ship_type, size):
        self.ship_type = ship_type
        self.size = size
        self.coords = []

    def plot_vertical(self, row, col):
        for i in range(self.size):
            self.coords.append((row, col))
            row = row + 1

    def plot_horizontal(self, row, col):
        for i in range(self.size):
            self.coords.append((row, col))
            col = col + 1

    def check_status(self):
        if self.coords == []:
            return True
        else:
            return False

class Player:

    ships = {"Авианосец": 5, "Крейсер": 4, "Эсминец": 3,
"Миноносец": 2}

    def __init__(self, name):
        self.ocean = Ocean()
        self.radar = Radar()
        self.name = name
        self.fleet = []


    def set_fleet(self):
        print("Выберите координаты между 0 и 9 для строк и столбцов на вашем поле")
        print("Суда размещаются справа налево")
        for ship, size in self.ships.items():

            flag = True
            while flag:
                self.view_console()
                try:
                    print("Разместите ваш %s" % (ship))
                    row = int(input("Выберите строку -----> "))
                    col = int(input("Выберите столбец -----> "))
                    orientation = str(input("По вертикали или горизонтали? (введите в or г) -----> "))

                    if orientation in ["в", "В"]:
                        if self.ocean.can_use_row(row, col, size):
                            self.ocean.set_ship_row(row, col, size)
                            boat = Ship(ship, size)
                            boat.plot_vertical(row, col)
                            self.fleet.append(boat)
                            flag = False
                        else:
                            print("Суда размещены друг на друге. Так не пойдёт, попробуйте ещё раз.")

                    elif orientation in ["г", "Г"]:
                        if self.ocean.can_use_col(row, col, size):
                            self.ocean.set_ship_col(row, col, size)
                            boat = Ship(ship, size)
                            boat.plot_horizontal(row, col)
                            self.fleet.append(boat)
                            flag = False
                        else:
                            print("Суда размещены друг на друге. Так не пойдёт, попробуйте ещё раз.")

                    else:
                        continue

                    self.view_console()

                except ValueError:
                    print("Вы что, читать не умеете? \n Введите номер!\n")

    def view_console(self):
        self.radar.view_radar()
        print("|                 |")
        self.ocean.view_ocean()


    def register_hit(self, row, col):
        for boat in self.fleet:
            if (row, col) in boat.coords:
                boat.coords.remove((row, col))
                if boat.check_status():
                    self.fleet.remove(boat)
                    print("%s %s утонул!" % (self.name, boat.ship_type))


    def strike(self, target):
        self.view_console()
        try:
            print("\n%s Выбирай цель!" % (self.name))
            row = int(input("Выбери строку -----> "))
            col = int(input("Выбери столбец -----> "))

            if self.ocean.valid_row(row) and self.ocean.valid_col(col):
                if target.ocean.ocean[row][col] == "S":
                    print("Прямое попадание!")
                    target.ocean.ocean[row][col] = "X"
                    target.register_hit(row, col)
                    self.radar.radar[row][col] = "X"

                else:
                    if self.radar.radar[row][col] == "O":
                        print("В эту клетку уже стреляли... Внимательно посмотрите на поле!")
                        self.strike(target)
                    else:
                        print("Мимо...")
                        self.radar.radar[row][col] = "O"

            else:
                print("Вы ввели координаты вне поля боя.")
                self.strike(target)

        except ValueError:
            print("Нужно ввести номер!....\n")
            self.strike(target)

class Computer(Player):

    def __init__(self):
        super().__init__(self)
        self.name = "Великий компьютерный стратег"


    def set_compu_fleet(self):
        positions = ["в", "г"]

        for ship, size in self.ships.items():

            flag = True
            while flag:
                row = random.randint(0, 9)
                col = random.randint(0, 9)
                orientation = random.choice(positions)

                if orientation == "в":
                    if self.ocean.can_use_row(row, col, size):
                        self.ocean.set_ship_row(row, col, size)
                        boat = Ship(ship, size)
                        boat.plot_vertical(row, col)
                        self.fleet.append(boat)
                        flag = False

                    else:
                        row = row + 2

                elif orientation == "г":
                    if self.ocean.can_use_col(row, col, size):
                        self.ocean.set_ship_col(row, col, size)
                        boat = Ship(ship, size)
                        boat.plot_horizontal(row, col)
                        self.fleet.append(boat)
                        flag = False

                    else:
                        col = col + 2

                else:
                    continue


    def compu_strike(self, target):
        row = random.randint(0, 9)
        col = random.randint(0, 9)

        if self.radar.radar[row][col] == ".":
            print("...Цель выбрана....%s, %s" % (row, col))

            if target.ocean.ocean[row][col] == "S":
                print("Прямое попадание!")
                target.ocean.ocean[row][col] = "X"
                target.register_hit(row, col)
                self.radar.radar[row][col] = "X"

            else:
                target.ocean.ocean[row][col] = "0"
                print("Промахнулся....Прицеливаюсь повторно!")


        else:
            self.compu_strike(target)

class BattleshipsPVP:
    def __init__(self):
        start = input("Начнём? (д или н) -----> ")
        if start in ["д", "Д"]:
            self.playPVP()
        else:
            print("Завершаем сессию...")

    def playPVP(self):
        p1name = input("Первый игрок, задайте своё имя! -----> ")
        p1 = Player(p1name)
        p1.set_fleet()
        p1.view_console()
        self.clear_screen()

        p2name = input("\n\nВторой игрок, задайте своё имя! -----> ")
        p2 = Player(p2name)
        p2.set_fleet()
        p2.view_console()
        self.clear_screen()

        flag = True
        while flag is True:
            p1.strike(p2)
            if self.fleet_sunk(p2) is True:
                self.victory_message(p1, p2)
                flag = False
            else:
                self.clear_screen()

                p2.strike(p1)
                if self.fleet_sunk(p1) is True:
                    self.victory_message(p2, p1)
                    flag = False
                else:
                    self.clear_screen()
        print("\nСпасибо за игру!")


    def fleet_sunk(self, player):
        ship_counters = 0
        """Traverses grid looking for 's' counters"""
        for row in range(len(player.ocean.ocean)):
            for col in range(len(player.ocean.ocean)):
                if player.ocean.ocean[row][col] == "S":
                    ship_counters += 1
        if ship_counters == 0:
            return True
        else:
            return False

    def clear_screen(self):
        print("\nСледующий ход?")


    def victory_message(self, winner, loser):
        print("\n\n\n*****************************************")
        print("Флот игрока %s был разгромлен! Игрок %s победил!" % (loser.name, winner.name))
        print("*****************************************")

class BattleshipsCOMP(BattleshipsPVP):

    def __init__(self):
        start = input("Начнём? (д или н) -----> ")
        if start in ["д", "Д"]:
            self.playCOMP()
        else:
            print("Завершаем сессию...")

    def playCOMP(self):
        pname = input("Первый игрок, задайте своё имя! -----> ")
        p = Player(pname)
        p.set_fleet()
        p.view_console()
        self.clear_screen()

        c = Computer()
        print("Компьютер расставляет свой флот...")
        c.set_compu_fleet()
        self.clear_screen()

        flag = True
        while flag is True:
            p.strike(c)
            if self.fleet_sunk(c) is True:
                self.victory_message(p, c)
                flag = False
            else:
                self.clear_screen()

                c.compu_strike(p)
                if self.fleet_sunk(p) is True:
                    self.victory_message(c, p)
                    flag = False
                else:
                    self.clear_screen()
        print("\nСпасибо за игру!")

def playbattleships():
    print("\n\n***********************")
    print("Добро пожаловать в Морской бой!")
    print("***********************\n")

    print("\n 1) Режим против живого игрока")
    print("\n 2) Игрок против компьютера")

    flag = True

    while flag:
        try:
            mode = int(input("\n\nВыберите 1 или 2, чтобы задать режим игры ----> "))
            if mode == 1:
                flag = False
                BattleshipsPVP()
            elif mode == 2:
                flag = False
                BattleshipsCOMP()
            else:
                continue
        except ValueError:
            print("Вы можете ввести только 1 или 2")


playbattleships()