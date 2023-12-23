import pygame
from pygame.math import Vector2
import time, random
import math


class Shooter(object):
    """
    Player instance
    """
    def __init__(self, game):
        self.game = game
        self.movement_set()
        self.angle = 0
        self.last_shot = 0
        self.last_gun_change = 0

        self.pos = Vector2(1060,600)
        self.vel = Vector2(0,0)
        self.acc = Vector2(0,0)

        self.ammo_add_config()
        self.hitpoints_restore_config()

        self.guns = list()
        self.gun_types = dict()
        self.bullets = list()
        GunPistol(self)
        self.current_gun_ind = 0
        self.current_gun = self.gun_types[self.current_gun_ind]

        self.hit_points_current = 300
        self.hit_points_max = 300

        self.active_sector = 11

        self.score = 0

    def ammo_add_config(self):
        """
        function sets ammo gaining configuration depending on chosen difficulty level
        """
        if self.game.menu.dict_difficulty_config["ammo_amount"] == "duży":
            self.ammo_add_rifle = 80
            self.ammo_add_shotgun = 35
            self.ammo_add_rocket_launcher = 8
            self.ammo_add_flame_thrower = 700
        elif self.game.menu.dict_difficulty_config["ammo_amount"] == "średni":
            self.ammo_add_rifle = 70
            self.ammo_add_shotgun = 30
            self.ammo_add_rocket_launcher = 6
            self.ammo_add_flame_thrower = 500
        elif self.game.menu.dict_difficulty_config["ammo_amount"] == "niski":
            self.ammo_add_rifle = 70
            self.ammo_add_shotgun = 25
            self.ammo_add_rocket_launcher = 4
            self.ammo_add_flame_thrower = 400

    def hitpoints_restore_config(self):
        """
        function sets player hitpoints restoring configuration depending on chosen difficulty level
        """
        if self.game.menu.dict_difficulty_config["hp_restore"] == "duży":
            self.hitpoints_restore = 100
        elif self.game.menu.dict_difficulty_config["hp_restore"] == "średni":
            self.hitpoints_restore = 60
        elif self.game.menu.dict_difficulty_config["hp_restore"] == "niski":
            self.hitpoints_restore = 35

    def add_force(self, force):
        """
        function adds force that moves player
        """
        self.acc += force

    def gun_change_up(self):
        """
        function is used to change gun to next one
        """
        keys_pressed = pygame.key.get_pressed()
        if not keys_pressed[self.shot]:
            ind = self.guns.index(self.current_gun_ind)
            if ind < len(self.guns)-1:
                ind += 1
                self.current_gun_ind = self.guns[ind]
                self.current_gun = self.gun_types[self.current_gun_ind]
            else:
                self.current_gun_ind = 0
                self.current_gun = self.gun_types[self.current_gun_ind]

    def gun_change_down(self):
        """
        function is used to change gun to previous one
        """
        keys_pressed = pygame.key.get_pressed()
        if not keys_pressed[self.shot]:
            ind = self.guns.index(self.current_gun_ind)
            if ind > 0:
                ind -= 1
                self.current_gun_ind = self.guns[ind]
                self.current_gun = self.gun_types[self.current_gun_ind]
            else:
                self.current_gun_ind = self.guns[-1]
                self.current_gun = self.gun_types[self.current_gun_ind]

    def movement_set(self):
        """
        function sets control configuration depending on this typed in option menu
        """
        self.up = self.game.control_buttons["góra"]
        self.down = self.game.control_buttons["dół"]
        self.left = self.game.control_buttons["lewo"]
        self.right = self.game.control_buttons["prawo"]
        self.shot = self.game.control_buttons["strzał"]
        self.next_gun = self.game.control_buttons["następna"]
        self.previous_gun = self.game.control_buttons["poprzednia"]

    def tick(self):
        """
        function maintains player's processes
        """
        self.sector_in()
        self.connect()
        self.collision()

        keys_pressed = pygame.key.get_pressed()

        speed = 4

        # rozwiazanie problemu szybszego chodzenia na skos
        if (keys_pressed[self.up] and keys_pressed[self.right]) ^ (keys_pressed[self.up] and keys_pressed[self.left]) ^ \
                (keys_pressed[self.down] and keys_pressed[self.right]) ^ (keys_pressed[self.down] and keys_pressed[self.left]):
            speed = speed/math.sqrt(2)

        if keys_pressed[self.up] and "up" not in self.edge:
            self.add_force(Vector2(0,-speed))
        if keys_pressed[self.down] and "down" not in self.edge:
            self.add_force(Vector2(0,speed))
        if keys_pressed[self.left] and "left" not in self.edge:
            self.add_force(Vector2(-speed,0))
        if keys_pressed[self.right] and "right" not in self.edge:
            self.add_force(Vector2(speed,0))

        # spowalnianie
        self.vel *= 0.5

        # przyspiesznaie
        self.vel += self.acc
        self.pos += self.vel
        self.acc *= 0

        # zmiana broni
        timer_gun_change = time.perf_counter()
        if keys_pressed[self.next_gun] and len(self.guns) > 1 and timer_gun_change-self.last_gun_change > 0.22:
            self.gun_change_up()
            self.last_gun_change = timer_gun_change
        if keys_pressed[self.previous_gun] and len(self.guns) > 1 and timer_gun_change-self.last_gun_change > 0.22:
            self.gun_change_down()
            self.last_gun_change = timer_gun_change
        if keys_pressed[pygame.K_1] and timer_gun_change-self.last_gun_change > 0.22:
            self.current_gun_ind = 0
            self.current_gun = self.gun_types[self.guns[self.current_gun_ind]]
        if keys_pressed[pygame.K_2] and 1 in self.guns and timer_gun_change-self.last_gun_change > 0.22:
            self.current_gun_ind = self.guns.index(1)
            self.current_gun = self.gun_types[self.guns[self.current_gun_ind]]
        if keys_pressed[pygame.K_3] and 2 in self.guns and timer_gun_change-self.last_gun_change > 0.22:
            self.current_gun_ind = self.guns.index(2)
            self.current_gun = self.gun_types[self.guns[self.current_gun_ind]]
        if keys_pressed[pygame.K_4] and 3 in self.guns and timer_gun_change-self.last_gun_change > 0.22:
            self.current_gun_ind = self.guns.index(3)
            self.current_gun = self.gun_types[self.guns[self.current_gun_ind]]
        if keys_pressed[pygame.K_5] and 4 in self.guns and timer_gun_change-self.last_gun_change > 0.22:
            self.current_gun_ind = self.guns.index(4)
            self.current_gun = self.gun_types[self.guns[self.current_gun_ind]]

        # strzelanie
        timer_shot = time.perf_counter()
        if keys_pressed[self.shot] and timer_shot-self.last_shot > self.current_gun.shot_block and self.guns:
            if self.current_gun.ammo_current > 0:
                self.current_gun.shot()
            else:
                self.current_gun = self.gun_types[0]
            self.last_shot = timer_shot

    def connect(self):
        """
        function connects player with other instances in game (bot and arena) and gets angle from bot to player
        """
        self.bots = self.game.bots
        self.arena = self.game.arena

    def sector_in(self):
        """
        function checks what is the players's current arena sector
        """
        for i in self.game.arena.sectors:
            if self.game.arena.sectors[i].position_check(self):
                self.active_sector = self.game.arena.sectors[i].sector
                break

    def collision(self):
        """
        function checks if player collides with obstacles or bots
        """
        self.edge = self.arena.collision(self, 25)
        for i in self.bots:
            self.edge.extend(self.collision_other(i))

    def collision_other(self, other):
        """
        function returns list of directions that leads to collision with bot
        :param other: bot instance
        :return: list
        """
        edge = []
        if 0 < self.pos[0] - other.pos[0] < 25 and abs(self.pos[1] - other.pos[1]) < 20:
            edge.append("left")
        if 0 < other.pos[0] - self.pos[0] < 25 and abs(self.pos[1] - other.pos[1]) < 20:
            edge.append("right")
        if 0 < self.pos[1] - other.pos[1] < 25 and abs(self.pos[0] - other.pos[0]) < 20:
            edge.append("up")
        if 0 < other.pos[1] - self.pos[1] < 25 and abs(self.pos[0] - other.pos[0]) < 20:
            edge.append("down")
        return edge

    def draw(self):
        """
        function that maintains drawing player-related stuff; it is run by the Game object in loop
        """
        self.angle = self.vel.angle_to(Vector2(0,1))
        self.draw_bullets()
        self.draw_position()
        self.draw_player_status()

    def draw_position(self):
        """
        function draws player on the screen
        """
        # podstawowy trójkąt
        points = [Vector2(0,-10), Vector2(5,5), Vector2(-5,5)]
        # obrót
        points = [p.rotate(self.angle) for p in points]
        points = [Vector2(p.x, p.y*-1) for p in points]
        # doajemy pozycję
        points = [self.pos+p*3 for p in points]
        # rysowanie
        pygame.draw.polygon(self.game.screen,(0,100,255),points)

    def draw_bullets(self):
        """
        function calls draw functions in shoted bullets
        """
        for i in self.bullets:
            i.draw()

    def draw_player_status(self):
        """
        function draws player ammo status, gun-type name, hitpoints bar and score
        """
        gun_type_surface = self.game.myfont.render(f"Broń: {str(self.current_gun)}", False, (255, 255, 255))
        ammo_surface = self.game.myfont.render(f"Amunicja: {self.current_gun.ammo_current}/{self.current_gun.ammo_max}",False, (255, 255, 255))
        score_surface = self.game.myfont.render(f"Wynik: {self.score}",False, (255, 255, 255))
        self.game.screen.blit(gun_type_surface, (5, 0))
        self.game.screen.blit(ammo_surface, (5, 20))
        self.game.screen.blit(score_surface, (5, 70))

        hp_current = (5, 50, ((self.hit_points_current/self.hit_points_max)*150)//1, 20)
        hp_max = (5, 50, 150, 20)
        pygame.draw.rect(self.game.screen, (0, 255, 0), hp_current, 0)
        pygame.draw.rect(self.game.screen, (255, 0, 0), hp_max, 2)


class GunPistol(object):
    """
    Pistol gun instance
    """
    def __init__(self, player):
        self.player = player
        self.shot_block = 0.3
        self.player.guns.append(0)
        self.player.gun_types[0] = self
        self.ammo_current = 9999
        self.ammo_max = 9999

    def __str__(self):
        return "Pistolet"

    def shot(self):
        """
        function creates bullet instance when shot button typed
        """
        self.pos = self.player.pos
        self.angle = self.player.angle
        bullet = BulletPistol(self, self.pos, self.angle)
        self.player.bullets.append(bullet)


class GunRifle(object):
    """
    Rifle gun instance
    """
    def __init__(self, player):
        self.player = player
        self.shot_block = 0.1
        self.ammo_max = 500
        self.ammo_current = self.player.ammo_add_rifle
        if 1 not in self.player.guns:
            # dodanie broni
            self.player.guns.append(1)
            self.player.guns.sort()
            self.player.gun_types[1] = self
        else:
            # uzupełnienie amunicji
            if self.player.gun_types[1].ammo_max == self.player.gun_types[1].ammo_current:
                if self.player.hit_points_max - self.player.hit_points_current >= self.player.hitpoints_restore:
                    self.player.hit_points_current += self.player.hitpoints_restore
                else:
                    self.player.hit_points_current = self.player.hit_points_max
            elif self.player.gun_types[1].ammo_max - self.player.gun_types[1].ammo_current <= self.player.ammo_add_rifle:
                self.player.gun_types[1].ammo_current = self.player.gun_types[1].ammo_max
            else:
                self.player.gun_types[1].ammo_current += self.player.ammo_add_rifle

    def __str__(self):
        return "Karabin"

    def shot(self):
        """
        function creates bullet instance when shot button typed
        """
        if self.ammo_current > 0:
            self.pos = self.player.pos
            self.angle = self.player.angle
            bullet = BulletPistol(self, self.pos, self.angle)
            self.player.bullets.append(bullet)
            self.ammo_current -= 1


class GunShotgun(object):
    """
    Shotgun gun instance
    """
    def __init__(self, player):
        self.player = player
        self.shot_block = 0.4
        self.ammo_max = 150
        self.ammo_current = self.player.ammo_add_shotgun
        if 2 not in self.player.guns:
            # dodanie broni
            self.player.guns.append(2)
            self.player.guns.sort()
            self.player.gun_types[2] = self
        else:
            # uzupełnienie amunicji
            if self.player.gun_types[2].ammo_max == self.player.gun_types[2].ammo_current:
                if self.player.hit_points_max - self.player.hit_points_current >= self.player.hitpoints_restore:
                    self.player.hit_points_current += self.player.hitpoints_restore
                else:
                    self.player.hit_points_current = self.player.hit_points_max
            elif self.player.gun_types[2].ammo_max - self.player.gun_types[2].ammo_current <= self.player.ammo_add_shotgun:
                self.player.gun_types[2].ammo_current = self.player.gun_types[2].ammo_max
            else:
                self.player.gun_types[2].ammo_current += self.player.ammo_add_shotgun

    def __str__(self):
        return "Strzelba"

    def shot(self):
        """
        function creates bullet instance when shot button typed
        """
        if self.ammo_current > 0:
            self.pos = self.player.pos
            self.angle = self.player.angle
            for i in [-12, -9, -6, -3, 0, 3, 6, 9, 12]:
                bullet = BulletShotgun(self, self.pos, self.angle+i)
                self.player.bullets.append(bullet)
            self.ammo_current -= 1


class GunRocketLauncher(object):
    """
    Rocket launcher gun instance
    """
    def __init__(self, player):
        self.player = player
        self.shot_block = 0.7
        self.ammo_max = 40
        self.ammo_current = self.player.ammo_add_rocket_launcher
        if 3 not in self.player.guns:
            # dodanie broni
            self.player.guns.append(3)
            self.player.guns.sort()
            self.player.gun_types[3] = self
        else:
            # uzupełnienie amunicji
            if self.player.gun_types[3].ammo_max == self.player.gun_types[3].ammo_current:
                if self.player.hit_points_max - self.player.hit_points_current >= self.player.hitpoints_restore:
                    self.player.hit_points_current += self.player.hitpoints_restore
                else:
                    self.player.hit_points_current = self.player.hit_points_max
            elif self.player.gun_types[3].ammo_max - self.player.gun_types[3].ammo_current <= self.player.ammo_add_rocket_launcher:
                self.player.gun_types[3].ammo_current = self.player.gun_types[3].ammo_max
            else:
                self.player.gun_types[3].ammo_current += self.player.ammo_add_rocket_launcher

    def __str__(self):
        return "Rakietnica"

    def shot(self):
        """
        function creates bullet instance when shot button typed
        """
        if self.ammo_current > 0:
            self.pos = self.player.pos
            self.angle = self.player.angle
            bullet = BulletRocketMain(self, self.pos, self.angle)
            self.player.bullets.append(bullet)
            self.ammo_current -= 1


class GunFlameThrower(object):
    """
    Flame thrower gun instance
    """
    def __init__(self, player):
        self.player = player
        self.shot_block = 0.00004
        self.ammo_max = 1500
        self.ammo_current = self.player.ammo_add_flame_thrower
        if 4 not in self.player.guns:
            # dodanie broni
            self.player.guns.append(4)
            self.player.guns.sort()
            self.player.gun_types[4] = self

        else:
            # uzupełnienie amunicji
            if self.player.gun_types[4].ammo_max == self.player.gun_types[4].ammo_current:
                if self.player.hit_points_max - self.player.hit_points_current >= self.player.hitpoints_restore:
                    self.player.hit_points_current += self.player.hitpoints_restore
                else:
                    self.player.hit_points_current = self.player.hit_points_max
            elif self.player.gun_types[4].ammo_max - self.player.gun_types[4].ammo_current <= self.player.ammo_add_flame_thrower:
                self.player.gun_types[4].ammo_current = self.player.gun_types[4].ammo_max
            else:
                self.player.gun_types[4].ammo_current += self.player.ammo_add_flame_thrower

    def __str__(self):
        return "Miotacz ognia"

    def shot(self):
        """
        function creates bullet instance when shot button typed
        """
        if self.ammo_current > 0:
            self.pos = self.player.pos
            self.angle = self.player.angle
            for i in [-3,0,3]:
                bullet = BulletFlameThrower(self, self.pos, self.angle+i)
                self.player.bullets.append(bullet)
            self.ammo_current -= 1


class BulletPistol(object):
    """
    Bullet instance that is shot by pistol gun or rifle gun
    """
    def __init__(self, gun, pos, angle):
        self.gun = gun
        self.pos = Vector2(pos[0], pos[1])
        self.angle = angle
        self.vel = Vector2(4*math.sin(angle/180*math.pi),4*math.cos(angle/180*math.pi))

    def draw(self):
        """
        function that maintains drawing bullet and moving it
        """
        pygame.draw.circle(self.gun.player.game.screen, (0, 255, 0), (int(self.pos[0]), int(self.pos[1])), 2)
        self.bullet_move()

    def bullet_move(self):
        """
        function that coordinates bullet movement and checks if it collides with bot or obstacle
        """
        self.pos += self.vel
        edge = self.gun.player.game.arena.collision(self)
        if edge:
            self.gun.player.bullets.remove(self)
            del self
        else:
            for bot in self.gun.player.game.bots:
                if self.collision_bot(bot):
                    bot.hit_points_current -= 19
                    self.gun.player.bullets.remove(self)
                    del self
                    break

    def collision_bot(self, bot):
        """
        function checks if bullet collides with bot
        :param bot: bot instance
        :return: bool
        """
        if abs(self.pos[0] - bot.pos[0]) < 25 and abs(self.pos[1] - bot.pos[1]) < 6:
            return True
        elif abs(self.pos[1] - bot.pos[1]) < 25 and abs(self.pos[0] - bot.pos[0]) < 6:
            return True
        return False


class BulletShotgun(object):
    """
    Bullet instance that is shot by pistol gun or rifle gun
    """
    def __init__(self, gun, pos, angle):
        self.gun = gun
        self.pos = Vector2(pos[0], pos[1])
        self.pos_start = Vector2(pos[0], pos[1])
        self.angle = angle
        self.vel = Vector2(4*math.sin(angle/180*math.pi),4*math.cos(angle/180*math.pi))

    def draw(self):
        """
        function that maintains drawing bullet and moving it
        """
        pygame.draw.circle(self.gun.player.game.screen, (0, 255, 0), (int(self.pos[0]), int(self.pos[1])), 2)
        self.bullet_move()

    def bullet_move(self):
        """
        function that coordinates bullet movement and checks if it collides with bot or obstacle
        """
        self.pos += self.vel
        edge = self.gun.player.game.arena.collision(self)
        if (self.pos-self.pos_start).length() > 150 or edge:
            self.gun.player.bullets.remove(self)
            del self
        else:
            for bot in self.gun.player.game.bots:
                if self.collision_bot(bot):
                    bot.hit_points_current -= 17
                    self.gun.player.bullets.remove(self)
                    del self
                    break


    def collision_bot(self, bot):
        """
        function checks if bullet collides with bot
        :param bot: bot instance
        :return: bool
        """
        if abs(self.pos[0] - bot.pos[0]) < 20 and abs(self.pos[1] - bot.pos[1]) < 3:
            return True
        elif abs(self.pos[1] - bot.pos[1]) < 20 and abs(self.pos[0] - bot.pos[0]) < 3:
            return True
        return False


class BulletRocketMain(object):
    """
    Bullet instance that is shot by pistol gun or rifle gun
    """
    def __init__(self, gun, pos, angle):
        self.gun = gun
        self.pos = Vector2(pos[0], pos[1])
        self.angle = angle
        self.vel = Vector2(4*math.sin(angle/180*math.pi),4*math.cos(angle/180*math.pi))

    def draw(self):
        """
        function that maintains drawing bullet and moving it
        """
        pygame.draw.circle(self.gun.player.game.screen, (0, 255, 0), (int(self.pos[0]), int(self.pos[1])), 2)
        self.bullet_move()

    def bullet_move(self):
        """
        function that coordinates bullet movement and checks if it collides with bot or obstacle
        """
        self.pos += self.vel
        edge = self.gun.player.game.arena.collision(self)
        if edge:
            for i in range(90):
                bullet = BulletRocketRecursed(self.gun, self.pos, (self.angle + i * 4))
                self.gun.player.bullets.append(bullet)
            self.gun.player.bullets.remove(self)
            del self
        else:
            for bot in self.gun.player.game.bots:
                if self.collision_bot(bot):
                    for i in range(90):
                        bullet = BulletRocketRecursed(self.gun, self.pos, (self.angle+i*4))
                        self.gun.player.bullets.append(bullet)
                    self.gun.player.bullets.remove(self)
                    del self
                    break

    def collision_bot(self, bot):
        """
        function checks if bullet collides with bot
        :param bot: bot instance
        :return: bool
        """
        if abs(self.pos[0] - bot.pos[0]) < 20 and abs(self.pos[1] - bot.pos[1]) < 4:
            return True
        elif abs(self.pos[1] - bot.pos[1]) < 20 and abs(self.pos[0] - bot.pos[0]) < 4:
            return True
        return False


class BulletRocketRecursed(object):
    """
    Bullet instance that is shot by pistol gun or rifle gun
    """
    def __init__(self, gun, pos, angle):
        self.gun = gun
        self.pos = Vector2(pos[0], pos[1])
        self.pos_start = Vector2(pos[0], pos[1])
        self.angle = angle
        self.vel = Vector2(4*math.sin(angle/180*math.pi),4*math.cos(angle/180*math.pi))
        self.timer_start = time.perf_counter()

    def draw(self):
        """
        function that maintains drawing bullet and moving it
        """
        pygame.draw.circle(self.gun.player.game.screen, (0, 255, 0), (int(self.pos[0]), int(self.pos[1])), 2)
        self.bullet_move()

    def bullet_move(self):
        """
        function that coordinates bullet movement and checks if it collides with bot or obstacle
        """
        self.pos += self.vel
        edge = self.gun.player.game.arena.collision(self, 2)
        now = time.perf_counter()
        if (self.pos-self.pos_start).length() > 70 or (edge and now - self.timer_start > 0.0001):
            self.gun.player.bullets.remove(self)
            del self
        else:
            for bot in self.gun.player.game.bots:
                if self.collision_bot(bot):
                    bot.hit_points_current -= 17
            if self.collision_bot(self.gun.player):
                self.gun.player.hit_points_current -= 1

    def collision_bot(self, bot):
        """
        function checks if bullet collides with bot
        :param bot: bot instance
        :return: bool
        """
        if abs(self.pos[0] - bot.pos[0]) < 20 and abs(self.pos[1] - bot.pos[1]) < 4:
            return True
        elif abs(self.pos[1] - bot.pos[1]) < 20 and abs(self.pos[0] - bot.pos[0]) < 4:
            return True
        return False


class BulletFlameThrower(object):
    """
    Bullet instance that is shot by pistol gun or rifle gun
    """
    def __init__(self, gun, pos, angle):
        self.gun = gun
        self.pos = Vector2(pos[0], pos[1])
        self.pos_start = Vector2(pos[0], pos[1])
        self.angle = angle
        self.vel = Vector2(4*math.sin(angle/180*math.pi),4*math.cos(angle/180*math.pi))
        self.timer_start = time.perf_counter()

    def draw(self):
        """
        function that maintains drawing bullet and moving it
        """
        pygame.draw.circle(self.gun.player.game.screen, (239, random.sample([44, 56, 70, 89], 1)[0], 0), (int(self.pos[0]), int(self.pos[1])), 5)
        self.bullet_move()

    def bullet_move(self):
        """
        function that coordinates bullet movement and checks if it collides with bot or obstacle
        """
        self.pos += self.vel
        edge = self.gun.player.game.arena.collision(self, 2)

        if (self.pos-self.pos_start).length() > 180 or edge:
            self.gun.player.bullets.remove(self)
            del self
        else:
            for bot in self.gun.player.game.bots:
                if self.collision_bot(bot):
                    bot.hit_points_current -= 0.25

    def collision_bot(self, bot):
        """
        function checks if bullet collides with bot
        :param bot: bot instance
        :return: bool
        """
        if abs(self.pos[0] - bot.pos[0]) < 20 and abs(self.pos[1] - bot.pos[1]) < 2:
            return True
        elif abs(self.pos[1] - bot.pos[1]) < 20 and abs(self.pos[0] - bot.pos[0]) < 2:
            return True
        return False
