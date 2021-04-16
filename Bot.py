import pygame
from pygame.math import Vector2
import time


class Bot(object):
    """
    Bot instance
    """
    def __init__(self, game, x, y):
        self.game = game
        self.angle_player = None
        self.angle_move = None

        self.stop_moving = False

        self.speed = self.game.menu.dict_difficulty_config["bot_speed"]
        self.pos = Vector2(x,y)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

        self.start_attack = False
        self.last_attack = 0
        self.attack_time = self.game.menu.dict_difficulty_config["bot_attack_frequency"]
        self.attack_damage = self.game.menu.dict_difficulty_config["bot_damage"]

        self.hit_points_current = self.game.menu.dict_difficulty_config["bot_hitpoints"]
        self.active_sector = self.game.arena.sectors[11]

    def tick(self):
        """
        main function that maintains bot processes
        """
        self.connect()
        self.collision()
        self.move_control()

        if not self.stop_moving:
            self.add_force()
            self.start_attack = False

            # dodging obstacles while near
            if "up" in self.edge:
                self.acc += Vector2(0,3*self.speed)
            if "down" in self.edge:
                self.acc += Vector2(0,-3*self.speed)
            if "left" in self.edge:
                self.acc += Vector2(3*self.speed,0)
            if "right" in self.edge:
                self.acc += Vector2(-3*self.speed,0)
        else:
            self.vel*=0
            self.acc*=0

        # to make end of motion looks more natural
        self.vel *= 0.2

        # adding movement speed
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0
        self.alive()


    def alive(self):
        """
        function checks if bot's hitpoints are below 0 and if so, deletes bot and adds player's score
        """
        if self.hit_points_current>0:
            pass
        else:
            self.player.score += 1
            self.game.bots.remove(self)
            del self

    def connect(self):
        """
        function connects bot with other instances in game (player and arena) and gets angle from bot to player
        """
        self.player = self.game.player
        self.angle_player = Vector2(1,0).angle_to(self.player_search())
        self.arena = self.game.arena

    def player_search(self):
        """
        function generates vector from bot to player
        :return: Vector2
        """
        return Vector2(self.player.pos[0]-self.pos[0], self.player.pos[1]-self.pos[1])

    def move_control(self):
        if (self.pos-self.player.pos).length()<30:
            self.vel*=0
            self.stop_moving = True
            self.attack()
        elif (self.pos-self.player.pos).length()<200:
            self.stop_moving = False
            self.angle_move = Vector2(1, 0).angle_to(Vector2(self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]))
        else:
            self.stop_moving = False
            self.sector_movement()

    def attack(self):
        """
        function maintains bot's attack process
        """
        now = time.perf_counter()
        if now - self.last_attack > 0.2:
            if self.start_attack:
                if now - self.start_attack > self.attack_time:
                    self.player.hit_points_current -= self.attack_damage
                    self.last_attack = now
                    self.start_attack = False
            else:
                self.start_attack = now

    def sector_movement(self):
        """
        function maintains how bot should behave in his current position to player
        """
        self.sector_in()
        if self.active_sector.sector in self.game.arena.sectors[self.game.player.active_sector].close:
            self.angle_move = Vector2(1, 0).angle_to(Vector2(self.player.pos[0] - self.pos[0], self.player.pos[1] - self.pos[1]))
        else:
            self.angle_move = Vector2(1, 0).angle_to(self.active_sector.vector) + 360

    def sector_in(self):
        """
        function checks what is the bot's current arena sector
        """
        for i in self.game.arena.sectors:
            if self.game.arena.sectors[i].position_check(self):
                self.active_sector = self.game.arena.sectors[i]
                break

    def collision(self):
        """
        function checks if bot collides with obstacles or other bots
        """
        self.edge = self.arena.collision(self, 10)
        self.other_bots = self.game.bots.copy()
        self.other_bots.remove(self)
        for bot in self.other_bots:
            self.edge.extend(self.collision_other(bot))

    def collision_other(self, other):
        """
        function returns True if bot collides with other bot
        :param other: bot
        :return: bool
        """
        edge = []
        if 0 < self.pos[0] - other.pos[0] < 40 and abs(self.pos[1] - other.pos[1]) < 5:
            edge.append("left")
        if 0 < other.pos[0] - self.pos[0] < 40 and abs(other.pos[1] - self.pos[1]) < 5:
            edge.append("right")
        if 0 < self.pos[1] - other.pos[1] < 30 and abs(self.pos[0] - other.pos[0]) < 5:
            edge.append("up")
        if 0 < other.pos[1] - self.pos[1] < 30 and abs(other.pos[0] - self.pos[0]) < 5:
            edge.append("down")
        return edge

    def add_force(self):
        """
        function adds force to move bot
        """
        if self.angle_move:
            force = Vector2(self.speed, 0)
            force = force.rotate(self.angle_move)
            self.acc += force

    def draw(self):
        """
        function that maintains drawing bot-related stuff; it is run by the Game object in loop
        """
        self.draw_position()

    def draw_position(self):
        """
        function draws bot on the screen
        """
        points = [Vector2(0,-10), Vector2(5,5), Vector2(-5,5)]
        if self.angle_move:
            points = [p.rotate(90-self.angle_move) for p in points]
        points = [Vector2(p.x, p.y*-1) for p in points]
        points = [self.pos+p*3 for p in points]
        pygame.draw.polygon(self.game.screen,(0,180,0),points)
