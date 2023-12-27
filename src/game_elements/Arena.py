import random

import pygame
from pygame.math import Vector2

from src.game_elements.Shooter import GunPistol, GunRifle, GunShotgun, GunRocketLauncher, GunFlameThrower


class Arena(object):
    """
    Game arena instance
    """
    def __init__(self, game):
        pygame.init()

        self.game = game
        self.size = self.game.screen.get_size()

        self.gunpck_max_ammount = self.game.menu.dict_difficulty_config["gunpack_max_amount"]

        self.obsticles = []
        self.gun_packs = []
        self.banned = []

        self.sectors = dict()

        self.create_obsticles()

    def collision(self, player, bufor=5):
        """
        function maintains collision checking for game instances (idea was to check only player collision but things
        evolved and only 'player' param name lasts :D)
        :param player: instance to check collision of
        :param bufor: amount of place near instance that counts as collision
        :return: list
        """
        edge_square = self.collision_square(player, bufor)
        return edge_square

    def collision_square(self, player, bufor):
        """
        function checks if instance's position is in collision with arena obstacle (same thing with 'player' param like
        in collision func)
        :param player: instance to check collision of
        :param bufor: amount of place near instance that counts as collision
        :return: list
        """
        edge = []
        frame = True

        for i in self.obsticles:
            if frame:
                if i.x_max-bufor <= player.pos[0] <= i.x_max+bufor:
                    edge.append("left")
                if i.x_min+bufor >= player.pos[0] >= i.x_min-bufor:
                    edge.append("right")
                if i.y_max-bufor <= player.pos[1] <= i.y_max+bufor:
                    edge.append("up")
                if i.y_min+bufor >= player.pos[1] >= i.y_min-bufor:
                    edge.append("down")
                frame = False
            else:
                if i.x_max-2*bufor <= player.pos[0] <= i.x_max+bufor and i.y_min-bufor/3 <= player.pos[1] <= i.y_max+bufor/2:
                    edge.append("left")
                if i.x_min+2*bufor >= player.pos[0] >= i.x_min-bufor and i.y_min-bufor/2 <= player.pos[1] <= i.y_max+bufor/3:
                    edge.append("right")
                if i.y_max-2*bufor <= player.pos[1] <= i.y_max+bufor and i.x_min-bufor/3 <= player.pos[0] <= i.x_max+bufor/2:
                    edge.append("up")
                if i.y_min+2*bufor >= player.pos[1] >= i.y_min-bufor and i.x_min-bufor/2 <= player.pos[0] <= i.x_max+bufor/3:
                    edge.append("down")

        return edge

    def create_obsticles(self):
        """
        main function that arranges arena obstacles creation and sectors of movement usage
        """
        arena_dict = {1: self.arena_1, 2: self.arena_2, 3: self.arena_3, 4: self.arena_4, 5: self.arena_5}
        arena = arena_dict[self.game.map_layout]
        arena()

    def arena_1(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.size[0], 200, self.size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        sector = Sector1(self, 11, 200, self.size[0], 0, self.size[1])

    def arena_2(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.size[0], 200, self.size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
        # kwadrat lewo, środek
        Obsticle(200, 400, 300, 500, (255, 0, 0), self)
        # kwadrat prawo, środek
        Obsticle(900, 1100, 300, 500, (255, 0, 0), self)

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        bufor = 9
        sector11 = Sector2(self, 11, 200, 400+bufor, 0, 300-bufor)
        sector12 = Sector2(self, 12, 400+bufor, 900-bufor, 0, 300-bufor)
        sector13 = Sector2(self, 13, 900-bufor, 1000, 0, 300-bufor)
        sector14 = Sector2(self, 14, 1000, 1100+bufor, 0, 300-bufor)
        sector15 = Sector2(self, 15, 1100+bufor, self.size[0], 0, 300-bufor)

        sector22 = Sector2(self, 22, 400+bufor, 900-bufor, 300-bufor, 400)
        sector25 = Sector2(self, 25, 1100+bufor, self.size[0], 300-bufor, 400)

        sector32 = Sector2(self, 32, 400+bufor, 900-bufor, 400, 500+bufor)
        sector35 = Sector2(self, 35, 1100+bufor, self.size[0], 400, 500+bufor)

        sector41 = Sector2(self, 41, 200, 400+bufor, 500+bufor, self.size[1])
        sector42 = Sector2(self, 42, 400+bufor, 900-bufor, 500+bufor, self.size[1])
        sector43 = Sector2(self, 43, 900-bufor, 1000, 500+bufor, self.size[1])
        sector44 = Sector2(self, 44, 1000, 1100+bufor, 500+bufor, self.size[1])
        sector45 = Sector2(self, 45, 1100+bufor, self.size[0], 500+bufor, self.size[1])

    def arena_3(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.size[0], 200, self.size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
        # prostokąt lewo długi
        Obsticle(505, 875, 180, 900, (255, 0, 0), self)
        # kwadrat góra, środek
        Obsticle(875, 1245, 180, 540, (255, 0, 0), self)
        # prostokąt prawo, długi
        Obsticle(1245, 1615, 180, 900, (255, 0, 0), self)

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        bufor = 9
        sector11 = Sector3(self, 11, 200, 505-bufor, 0, 180-bufor)
        sector12 = Sector3(self, 12, 505-bufor, 875+bufor, 0, 180-bufor)
        sector13 = Sector3(self, 13, 875+bufor, 1060, 0, 180-bufor)
        sector14 = Sector3(self, 14, 1060, 1245-bufor, 0, 180-bufor)
        sector15 = Sector3(self, 15, 1245-bufor, 1615+bufor, 0, 180-bufor)
        sector16 = Sector3(self, 16, 1615+bufor, self.size[0], 0, 180-bufor)

        sector21 = Sector3(self, 21, 200, 505-bufor, 180-bufor, 540)
        sector26 = Sector3(self, 26, 1615+bufor, self.size[0], 180-bufor, 540)

        sector31 = Sector3(self, 31, 200, 505-bufor, 540, 900+bufor)
        sector33 = Sector3(self, 33, 875+bufor, 1060, 540, 900+bufor)
        sector34 = Sector3(self, 34, 1060, 1245-bufor, 540, 900+bufor)
        sector36 = Sector3(self, 36, 1615-bufor, self.size[0], 540, 900+bufor)

        sector41 = Sector3(self, 41, 200, 505-bufor, 900+bufor, self.size[1])
        sector42 = Sector3(self, 42, 505-bufor, 875+bufor, 900+bufor, self.size[1])
        sector43 = Sector3(self, 43, 875+bufor, 1060, 900+bufor, self.size[1])
        sector44 = Sector3(self, 44, 1060, 1245-bufor, 900+bufor, self.size[1])
        sector45 = Sector3(self, 45, 1245-bufor, 1615+bufor, 900+bufor, self.size[1])
        sector46 = Sector3(self, 46, 1615+bufor, self.size[0], 900+bufor, self.size[1])

    def arena_4(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.size[0], 200, self.size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
        # prostokąt długi góra
        Obsticle(200, 1520, 180, 450, (255, 0, 0), self)
        # prostokąt długi dół
        Obsticle(600, self.size[0], 630, 900, (255, 0, 0), self)

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        bufor = 9
        sector11 = Sector4(self, 11, 200, 600-bufor, 0, 180-bufor)
        sector12 = Sector4(self, 12, 600-bufor, 1520+bufor, 0, 180-bufor)
        sector13 = Sector4(self, 13, 1520+bufor, self.size[0], 0, 180-bufor)

        sector23 = Sector4(self, 23, 1520+bufor, self.size[0], 180-bufor, 450+bufor)

        sector31 = Sector4(self, 31, 200, 600-bufor, 450+bufor, 630-bufor)
        sector32 = Sector4(self, 32, 600-bufor, 1520+bufor, 450+bufor, 630-bufor)
        sector33 = Sector4(self, 33, 1520+bufor, self.size[0], 450+bufor, 630-bufor)

        sector41 = Sector4(self, 41, 200, 600-bufor, 630-bufor, 900+bufor)

        sector51 = Sector4(self, 51, 200, 600-bufor, 900+bufor, self.size[1])
        sector52 = Sector4(self, 52, 600-bufor, 1520+bufor, 900+bufor, self.size[1])
        sector53 = Sector4(self, 53, 1520+bufor, self.size[0], 900+bufor, self.size[1])

    def arena_5(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.size[0], 200, self.size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
        # prostokąt góra
        Obsticle(800, 1320, 0, 270, (255, 0, 0), self)
        # prostokąt dół
        Obsticle(800, 1320, 810, self.size[1], (255, 0, 0), self)
        # prostokąt lewo
        Obsticle(200, 780, 405, 675, (255, 0, 0), self)
        # prostokąt prawo
        Obsticle(1340, self.size[0], 405, 675, (255, 0, 0), self)

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        bufor = 9
        sector11 = Sector5(self, 11, 200, 500, 0, 135)
        sector12 = Sector5(self, 12, 500, 800-bufor, 0, 135)
        sector15 = Sector5(self, 15, 1320+bufor, 1620, 0, 135)
        sector16 = Sector5(self, 16, 1620, self.size[0], 0, 135)

        sector21 = Sector5(self, 21, 200, 500, 135, 270+bufor)
        sector22 = Sector5(self, 22, 500, 800-bufor, 135, 270+bufor)
        sector25 = Sector5(self, 25, 1320+bufor, 1620, 135, 270+bufor)
        sector26 = Sector5(self, 26, 1620, self.size[0], 135, 270+bufor)

        sector31 = Sector5(self, 31, 200, 500, 270+bufor, 405-bufor)
        sector32 = Sector5(self, 32, 500, 800-bufor, 270+bufor, 405-bufor)
        sector33 = Sector5(self, 33, 800-bufor, 1060, 270+bufor, 405-bufor)
        sector34 = Sector5(self, 34, 1060, 1320+bufor, 270+bufor, 405-bufor)
        sector35 = Sector5(self, 35, 1320+bufor, 1620, 270+bufor, 405-bufor)
        sector36 = Sector5(self, 36, 1620, self.size[0], 270+bufor, 405-bufor)

        sector43 = Sector5(self, 43, 800+bufor, 1060, 405-bufor, 540)
        sector44 = Sector5(self, 44, 1060, 1320-bufor, 405-bufor, 540)

        sector53 = Sector5(self, 53, 800+bufor, 1060, 540, 675+bufor)
        sector54 = Sector5(self, 54, 1060, 1320-bufor, 540, 675+bufor)

        sector61 = Sector5(self, 61, 200, 500, 675+bufor, 810-bufor)
        sector62 = Sector5(self, 62, 500, 800-bufor, 675+bufor, 810-bufor)
        sector63 = Sector5(self, 63, 800-bufor, 1060, 675+bufor, 810-bufor)
        sector64 = Sector5(self, 64, 1060, 1320+bufor, 675+bufor, 810-bufor)
        sector65 = Sector5(self, 65, 1320+bufor, 1620, 675+bufor, 810-bufor)
        sector66 = Sector5(self, 66, 1620, self.size[0], 675+bufor, 810-bufor)

        sector71 = Sector5(self, 71, 200, 500, 810-bufor, 945)
        sector72 = Sector5(self, 72, 500, 800-bufor, 810-bufor, 945)
        sector75 = Sector5(self, 75, 1320+bufor, 1620, 810-bufor, 945)
        sector76 = Sector5(self, 76, 1620, self.size[0], 810-bufor, 945)

        sector81 = Sector5(self, 81, 200, 500, 945, self.size[1])
        sector82 = Sector5(self, 82, 500, 800-bufor, 945, self.size[1])
        sector85 = Sector5(self, 85, 1320+bufor, 1620, 945, self.size[1])
        sector86 = Sector5(self, 86, 1620, self.size[0], 945, self.size[1])

    def create_gunpack(self):
        """
        function maintains gunpack creation
        :return:
        """
        if len(self.gun_packs) < self.gunpck_max_ammount:
            rand_pos_x = random.randint(200, self.size[0])
            rand_pos_y = random.randint(0, self.size[1])

            loop = True
            while loop:
                loop = False
                for i in self.banned:
                    if i[0] < rand_pos_x < i[1]:
                        for q in self.banned:
                            if q[2] < rand_pos_y < q[3]:
                                rand_pos_x = random.randint(200, self.size[0])
                                rand_pos_y = random.randint(0, self.size[1])
                                loop = True
                                break

            GunPack(rand_pos_x, rand_pos_y, self)

    def draw(self):
        """
        function that maintains drawing arena-related stuff; it is run by the Game object in loop
        """
        # obsticles
        for i in self.obsticles:
            i.draw()
        # gun packs
        for i in self.gun_packs:
            i.if_picked()
            if i.picked:
                i.type(self.game.player)
                self.gun_packs.remove(i)
                del self
            else:
                i.draw()


class Obsticle(object):
    """
    Obstacle instance (sorry for typo :D)
    """
    def __init__(self, x_min, x_max, y_min, y_max, color, arena):
        # x_min, y_min - lewy górny róg
        self.arena = arena
        self.x_min, self.x_max, self. y_min, self.y_max = x_min, x_max, y_min, y_max
        self.color = color
        self.arena.obsticles.append(self)

    def draw(self):
        """
        function that maintains drawing obstacle-related stuff; it is run by the Game object in loop
        """
        points = [(self.x_min, self.y_min), (self.x_max, self.y_min), (self.x_max, self.y_max), (self.x_min, self.y_max)]
        pygame.draw.lines(self.arena.game.screen, self.color, True, points, 5)


class GunPack(object):
    """
    Gun Pack instance
    """
    def __init__(self, x_min, y_min, arena):
        length = 15
        self.arena = arena
        self.player = self.arena.game.player

        self.rect = (x_min, y_min, length, length)
        self.pos = (x_min+length/2, y_min+length/2)

        self.picked = False

        types = [GunRifle, GunShotgun, GunRocketLauncher, GunFlameThrower]
        i = random.randint(0,len(types)-1)
        self.type = types[i]

        arena.gun_packs.append(self)

    def draw(self):
        """
        function that maintains drawing arena-related stuff; it is run by the Game object in loop
        """
        pygame.draw.rect(self.arena.game.screen, (255, 120, 0), self.rect)

    def if_picked(self):
        """
        function checks if instance is picked by player and if so marks self.picked var as True
        """
        if abs(self.player.pos[0]-self.pos[0]) < 25 and abs(self.player.pos[1]-self.pos[1]) < 25:
            self.picked = True


class Sector1:
    """
    Sector instance
    """
    def __init__(self, arena, sector, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.arena = arena
        self.sector = sector
        self.arena.sectors[sector] = self
        self.vector = None
        self.close = self.close_sectors()

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        close_to_11 = [11]

        dir_match = {11: close_to_11}

        return dir_match[self.sector]

    def position_check(self, other):
        """
        function can be used to check if player or bot is in current sector
        :param other: bot or player instance
        :return: bool
        """
        if (self.xmin <= other.pos[0] < self.xmax) and (self.ymin <= other.pos[1] < self.ymax):
            return True
        else:
            return False

    def tick(self):
        pass


class Sector2:
    """
    Sector instance
    """
    def __init__(self, arena, sector, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.arena = arena
        self.sector = sector
        self.arena.sectors[sector] = self
        self.vector = None
        self.close = self.close_sectors()

    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_dict11 = {12: "right", 13: "right", 14: "right", 15: "right",
                      22: "right", 25: "right",
                      32: "right", 35: "right",
                      41: "right", 42: "right", 43: "right", 44: "right", 45: "right"}
        dir_dict12 = {11: "left", 13: "right", 14: "right", 15: "right",
                      22: "down", 25: "right",
                      32: "down", 35: "right",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}
        dir_dict13 = {11: "left", 12: "left", 14: "right", 15: "right",
                      22: "left", 25: "right",
                      32: "left", 35: "right",
                      41: "left", 42: "left", 43: "left", 44: "right", 45: "right"}
        dir_dict14 = {11: "left", 12: "left", 13: "left", 15: "right",
                      22: "left", 25: "right",
                      32: "left", 35: "right",
                      41: "left", 42: "left", 43: "left", 44: "right", 45: "right"}
        dir_dict15 = {11: "left", 12: "left", 13: "left", 14: "left",
                      22: "left", 25: "down",
                      32: "left", 35: "down",
                      41: "left", 42: "left", 43: "down", 44: "down", 45: "down"}

        dir_dict22 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                      25: "up",
                      32: "down", 35: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}
        dir_dict25 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                      22: "up",
                      32: "up", 35: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}

        dir_dict32 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                      22: "up", 25: "up",
                      35: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}
        dir_dict35 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                      22: "down", 25: "up",
                      32: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down"}

        dir_dict41 = {11: "right", 12: "right", 13: "right", 14: "right", 15: "right",
                      22: "right", 25: "right",
                      32: "right", 35: "right",
                      42: "right", 43: "right", 44: "right", 45: "right"}
        dir_dict42 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up",
                      22: "up", 25: "right",
                      32: "up", 35: "right",
                      41: "left", 43: "right", 44: "right", 45: "right"}
        dir_dict43 = {11: "left", 12: "left", 13: "left", 14: "left", 15: "right",
                      22: "left", 25: "right",
                      32: "left", 35: "right",
                      41: "left", 42: "left", 44: "right", 45: "right"}
        dir_dict44 = {11: "left", 12: "left", 13: "left", 14: "right", 15: "right",
                      22: "left", 25: "right",
                      32: "left", 35: "right",
                      41: "left", 42: "left", 43: "left", 45: "right"}
        dir_dict45 = {11: "left", 12: "left", 13: "up", 14: "up", 15: "up",
                      22: "left", 25: "up",
                      32: "left", 35: "up",
                      41: "left", 42: "left", 43: "left", 44: "left"}


        dir_match = {11: dir_dict11, 12: dir_dict12, 13: dir_dict13, 14: dir_dict14, 15: dir_dict15,
                     22: dir_dict22, 25: dir_dict25, 32: dir_dict32, 35: dir_dict35,
                     41: dir_dict41, 42: dir_dict42, 43: dir_dict43, 44: dir_dict44, 45: dir_dict45}

        dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                      "right": Vector2(1,0), "down": Vector2(0,1)}

        self.vector = dir_vector[dir_match[self.sector][self.arena.game.player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        close_to_11 = [11, 12]
        close_to_12 = [12, 11, 13, 22]
        close_to_13 = [13, 12, 14]
        close_to_14 = [14, 13, 15]
        close_to_15 = [15, 14, 25]

        close_to_22 = [22, 12, 32]
        close_to_25 = [25, 15, 35]

        close_to_32 = [32, 22, 42]
        close_to_35 = [35, 25, 45]

        close_to_41 = [41, 42]
        close_to_42 = [42, 41, 43, 32]
        close_to_43 = [43, 42, 44]
        close_to_44 = [44, 43, 45]
        close_to_45 = [45, 44, 35]

        dir_match = {11: close_to_11, 12: close_to_12, 13: close_to_13, 14: close_to_14, 15: close_to_15,
                     22: close_to_22, 25: close_to_25,
                     32: close_to_32, 35: close_to_35,
                     41: close_to_41, 42: close_to_42, 43: close_to_43, 44: close_to_44, 45: close_to_45}

        return dir_match[self.sector]

    def position_check(self, other):
        """
        function can be used to check if player or bot is in current sector
        :param other: bot or player instance
        :return: bool
        """
        if (self.xmin <= other.pos[0] < self.xmax) and (self.ymin <= other.pos[1] < self.ymax):
            return True
        else:
            return False

    def tick(self):
        """
        function keeps sector's direction updated with the current player's active sector
        """
        if self.sector != self.arena.game.player.active_sector:
            self.direction_dict()


class Sector3:
    """
    Sector instance
    """
    def __init__(self, arena, sector, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.arena = arena
        self.sector = sector
        self.arena.sectors[sector] = self
        self.vector = None
        self.close = self.close_sectors()

    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_dict11 = {12: "right", 13: "right", 14: "right", 15: "right", 16: "right",
                      21: "down", 26: "right",
                      31: "down", 33: "down", 34: "down", 36: "right",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
        dir_dict12 = {11: "left", 13: "right", 14: "right", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "left", 34: "left", 36: "right",
                      41: "left", 42: "left", 43: "left", 44: "left", 45: "right", 46: "right"}
        dir_dict13 = {11: "left", 12: "left", 14: "right", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "left", 34: "right", 36: "right",
                      41: "left", 42: "left", 43: "left", 44: "right", 45: "right", 46: "right"}
        dir_dict14 = {11: "left", 12: "left", 13: "left", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "right", 34: "right", 36: "right",
                      41: "left", 42: "left", 43: "right", 44: "right", 45: "right", 46: "right"}
        dir_dict15 = {11: "left", 12: "left", 13: "left", 14: "left", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "right", 34: "right", 36: "right",
                      41: "left", 42: "right", 43: "right", 44: "right", 45: "right", 46: "right"}
        dir_dict16 = {11: "left", 12: "left", 13: "left", 14: "left", 15: "left",
                      21: "left", 26: "down",
                      31: "left", 33: "down", 34: "down", 36: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}

        dir_dict21 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                      26: "up",
                      31: "down", 33: "down", 34: "down", 36: "up",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
        dir_dict26 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                      21: "up",
                      31: "down", 33: "down", 34: "down", 36: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}

        dir_dict31 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                      21: "up", 26: "down",
                      33: "down", 34: "down", 36: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
        dir_dict33 = {11: "down", 12: "down", 13: "down", 14: "down", 15: "down", 16: "down",
                      21: "down", 26: "down",
                      31: "down", 34: "right", 36: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
        dir_dict34 = {11: "down", 12: "down", 13: "down", 14: "down", 15: "down", 16: "down",
                      21: "down", 26: "down",
                      31: "down", 33: "left", 36: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}
        dir_dict36 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                      21: "down", 26: "up",
                      31: "down", 33: "down", 34: "down",
                      41: "down", 42: "down", 43: "down", 44: "down", 45: "down", 46: "down"}

        dir_dict41 = {11: "up", 12: "up", 13: "up", 14: "up", 15: "up", 16: "right",
                      21: "up", 26: "right",
                      31: "up", 33: "right", 34: "right", 36: "right",
                      42: "right", 43: "right", 44: "right", 45: "right", 46: "right"}
        dir_dict42 = {11: "left", 12: "left", 13: "left", 14: "left", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "right", 34: "right", 36: "right",
                      41: "left", 43: "right", 44: "right", 45: "right", 46: "right"}
        dir_dict43 = {11: "left", 12: "left", 13: "left", 14: "right", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "up", 34: "up", 36: "right",
                      41: "left", 42: "left", 44: "right", 45: "right", 46: "right"}
        dir_dict44 = {11: "left", 12: "left", 13: "right", 14: "right", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "up", 34: "up", 36: "right",
                      41: "left", 42: "left", 43: "left", 45: "right", 46: "right"}
        dir_dict45 = {11: "left", 12: "right", 13: "right", 14: "right", 15: "right", 16: "right",
                      21: "left", 26: "right",
                      31: "left", 33: "left", 34: "left", 36: "right",
                      41: "left", 42: "left", 43: "left", 44: "left", 46: "right"}
        dir_dict46 = {11: "left", 12: "up", 13: "up", 14: "up", 15: "up", 16: "up",
                      21: "left", 26: "up",
                      31: "left", 33: "left", 34: "left", 36: "up",
                      41: "left", 42: "left", 43: "left", 44: "left", 45: "left"}


        dir_match = {11: dir_dict11, 12: dir_dict12, 13: dir_dict13, 14: dir_dict14, 15: dir_dict15, 16: dir_dict16,
                     21: dir_dict21, 26: dir_dict26,
                     31: dir_dict31, 33: dir_dict33, 34: dir_dict34, 36: dir_dict36,
                     41: dir_dict41, 42: dir_dict42, 43: dir_dict43, 44: dir_dict44, 45: dir_dict45, 46: dir_dict46}

        dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                      "right": Vector2(1,0), "down": Vector2(0,1)}

        self.vector = dir_vector[dir_match[self.sector][self.arena.game.player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        close_to_11 = [11, 12, 21]
        close_to_12 = [12, 11, 13]
        close_to_13 = [13, 12, 14]
        close_to_14 = [14, 13, 15]
        close_to_15 = [15, 14, 16]
        close_to_16 = [16, 15, 26]

        close_to_21 = [21, 11, 31]
        close_to_26 = [26, 16, 36]

        close_to_31 = [31, 21, 41]
        close_to_33 = [33, 34, 43, 44]
        close_to_34 = [34, 33, 44, 43]
        close_to_36 = [36, 26, 46]

        close_to_41 = [41, 31, 42]
        close_to_42 = [42, 41, 43]
        close_to_43 = [43, 42, 44, 33, 34]
        close_to_44 = [44, 43, 45, 34, 33]
        close_to_45 = [45, 44, 46]
        close_to_46 = [46, 45, 36]

        dir_match = {11: close_to_11, 12: close_to_12, 13: close_to_13, 14: close_to_14, 15: close_to_15, 16: close_to_16,
                     21: close_to_21, 26: close_to_26,
                     31: close_to_31, 33: close_to_33, 34: close_to_34, 36: close_to_36,
                     41: close_to_41, 42: close_to_42, 43: close_to_43, 44: close_to_44, 45: close_to_45, 46: close_to_46}

        return dir_match[self.sector]

    def position_check(self, other):
        """
        function can be used to check if player or bot is in current sector
        :param other: bot or player instance
        :return: bool
        """
        if (self.xmin <= other.pos[0] < self.xmax) and (self.ymin <= other.pos[1] < self.ymax):
            return True
        else:
            return False

    def tick(self):
        """
        function keeps sector's direction updated with the current player's active sector
        """
        if self.sector != self.arena.game.player.active_sector:
            self.direction_dict()


class Sector4:
    """
    Sector instance
    """
    def __init__(self, arena, sector, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.arena = arena
        self.sector = sector
        self.arena.sectors[sector] = self
        self.vector = None
        self.close = self.close_sectors()

    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_dict11 = {12: "right", 13: "right",
                      23: "right",
                      31: "right", 32: "right", 33: "right",
                      41: "right",
                      51: "right", 52: "right", 53: "right"}
        dir_dict12 = {11: "left", 13: "right",
                      23: "right",
                      31: "right", 32: "right", 33: "right",
                      41: "right",
                      51: "right", 52: "right", 53: "right"}
        dir_dict13 = {11: "left", 12: "left",
                      23: "down",
                      31: "down", 32: "down", 33: "down",
                      41: "down",
                      51: "down", 52: "down", 53: "down"}

        dir_dict23 = {11: "up", 12: "up", 13: "up",
                      31: "down", 32: "down", 33: "down",
                      41: "down",
                      51: "down", 52: "down", 53: "down"}

        dir_dict31 = {11: "right", 12: "right", 13: "right",
                      23: "right",
                      32: "right", 33: "right",
                      41: "down",
                      51: "down", 52: "down", 53: "down"}
        dir_dict32 = {11: "right", 12: "right", 13: "right",
                      23: "right",
                      31: "left", 33: "right",
                      41: "left",
                      51: "left", 52: "left", 53: "left"}
        dir_dict33 = {11: "up", 12: "up", 13: "up",
                      23: "up",
                      31: "left", 32: "left",
                      41: "left",
                      51: "left", 52: "left", 53: "left"}

        dir_dict41 = {11: "up", 12: "up", 13: "up",
                      23: "up",
                      31: "up", 32: "up", 33: "up",
                      51: "down", 52: "down", 53: "down"}

        dir_dict51 = {11: "up", 12: "up", 13: "up",
                      23: "up",
                      31: "up", 32: "up", 33: "up",
                      41: "up",
                      52: "right", 53: "right"}
        dir_dict52 = {11: "left", 12: "left", 13: "left",
                      23: "left",
                      31: "left", 32: "left", 33: "left",
                      41: "left",
                      51: "left", 53: "right"}
        dir_dict53 = {11: "left", 12: "left", 13: "left",
                      23: "left",
                      31: "left", 32: "left", 33: "left",
                      41: "left",
                      51: "left", 52: "left"}


        dir_match = {11: dir_dict11, 12: dir_dict12, 13: dir_dict13,
                     23: dir_dict23,
                     31: dir_dict31, 32: dir_dict32, 33: dir_dict33,
                     41: dir_dict41,
                     51: dir_dict51, 52: dir_dict52, 53: dir_dict53}

        dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                      "right": Vector2(1,0), "down": Vector2(0,1)}

        self.vector = dir_vector[dir_match[self.sector][self.arena.game.player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        close_to_11 = [11, 12]
        close_to_12 = [12, 11, 13]
        close_to_13 = [13, 12, 23]

        close_to_23 = [23, 13, 33]

        close_to_31 = [31, 32, 41]
        close_to_32 = [32, 31, 33]
        close_to_33 = [33, 32, 23]

        close_to_41 = [41, 31, 51]

        close_to_51 = [51, 41, 52]
        close_to_52 = [52, 51, 53]
        close_to_53 = [53, 52]

        dir_match = {11: close_to_11, 12: close_to_12, 13: close_to_13,
                     23: close_to_23,
                     31: close_to_31, 32: close_to_32, 33: close_to_33,
                     41: close_to_41,
                     51: close_to_51, 52: close_to_52, 53: close_to_53}

        return dir_match[self.sector]

    def position_check(self, other):
        """
        function can be used to check if player or bot is in current sector
        :param other: bot or player instance
        :return: bool
        """
        if (self.xmin <= other.pos[0] < self.xmax) and (self.ymin <= other.pos[1] < self.ymax):
            return True
        else:
            return False

    def tick(self):
        """
        function keeps sector's direction updated with the current player's active sector
        """
        if self.sector != self.arena.game.player.active_sector:
            self.direction_dict()


class Sector5:
    """
    Sector instance
    """
    def __init__(self, arena, sector, xmin, xmax, ymin, ymax):
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.arena = arena
        self.sector = sector
        self.arena.sectors[sector] = self
        self.vector = None
        self.close = self.close_sectors()

    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_dict11 = {12: "right", 15: "downright", 16: "downright",
                      21: "down", 22: "downright", 25: "downright", 26: "downright",
                      31: "down", 32: "downright", 33: "downright", 34: "downright", 35: "downright", 36: "downright",
                      43: "downright", 44: "downright",
                      53: "downright", 54: "downright",
                      61: "downright", 62: "downright", 63: "downright", 64: "downright", 65: "downright", 66: "downright",
                      71: "downright", 72: "downright", 75: "downright", 76: "downright",
                      81: "downright", 82: "downright", 85: "downright", 86: "downright"}
        dir_dict12 = {11: "left", 15: "down", 16: "down",
                      21: "downleft", 22: "down", 25: "down", 26: "down",
                      31: "downleft", 32: "down", 33: "down", 34: "down", 35: "down", 36: "down",
                      43: "down", 44: "down",
                      53: "down", 54: "down",
                      61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                      71: "down", 72: "down", 75: "down", 76: "down",
                      81: "down", 82: "down", 85: "down", 86: "down"}
        dir_dict15 = {11: "down", 12: "down", 16: "right",
                      21: "down", 22: "down", 25: "down", 26: "downright",
                      31: "down", 32: "down", 33: "down", 34: "down", 35: "down", 36: "downright",
                      43: "down", 44: "down",
                      53: "down", 54: "down",
                      61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                      71: "down", 72: "down", 75: "down", 76: "down",
                      81: "down", 82: "down", 85: "down", 86: "down"}
        dir_dict16 = {11: "downleft", 12: "downleft", 15: "left",
                      21: "downleft", 22: "downleft", 25: "downleft", 26: "down",
                      31: "downleft", 32: "downleft", 33: "downleft", 34: "downleft", 35: "downleft", 36: "down",
                      43: "downleft", 44: "downleft",
                      53: "downleft", 54: "downleft",
                      61: "downleft", 62: "downleft", 63: "downleft", 64: "downleft", 65: "downleft", 66: "downleft",
                      71: "downleft", 72: "downleft", 75: "downleft", 76: "downleft",
                      81: "downleft", 82: "downleft", 85: "downleft", 86: "downleft"}

        dir_dict21 = {11: "up", 12: "upright", 15: "downright", 16: "downright",
                      22: "right", 25: "downright", 26: "downright",
                      31: "down", 32: "downright", 33: "downright", 34: "downright", 35: "downright", 36: "downright",
                      43: "downright", 44: "downright",
                      53: "downright", 54: "downright",
                      61: "downright", 62: "downright", 63: "downright", 64: "downright", 65: "downright", 66: "downright",
                      71: "downright", 72: "downright", 75: "downright", 76: "downright",
                      81: "downright", 82: "downright", 85: "downright", 86: "downright"}
        dir_dict22 = {11: "upleft", 12: "up", 15: "down", 16: "down",
                      21: "left", 25: "down", 26: "down",
                      31: "downleft", 32: "down", 33: "down", 34: "down", 35: "down", 36: "down",
                      43: "down", 44: "down",
                      53: "down", 54: "down",
                      61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                      71: "down", 72: "down", 75: "down", 76: "down",
                      81: "down", 82: "down", 85: "down", 86: "down"}
        dir_dict25 = {11: "down", 12: "down", 15: "up", 16: "upright",
                      21: "down", 22: "down", 26: "right",
                      31: "down", 32: "down", 33: "down", 34: "down", 35: "down", 36: "downright",
                      43: "down", 44: "down",
                      53: "down", 54: "down",
                      61: "down", 62: "down", 63: "down", 64: "down", 65: "down", 66: "down",
                      71: "down", 72: "down", 75: "down", 76: "down",
                      81: "down", 82: "down", 85: "down", 86: "down"}
        dir_dict26 = {11: "downleft", 12: "downleft", 15: "upleft", 16: "up",
                      21: "downleft", 22: "downleft", 25: "left",
                      31: "downleft", 32: "downleft", 33: "downleft", 34: "downleft", 35: "downleft", 36: "down",
                      43: "downleft", 44: "downleft",
                      53: "downleft", 54: "downleft",
                      61: "downleft", 62: "downleft", 63: "downleft", 64: "downleft", 65: "downleft", 66: "downleft",
                      71: "downleft", 72: "downleft", 75: "downleft", 76: "downleft",
                      81: "downleft", 82: "downleft", 85: "downleft", 86: "downleft"}

        dir_dict31 = {11: "up", 12: "upright", 15: "right", 16: "right",
                      21: "up", 22: "upright", 25: "right", 26: "right",
                      32: "right", 33: "right", 34: "right", 35: "right", 36: "right",
                      43: "right", 44: "right",
                      53: "right", 54: "right",
                      61: "right", 62: "right", 63: "right", 64: "right", 65: "right", 66: "right",
                      71: "right", 72: "right", 75: "right", 76: "right",
                      81: "right", 82: "right", 85: "right", 86: "right"}
        dir_dict32 = {11: "upleft", 12: "up", 15: "right", 16: "right",
                      21: "upleft", 22: "up", 25: "right", 26: "right",
                      31: "left", 33: "right", 34: "right", 35: "right", 36: "right",
                      43: "right", 44: "right",
                      53: "right", 54: "right",
                      61: "right", 62: "right", 63: "right", 64: "right", 65: "right", 66: "right",
                      71: "right", 72: "right", 75: "right", 76: "right",
                      81: "right", 82: "right", 85: "right", 86: "right"}
        dir_dict33 = {11: "left", 12: "left", 15: "right", 16: "right",
                      21: "left", 22: "left", 25: "right", 26: "right",
                      31: "left", 32: "left", 34: "right", 35: "right", 36: "right",
                      43: "down", 44: "downright",
                      53: "down", 54: "downright",
                      61: "down", 62: "down", 63: "down", 64: "downright", 65: "downright", 66: "downright",
                      71: "down", 72: "down", 75: "downright", 76: "downright",
                      81: "down", 82: "down", 85: "downright", 86: "downright"}
        dir_dict34 = {11: "left", 12: "left", 15: "right", 16: "right",
                      21: "left", 22: "left", 25: "right", 26: "right",
                      31: "left", 32: "left", 33: "left", 35: "right", 36: "right",
                      43: "downleft", 44: "down",
                      53: "downleft", 54: "down",
                      61: "downleft", 62: "downleft", 63: "downleft", 64: "down", 65: "down", 66: "down",
                      71: "downleft", 72: "downleft", 75: "down", 76: "down",
                      81: "downleft", 82: "downleft", 85: "down", 86: "down"}
        dir_dict35 = {11: "left", 12: "left", 15: "up", 16: "upright",
                      21: "left", 22: "left", 25: "up", 26: "upright",
                      31: "left", 32: "left", 33: "left", 34: "left", 36: "right",
                      43: "left", 44: "left",
                      53: "left", 54: "left",
                      61: "left", 62: "left", 63: "left", 64: "left", 65: "left", 66: "left",
                      71: "left", 72: "left", 75: "left", 76: "left",
                      81: "left", 82: "left", 85: "left", 86: "left"}
        dir_dict36 = {11: "left", 12: "left", 15: "upleft", 16: "up",
                      21: "left", 22: "left", 25: "upleft", 26: "up",
                      31: "left", 32: "left", 33: "left", 34: "left", 35: "left",
                      43: "left", 44: "left",
                      53: "left", 54: "left",
                      61: "left", 62: "left", 63: "left", 64: "left", 65: "left", 66: "left",
                      71: "left", 72: "left", 75: "left", 76: "left",
                      81: "left", 82: "left", 85: "left", 86: "left"}

        dir_dict43 = {11: "up", 12: "up", 15: "upright", 16: "upright",
                      21: "up", 22: "up", 25: "upright", 26: "upright",
                      31: "up", 32: "up", 33: "up", 34: "upright", 35: "upright", 36: "upright",
                      44: "right",
                      53: "down", 54: "downright",
                      61: "down", 62: "down", 63: "down", 64: "downright", 65: "downright", 66: "downright",
                      71: "down", 72: "down", 75: "downright", 76: "downright",
                      81: "down", 82: "down", 85: "downright", 86: "downright"}
        dir_dict44 = {11: "upleft", 12: "upleft", 15: "up", 16: "up",
                      21: "upleft", 22: "upleft", 25: "up", 26: "up",
                      31: "upleft", 32: "upleft", 33: "upleft", 34: "up", 35: "up", 36: "up",
                      43: "left",
                      53: "downleft", 54: "down",
                      61: "downleft", 62: "downleft", 63: "downleft", 64: "down", 65: "down", 66: "down",
                      71: "downleft", 72: "downleft", 75: "down", 76: "down",
                      81: "downleft", 82: "downleft", 85: "down", 86: "down"}

        dir_dict53 = {11: "up", 12: "up", 15: "upright", 16: "upright",
                      21: "up", 22: "up", 25: "upright", 26: "upright",
                      31: "up", 32: "up", 33: "up", 34: "upright", 35: "upright", 36: "upright",
                      43: "up", 44: "upright",
                      54: "right",
                      61: "down", 62: "down", 63: "down", 64: "downright", 65: "downright", 66: "downright",
                      71: "down", 72: "down", 75: "downright", 76: "downright",
                      81: "down", 82: "down", 85: "downright", 86: "downright"}
        dir_dict54 = {11: "upleft", 12: "upleft", 15: "up", 16: "up",
                      21: "upleft", 22: "upleft", 25: "up", 26: "up",
                      31: "upleft", 32: "upleft", 33: "upleft", 34: "up", 35: "up", 36: "up",
                      43: "upleft", 44: "up",
                      53: "left",
                      61: "downleft", 62: "downleft", 63: "downleft", 64: "down", 65: "down", 66: "down",
                      71: "downleft", 72: "downleft", 75: "down", 76: "down",
                      81: "downleft", 82: "downleft", 85: "down", 86: "down"}

        dir_dict61 = {11: "right", 12: "right", 15: "right", 16: "right",
                      21: "right", 22: "right", 25: "right", 26: "right",
                      31: "right", 32: "right", 33: "right", 34: "right", 35: "right", 36: "right",
                      43: "right", 44: "right",
                      53: "right", 54: "right",
                      62: "right", 63: "right", 64: "right", 65: "right", 66: "right",
                      71: "down", 72: "downright", 75: "right", 76: "right",
                      81: "down", 82: "downright", 85: "right", 86: "right"}
        dir_dict62 = {11: "right", 12: "right", 15: "right", 16: "right",
                      21: "right", 22: "right", 25: "right", 26: "right",
                      31: "right", 32: "right", 33: "right", 34: "right", 35: "right", 36: "right",
                      43: "right", 44: "right",
                      53: "right", 54: "right",
                      61: "left", 63: "right", 64: "right", 65: "right", 66: "right",
                      71: "downleft", 72: "down", 75: "right", 76: "right",
                      81: "downleft", 82: "down", 85: "right", 86: "right"}
        dir_dict63 = {11: "up", 12: "up", 15: "upright", 16: "upright",
                      21: "up", 22: "up", 25: "upright", 26: "upright",
                      31: "up", 32: "up", 33: "up", 34: "upright", 35: "upright", 36: "upright",
                      43: "up", 44: "upright",
                      53: "up", 54: "upright",
                      61: "left", 62: "left", 64: "right", 65: "right", 66: "right",
                      71: "left", 72: "left", 75: "right", 76: "right",
                      81: "left", 82: "left", 85: "right", 86: "right"}
        dir_dict64 = {11: "upleft", 12: "upleft", 15: "up", 16: "up",
                      21: "upleft", 22: "upleft", 25: "up", 26: "up",
                      31: "upleft", 32: "upleft", 33: "upleft", 34: "up", 35: "up", 36: "up",
                      43: "upleft", 44: "up",
                      53: "upleft", 54: "up",
                      61: "left", 62: "left", 63: "left", 65: "right", 66: "right",
                      71: "left", 72: "left", 75: "right", 76: "right",
                      81: "left", 82: "left", 85: "right", 86: "right"}
        dir_dict65 = {11: "left", 12: "left", 15: "left", 16: "left",
                      21: "left", 22: "left", 25: "left", 26: "left",
                      31: "left", 32: "left", 33: "left", 34: "left", 35: "left", 36: "left",
                      43: "left", 44: "left",
                      53: "left", 54: "left",
                      61: "left", 62: "left", 63: "left", 64: "left", 66: "right",
                      71: "left", 72: "left", 75: "down", 76: "downright",
                      81: "left", 82: "left", 85: "down", 86: "downright"}
        dir_dict66 = {11: "left", 12: "left", 15: "left", 16: "left",
                      21: "left", 22: "left", 25: "left", 26: "left",
                      31: "left", 32: "left", 33: "left", 34: "left", 35: "left", 36: "left",
                      43: "left", 44: "left",
                      53: "left", 54: "left",
                      61: "left", 62: "left", 63: "left", 64: "left", 65: "left",
                      71: "left", 72: "left", 75: "downleft", 76: "down",
                      81: "left", 82: "left", 85: "downleft", 86: "down"}

        dir_dict71 = {11: "upright", 12: "upright", 15: "upright", 16: "upright",
                      21: "upright", 22: "upright", 25: "upright", 26: "upright",
                      31: "upright", 32: "upright", 33: "upright", 34: "upright", 35: "upright", 36: "upright",
                      43: "upright", 44: "upright",
                      53: "upright", 54: "upright",
                      61: "up", 62: "upright", 63: "upright", 64: "upright", 65: "upright", 66: "upright",
                      72: "right", 75: "upright", 76: "upright",
                      81: "down", 82: "downright", 85: "upright", 86: "upright"}
        dir_dict72 = {11: "up", 12: "up", 15: "up", 16: "up",
                      21: "up", 22: "up", 25: "up", 26: "up",
                      31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                      43: "up", 44: "up",
                      53: "up", 54: "up",
                      61: "upleft", 62: "up", 63: "up", 64: "up", 65: "up", 66: "up",
                      71: "left", 75: "up", 76: "up",
                      81: "downleft", 82: "down", 85: "up", 86: "up"}
        dir_dict75 = {11: "up", 12: "up", 15: "up", 16: "up",
                      21: "up", 22: "up", 25: "up", 26: "up",
                      31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                      43: "up", 44: "up",
                      53: "up", 54: "up",
                      61: "up", 62: "up", 63: "up", 64: "up", 65: "up", 66: "upright",
                      71: "up", 72: "up", 76: "right",
                      81: "up", 82: "up", 85: "down", 86: "downright"}
        dir_dict76 = {11: "upleft", 12: "upleft", 15: "upleft", 16: "upleft",
                      21: "upleft", 22: "upleft", 25: "upleft", 26: "upleft",
                      31: "upleft", 32: "upleft", 33: "upleft", 34: "upleft", 35: "upleft", 36: "upleft",
                      43: "upleft", 44: "upleft",
                      53: "upleft", 54: "upleft",
                      61: "upleft", 62: "upleft", 63: "upleft", 64: "upleft", 65: "upleft", 66: "up",
                      71: "upleft", 72: "upleft", 75: "left",
                      81: "upleft", 82: "upleft", 85: "downleft", 86: "down"}

        dir_dict81 = {11: "upright", 12: "upright", 15: "upright", 16: "upright",
                      21: "upright", 22: "upright", 25: "upright", 26: "upright",
                      31: "upright", 32: "upright", 33: "upright", 34: "upright", 35: "upright", 36: "upright",
                      43: "upright", 44: "upright",
                      53: "upright", 54: "upright",
                      61: "up", 62: "upright", 63: "upright", 64: "upright", 65: "upright", 66: "upright",
                      71: "up", 72: "upright", 75: "upright", 76: "upright",
                      82: "right", 85: "upright", 86: "upright"}
        dir_dict82 = {11: "up", 12: "up", 15: "up", 16: "up",
                      21: "up", 22: "up", 25: "up", 26: "up",
                      31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                      43: "up", 44: "up",
                      53: "up", 54: "up",
                      61: "upleft", 62: "up", 63: "up", 64: "up", 65: "up", 66: "up",
                      71: "upleft", 72: "up", 75: "up", 76: "up",
                      81: "left", 85: "up", 86: "up"}
        dir_dict85 = {11: "up", 12: "up", 15: "up", 16: "up",
                      21: "up", 22: "up", 25: "up", 26: "up",
                      31: "up", 32: "up", 33: "up", 34: "up", 35: "up", 36: "up",
                      43: "up", 44: "up",
                      53: "up", 54: "up",
                      61: "up", 62: "up", 63: "up", 64: "up", 65: "up", 66: "upright",
                      71: "up", 72: "up", 75: "up", 76: "upright",
                      81: "up", 82: "up", 86: "right"}
        dir_dict86 = {11: "upleft", 12: "upleft", 15: "upleft", 16: "upleft",
                      21: "upleft", 22: "upleft", 25: "upleft", 26: "upleft",
                      31: "upleft", 32: "upleft", 33: "upleft", 34: "upleft", 35: "upleft", 36: "upleft",
                      43: "upleft", 44: "upleft",
                      53: "upleft", 54: "upleft",
                      61: "upleft", 62: "upleft", 63: "upleft", 64: "upleft", 65: "upleft", 66: "up",
                      71: "upleft", 72: "upleft", 75: "upleft", 76: "up",
                      81: "upleft", 82: "upleft", 85: "left"}


        dir_match = {11: dir_dict11, 12: dir_dict12, 15: dir_dict15, 16: dir_dict16,
                     21: dir_dict21, 22: dir_dict22, 25: dir_dict25, 26: dir_dict26,
                     31: dir_dict31, 32: dir_dict32, 33: dir_dict33, 34: dir_dict34, 35: dir_dict35, 36: dir_dict36,
                     43: dir_dict43, 44: dir_dict44,
                     53: dir_dict53, 54: dir_dict54,
                     61: dir_dict61, 62: dir_dict62, 63: dir_dict63, 64: dir_dict64, 65: dir_dict65, 66: dir_dict66,
                     71: dir_dict71, 72: dir_dict72, 75: dir_dict75, 76: dir_dict76,
                     81: dir_dict81, 82: dir_dict82, 85: dir_dict85, 86: dir_dict86}

        dir_vector = {"left": Vector2(-1,0), "up": Vector2(0,-1),
                      "right": Vector2(1,0), "down": Vector2(0,1),
                      "upleft": Vector2(1,0).rotate(225), "upright": Vector2(1,0).rotate(315),
                      "downleft": Vector2(1,0).rotate(135), "downright": Vector2(1,0).rotate(45)}

        self.vector = dir_vector[dir_match[self.sector][self.arena.game.player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        close_to_11 = [11, 12, 21, 22, 31, 32]
        close_to_12 = [12, 11, 21, 22, 31, 32]
        close_to_15 = [15, 16, 25, 26, 35, 36]
        close_to_16 = [16, 15, 25, 26, 35, 36]

        close_to_21 = [21, 22, 11, 12, 31, 32]
        close_to_22 = [22, 21, 11, 12, 31, 32]
        close_to_25 = [25, 26, 15, 16, 35, 36]
        close_to_26 = [26, 25, 15, 16, 35, 36]

        close_to_31 = [31, 32, 11, 12, 21, 22]
        close_to_32 = [32, 31, 11, 12, 21, 22, 33]
        close_to_33 = [33, 34, 43, 44, 53, 54, 63, 64, 32]
        close_to_34 = [34, 33, 43, 44, 53, 54, 63, 64, 35]
        close_to_35 = [35, 36, 15, 16, 25, 26, 43]
        close_to_36 = [36, 35, 15, 16, 25, 26]

        close_to_43 = [43, 44, 33, 34, 53, 54, 63, 64]
        close_to_44 = [44, 43, 33, 34, 53, 54, 63, 64]

        close_to_53 = [53, 54, 33, 34, 43, 44, 63, 64]
        close_to_54 = [54, 53, 33, 34, 43, 44, 63, 64]

        close_to_61 = [61, 62, 71, 72, 81, 82]
        close_to_62 = [62, 61, 71, 72, 81, 82, 63]
        close_to_63 = [63, 64, 33, 34, 53, 54, 43, 44, 62]
        close_to_64 = [64, 63, 33, 34, 53, 54, 43, 44, 65]
        close_to_65 = [65, 66, 75, 76, 85, 86, 64]
        close_to_66 = [66, 65, 75, 76, 85, 86]

        close_to_71 = [71, 72, 61, 62, 81, 82]
        close_to_72 = [72, 71, 61, 62, 81, 82]
        close_to_75 = [75, 76, 65, 66, 85, 86]
        close_to_76 = [76, 75, 65, 66, 85, 86]

        close_to_81 = [81, 82, 61, 62, 71, 72]
        close_to_82 = [82, 81, 61, 62, 71, 72]
        close_to_85 = [85, 86, 65, 66, 75, 76]
        close_to_86 = [86, 85, 65, 66, 75, 76]

        dir_match = {11: close_to_11, 12: close_to_12, 15: close_to_15, 16: close_to_16,
                     21: close_to_21, 22: close_to_22, 25: close_to_25, 26: close_to_26,
                     31: close_to_31, 32: close_to_32, 33: close_to_33, 34: close_to_34, 35: close_to_35, 36: close_to_36,
                     43: close_to_43, 44: close_to_44,
                     53: close_to_53, 54: close_to_54,
                     61: close_to_61, 62: close_to_62, 63: close_to_63, 64: close_to_64, 65: close_to_65, 66: close_to_66,
                     71: close_to_71, 72: close_to_72, 75: close_to_75, 76: close_to_76,
                     81: close_to_81, 82: close_to_82, 85: close_to_85, 86: close_to_86}

        return dir_match[self.sector]

    def position_check(self, other):
        """
        function can be used to check if player or bot is in current sector
        :param other: bot or player instance
        :return: bool
        """
        if (self.xmin <= other.pos[0] < self.xmax) and (self.ymin <= other.pos[1] < self.ymax):
            return True
        else:
            return False

    def tick(self):
        """
        function keeps sector's direction updated with the current player's active sector
        """
        if self.sector != self.arena.game.player.active_sector:
            self.direction_dict()
