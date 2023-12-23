import random
import time

from Bot import Bot


class GamePlay:
    """
    Instance to coordinate some of the game processes
    """
    def __init__(self, game):
        self.game = game

        self.bots = self.game.bots

        self.gunpck_frequency = self.game.menu.dict_difficulty_config["gunpack_frequency"]

        self.time_wave_start = 0
        self.time_last_kill = 0
        self.wave_counter = 0
        self.time_last_gunpack = 0
        self.bot_ammount_wave = 0
        self.banned_places()

    def banned_places(self):
        """
        function that checks which places bots can be spawned in
        """
        ys1 = list(range(20, 1060, 5))
        ys2 = list(range(20, 1060, 5))
        x1, x2 = 220, self.game.arena.size[0]-20

        for y in range(20, 1060, 5):
            for ban in self.game.arena.banned:
                if ban[0] < x1 < ban[1] and ban[2] < y < ban[3]:
                    ys1.remove(y)
                if ban[0] < x2 < ban[1] and ban[2] < y < ban[3]:
                    ys2.remove(y)
        self.pos_dict_bot = {1: (x1, ys1), 2: (x2, ys2)}


    def tick(self):
        """
        function calls bot spawning function
        """
        self.connect()

    def connect(self):
        """
        function coordinates bot spawning process
        """
        bot_ammount_current = len(self.bots)
        if bot_ammount_current==0:
            self.wave_counter+=1
            self.bot_ammount_wave = ((self.wave_counter // 2) + 1) * 5
            bot_ammount_create = self.bot_ammount_wave if self.bot_ammount_wave<=50 else 50
            for _ in range(bot_ammount_create):
                pos_cofig = self.pos_dict_bot[random.randint(1,2)]
                start_pos = pos_cofig[0], random.sample(pos_cofig[1], 1)[0]
                self.bots.append(Bot(self.game, start_pos[0], start_pos[1]))
                self.bot_ammount_wave -= 1
        elif bot_ammount_current < 50 and self.bot_ammount_wave>0:
            bot_ammount_create = 50 - bot_ammount_current
            if self.bot_ammount_wave < bot_ammount_create:
                bot_ammount_create = self.bot_ammount_wave
            for _ in range(bot_ammount_create):
                pos_cofig = self.pos_dict_bot[random.randint(1,2)]
                start_pos = pos_cofig[0], random.sample(pos_cofig[1], 1)[0]
                self.bots.append(Bot(self.game, start_pos[0], start_pos[1]))
                self.bot_ammount_wave -= 1

        current_time = time.perf_counter()
        if current_time-self.time_last_gunpack > self.gunpck_frequency:
            self.game.arena.create_gunpack()
            self.time_last_gunpack = current_time

    def draw(self):
        """
        function draws level counter on screen
        """
        wave_counter = self.game.myfont.render(f"Poziom: {self.wave_counter}", False, (255, 255, 255))
        self.game.screen.blit(wave_counter, (5, 95))
