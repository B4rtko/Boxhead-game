import random
from typing import Dict, List, Tuple

import pygame

from src.game_elements.Shooter import (
    GunFlameThrower,
    GunRifle,
    GunRocketLauncher,
    GunShotgun,
    Shooter,
)
from src.game_configs.Config_arena_sectors import (
    Sector2BotDirections,
    Sector3BotDirections,
    Sector4BotDirections,
    Sector5BotDirections,
)


class Arena(object):
    """
    Game arena instance
    """
    def __init__(
        self,
        game_screen: pygame.surface.Surface,
        gunpack_max_amount: int,
        map_layout: int,
        game_player: Shooter,
    ) -> None:
        pygame.init()

        self.game_player: Shooter = game_player
        self.game_screen: pygame.surface.Surface = game_screen
        self.game_screen_size: Tuple[float, float] = game_screen.get_size()
        self.gunpck_max_ammount: int = gunpack_max_amount
        self.map_layout: int = map_layout

        self.obsticles: List[Obsticle] = []
        self.gun_packs: List[GunPack] = []
        self.banned: List[Tuple[int, int, int, int]] = []

        self.sectors: Dict[int, SectorBase] = dict()

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
        arena = arena_dict[self.map_layout]
        arena()

    def arena_1(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.game_screen_size[0], 200, self.game_screen_size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        sector = Sector1(self, 11, 200, self.game_screen_size[0], 0, self.game_screen_size[1])

    def arena_2(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.game_screen_size[0], 200, self.game_screen_size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
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
        sector15 = Sector2(self, 15, 1100+bufor, self.game_screen_size[0], 0, 300-bufor)

        sector22 = Sector2(self, 22, 400+bufor, 900-bufor, 300-bufor, 400)
        sector25 = Sector2(self, 25, 1100+bufor, self.game_screen_size[0], 300-bufor, 400)

        sector32 = Sector2(self, 32, 400+bufor, 900-bufor, 400, 500+bufor)
        sector35 = Sector2(self, 35, 1100+bufor, self.game_screen_size[0], 400, 500+bufor)

        sector41 = Sector2(self, 41, 200, 400+bufor, 500+bufor, self.game_screen_size[1])
        sector42 = Sector2(self, 42, 400+bufor, 900-bufor, 500+bufor, self.game_screen_size[1])
        sector43 = Sector2(self, 43, 900-bufor, 1000, 500+bufor, self.game_screen_size[1])
        sector44 = Sector2(self, 44, 1000, 1100+bufor, 500+bufor, self.game_screen_size[1])
        sector45 = Sector2(self, 45, 1100+bufor, self.game_screen_size[0], 500+bufor, self.game_screen_size[1])

    def arena_3(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.game_screen_size[0], 200, self.game_screen_size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
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
        sector16 = Sector3(self, 16, 1615+bufor, self.game_screen_size[0], 0, 180-bufor)

        sector21 = Sector3(self, 21, 200, 505-bufor, 180-bufor, 540)
        sector26 = Sector3(self, 26, 1615+bufor, self.game_screen_size[0], 180-bufor, 540)

        sector31 = Sector3(self, 31, 200, 505-bufor, 540, 900+bufor)
        sector33 = Sector3(self, 33, 875+bufor, 1060, 540, 900+bufor)
        sector34 = Sector3(self, 34, 1060, 1245-bufor, 540, 900+bufor)
        sector36 = Sector3(self, 36, 1615-bufor, self.game_screen_size[0], 540, 900+bufor)

        sector41 = Sector3(self, 41, 200, 505-bufor, 900+bufor, self.game_screen_size[1])
        sector42 = Sector3(self, 42, 505-bufor, 875+bufor, 900+bufor, self.game_screen_size[1])
        sector43 = Sector3(self, 43, 875+bufor, 1060, 900+bufor, self.game_screen_size[1])
        sector44 = Sector3(self, 44, 1060, 1245-bufor, 900+bufor, self.game_screen_size[1])
        sector45 = Sector3(self, 45, 1245-bufor, 1615+bufor, 900+bufor, self.game_screen_size[1])
        sector46 = Sector3(self, 46, 1615+bufor, self.game_screen_size[0], 900+bufor, self.game_screen_size[1])

    def arena_4(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.game_screen_size[0], 200, self.game_screen_size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
        # prostokąt długi góra
        Obsticle(200, 1520, 180, 450, (255, 0, 0), self)
        # prostokąt długi dół
        Obsticle(600, self.game_screen_size[0], 630, 900, (255, 0, 0), self)

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        bufor = 9
        sector11 = Sector4(self, 11, 200, 600-bufor, 0, 180-bufor)
        sector12 = Sector4(self, 12, 600-bufor, 1520+bufor, 0, 180-bufor)
        sector13 = Sector4(self, 13, 1520+bufor, self.game_screen_size[0], 0, 180-bufor)

        sector23 = Sector4(self, 23, 1520+bufor, self.game_screen_size[0], 180-bufor, 450+bufor)

        sector31 = Sector4(self, 31, 200, 600-bufor, 450+bufor, 630-bufor)
        sector32 = Sector4(self, 32, 600-bufor, 1520+bufor, 450+bufor, 630-bufor)
        sector33 = Sector4(self, 33, 1520+bufor, self.game_screen_size[0], 450+bufor, 630-bufor)

        sector41 = Sector4(self, 41, 200, 600-bufor, 630-bufor, 900+bufor)

        sector51 = Sector4(self, 51, 200, 600-bufor, 900+bufor, self.game_screen_size[1])
        sector52 = Sector4(self, 52, 600-bufor, 1520+bufor, 900+bufor, self.game_screen_size[1])
        sector53 = Sector4(self, 53, 1520+bufor, self.game_screen_size[0], 900+bufor, self.game_screen_size[1])

    def arena_5(self):
        """
        function creates arena and its sectors
        """
        # frame
        Obsticle(self.game_screen_size[0], 200, self.game_screen_size[1], 0, (255, 0, 0), self)  # odwrotnie bo wewnątrz
        # prostokąt góra
        Obsticle(800, 1320, 0, 270, (255, 0, 0), self)
        # prostokąt dół
        Obsticle(800, 1320, 810, self.game_screen_size[1], (255, 0, 0), self)
        # prostokąt lewo
        Obsticle(200, 780, 405, 675, (255, 0, 0), self)
        # prostokąt prawo
        Obsticle(1340, self.game_screen_size[0], 405, 675, (255, 0, 0), self)

        for i in self.obsticles[1:]:
            self.banned.append((i.x_min-40, i.x_max+40, i.y_min-40, i.y_max+40))

        bufor = 9
        sector11 = Sector5(self, 11, 200, 500, 0, 135)
        sector12 = Sector5(self, 12, 500, 800-bufor, 0, 135)
        sector15 = Sector5(self, 15, 1320+bufor, 1620, 0, 135)
        sector16 = Sector5(self, 16, 1620, self.game_screen_size[0], 0, 135)

        sector21 = Sector5(self, 21, 200, 500, 135, 270+bufor)
        sector22 = Sector5(self, 22, 500, 800-bufor, 135, 270+bufor)
        sector25 = Sector5(self, 25, 1320+bufor, 1620, 135, 270+bufor)
        sector26 = Sector5(self, 26, 1620, self.game_screen_size[0], 135, 270+bufor)

        sector31 = Sector5(self, 31, 200, 500, 270+bufor, 405-bufor)
        sector32 = Sector5(self, 32, 500, 800-bufor, 270+bufor, 405-bufor)
        sector33 = Sector5(self, 33, 800-bufor, 1060, 270+bufor, 405-bufor)
        sector34 = Sector5(self, 34, 1060, 1320+bufor, 270+bufor, 405-bufor)
        sector35 = Sector5(self, 35, 1320+bufor, 1620, 270+bufor, 405-bufor)
        sector36 = Sector5(self, 36, 1620, self.game_screen_size[0], 270+bufor, 405-bufor)

        sector43 = Sector5(self, 43, 800+bufor, 1060, 405-bufor, 540)
        sector44 = Sector5(self, 44, 1060, 1320-bufor, 405-bufor, 540)

        sector53 = Sector5(self, 53, 800+bufor, 1060, 540, 675+bufor)
        sector54 = Sector5(self, 54, 1060, 1320-bufor, 540, 675+bufor)

        sector61 = Sector5(self, 61, 200, 500, 675+bufor, 810-bufor)
        sector62 = Sector5(self, 62, 500, 800-bufor, 675+bufor, 810-bufor)
        sector63 = Sector5(self, 63, 800-bufor, 1060, 675+bufor, 810-bufor)
        sector64 = Sector5(self, 64, 1060, 1320+bufor, 675+bufor, 810-bufor)
        sector65 = Sector5(self, 65, 1320+bufor, 1620, 675+bufor, 810-bufor)
        sector66 = Sector5(self, 66, 1620, self.game_screen_size[0], 675+bufor, 810-bufor)

        sector71 = Sector5(self, 71, 200, 500, 810-bufor, 945)
        sector72 = Sector5(self, 72, 500, 800-bufor, 810-bufor, 945)
        sector75 = Sector5(self, 75, 1320+bufor, 1620, 810-bufor, 945)
        sector76 = Sector5(self, 76, 1620, self.game_screen_size[0], 810-bufor, 945)

        sector81 = Sector5(self, 81, 200, 500, 945, self.game_screen_size[1])
        sector82 = Sector5(self, 82, 500, 800-bufor, 945, self.game_screen_size[1])
        sector85 = Sector5(self, 85, 1320+bufor, 1620, 945, self.game_screen_size[1])
        sector86 = Sector5(self, 86, 1620, self.game_screen_size[0], 945, self.game_screen_size[1])

    def create_gunpack(self):
        """
        function maintains gunpack creation
        :return:
        """
        if len(self.gun_packs) < self.gunpck_max_ammount:
            rand_pos_x = random.randint(200, self.game_screen_size[0])
            rand_pos_y = random.randint(0, self.game_screen_size[1])

            loop = True
            while loop:
                loop = False
                for i in self.banned:
                    if i[0] < rand_pos_x < i[1]:
                        for q in self.banned:
                            if q[2] < rand_pos_y < q[3]:
                                rand_pos_x = random.randint(200, self.game_screen_size[0])
                                rand_pos_y = random.randint(0, self.game_screen_size[1])
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
                i.type(self.game_player)
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
        self.x_min, self.x_max, self. y_min, self.y_max = x_min, x_max, y_min, y_max
        self.color = color
        self.arena_game_screen = arena.game_screen
        arena.obsticles.append(self)

    def draw(self):
        """
        function that maintains drawing obstacle-related stuff; it is run by the Game object in loop
        """
        points = [(self.x_min, self.y_min), (self.x_max, self.y_min), (self.x_max, self.y_max), (self.x_min, self.y_max)]
        pygame.draw.lines(self.arena_game_screen, self.color, True, points, 5)


class GunPack(object):
    """
    Gun Pack instance
    """
    def __init__(self, x_min, y_min, arena):
        length = 15
        self.arena = arena
        self.player = self.arena.game_player

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
        pygame.draw.rect(self.arena.game_screen, (255, 120, 0), self.rect)

    def if_picked(self):
        """
        function checks if instance is picked by player and if so marks self.picked var as True
        """
        if abs(self.player.pos[0]-self.pos[0]) < 25 and abs(self.player.pos[1]-self.pos[1]) < 25:
            self.picked = True


class SectorBase:
    def __init__(self, arena, sector, xmin, xmax, ymin, ymax) -> None:
        self.xmin, self.xmax, self.ymin, self.ymax = xmin, xmax, ymin, ymax
        self.arena = arena
        self.sector = sector
        self.arena.sectors[sector] = self  # TODO change way of work
        self.vector = None
        self.close = self.close_sectors()

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
        if self.sector != self.arena.game_player.active_sector:
            self.direction_dict()


class Sector1(SectorBase):
    """
    Sector instance
    """
    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        close_to_11 = [11]

        dir_match = {11: close_to_11}

        return dir_match[self.sector]

    def tick(self):
        pass


class Sector2(SectorBase):
    """
    Sector instance
    """
    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_match = Sector2BotDirections.dir_match_direction
        dir_vector = Sector2BotDirections.dir_vector

        self.vector = dir_vector[dir_match[self.sector][self.arena.game_player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        dir_match = Sector2BotDirections.dir_match_close_sectors
        return dir_match[self.sector]


class Sector3(SectorBase):
    """
    Sector instance
    """
    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_match = Sector3BotDirections.dir_match_direction
        dir_vector = Sector3BotDirections.dir_vector

        self.vector = dir_vector[dir_match[self.sector][self.arena.game_player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        dir_match = Sector3BotDirections.dir_match_close_sectors
        return dir_match[self.sector]


class Sector4(SectorBase):
    """
    Sector instance
    """
    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_match = Sector4BotDirections.dir_match_direction
        dir_vector = Sector4BotDirections.dir_vector

        self.vector = dir_vector[dir_match[self.sector][self.arena.game_player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        dir_match = Sector4BotDirections.dir_match_close_sectors
        return dir_match[self.sector]


class Sector5(SectorBase):
    """
    Sector instance
    """
    def direction_dict(self):
        """
        function matches current sector with direction that bot should keep to reach sector that player is currently in
        """
        dir_match = Sector5BotDirections.dir_match_direction
        dir_vector = Sector5BotDirections.dir_vector

        self.vector = dir_vector[dir_match[self.sector][self.arena.game_player.active_sector]]

    def close_sectors(self):
        """
        function is used to match close sectors to the current one
        :return: list
        """
        dir_match = Sector5BotDirections.dir_match_close_sectors
        return dir_match[self.sector]
