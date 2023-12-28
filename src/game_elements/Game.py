import os
import sys

import pygame
from pygame.locals import *

from src.game_elements.Arena import Arena
from src.game_elements.Gameplay import GamePlay
from src.game_elements.Pause_screen import PauseScreen
from src.game_elements.Result_screen import ResultScreen
from src.game_elements.Shooter import Shooter


class Game:
    """
    Game screen instance
    """
    def __init__(
        self,
        menu,
        path_media_elements: str,
        main_clock: pygame.time.Clock,
    ) -> None:
        self.tps_max = 40
        pygame.font.init()
        self.myfont = pygame.font.SysFont('Comic Sans MS', 18)
        pygame.mixer.pre_init(44100, -16, 1, 512)
        pygame.init()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.tps_clock = pygame.time.Clock()
        self.tps_delta = 0.0

        self.menu = menu
        self.control_buttons = menu.control_buttons
        self.map_layout = menu.map_layout
        
        self._path_media_elements: str = path_media_elements
        self._main_clock = main_clock

        self.player = Shooter(self)
        self.arena: Arena = Arena(
            game_screen = self.screen,
            gunpack_max_amount = self.menu.dict_difficulty_config["gunpack_max_amount"],
            map_layout = self.map_layout,
            game_player = self.player,
        )
        self.bots = []
        self.gameplay = GamePlay(self)

        self.muted = self.menu.muted

        self.loop = True
        self.pause_loop = False
        self.break_loop = False

        while self.loop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                elif event.type == pygame.KEYUP and event.key in [pygame.K_ESCAPE, pygame.K_p]:
                    pygame.image.save(self.screen, os.path.join(path_media_elements, "grafika_menu", "obraz_przed_pauza.png"))
                    PauseScreen(
                        game=self,
                        path_media_elements=self.path_media_elements,
                        main_clock=self.main_clock,
                    )
                if event.type == pygame.KEYUP and event.key == K_m and not self.muted:
                    self.muted = True
                    self.menu.muted = True
                    pygame.mixer.music.stop()
                elif event.type == pygame.KEYUP and event.key == K_m and self.muted:
                    self.muted = False
                    self.menu.muted = False
                    pygame.mixer.music.play(-1)

            if self.player.hit_points_current <= 0:
                ResultScreen(
                    game=self,
                    path_media_elements=self.path_media_elements,
                    main_clock=self.main_clock,
                )

            if self.break_loop:
                break

            # ticking
            self.tps_delta += self.tps_clock.tick()/1000
            while self.tps_delta > 1/self.tps_max:
                self.tick()
                self.tps_delta -= 1/self.tps_max

            # drawing
            self.screen.fill((39, 39, 39))
            self.draw()
            pygame.display.flip()
    
    @property
    def path_media_elements(self) -> str:
        return self._path_media_elements
        
    @property
    def main_clock(self) -> pygame.time.Clock:
        return self._main_clock

    def tick(self):
        """
        function maintains game instances (player, bots, arena) ticks
        """
        self.player.tick()
        for sec in self.arena.sectors:
            self.arena.sectors[sec].tick()
        for bot in self.bots:
            bot.tick()
        self.gameplay.tick()

    def draw(self):
        """
        function maintains drawing game object on screen
        """
        self.arena.draw()
        self.player.draw()
        self.gameplay.draw()
        for bot in self.bots:
            bot.draw()
