import os
import sys

import pygame
from pygame.locals import *

from src.game_configs.Config_layouts import config_pause_screen_layout
from src.game_elements.Result_screen import ResultScreen


class PauseScreen:
    """
    Game pause screen instance
    """
    def __init__(
        self,
        game,
        path_media_elements: str,
        main_clock: pygame.time.Clock,
    ) -> None:
        pygame.init()

        self.game = game
        self.screen = game.screen
        pygame.mouse.set_visible(0)
        
        self._path_media_elements: str = path_media_elements
        self._main_clock: pygame.time.Clock = main_clock

        self.sound_select = pygame.mixer.Sound(os.path.join(self.path_media_elements, "dzwieki", "menu_select.wav"))

        self.highlight_ind = 0
        self.buttons = ["wznów", "zakończ"]

        self.image_game = pygame.image.load(os.path.join(self.path_media_elements, "grafika_menu", "obraz_przed_pauza.png"))
        self.image_pause = pygame.image.load(os.path.join(self.path_media_elements, "grafika_menu", "pauza_przyciski.png"))
        self.image_index = pygame.image.load(os.path.join(self.path_media_elements, "grafika_menu", "wskaznik_bialy.png"))

        self.ind_position = config_pause_screen_layout

        self.move_pressed = False
        self.muted = self.game.menu.muted

        self.loop = True
        self.pause()
        
    @property
    def path_media_elements(self) -> str:
        return self._path_media_elements
        
    @property
    def main_clock(self) -> pygame.time.Clock:
        return self._main_clock

    def pause(self):
        """
        function with main loop
        """
        while self.loop:
            self.game.tps_delta += self.game.tps_clock.tick() / 1000
            while self.game.tps_delta > 1 / self.game.tps_max:
                self.game.tps_delta -= 1 / self.game.tps_max

            click = False
            highlighted = self.buttons[self.highlight_ind]

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and event.key in [K_UP, K_w, K_DOWN, K_s] and (not self.move_pressed) and (not self.muted):
                    self.sound_select.play()
                    self.move_pressed = True
                if event.type == KEYUP:
                    if event.key in [K_ESCAPE, K_p]:
                        self.loop = False
                    if event.key == K_m and not self.muted:
                        self.muted = True
                        self.game.muted = True
                        self.game.menu.muted = True
                        pygame.mixer.music.stop()
                    elif event.key == K_m and self.muted:
                        self.muted = False
                        self.game.muted = False
                        self.game.menu.muted = False
                        pygame.mixer.music.play(-1)
                    if event.key in [K_RETURN, K_SPACE]:
                        click = True
                    if event.key in [K_UP, K_w]:
                        self.move_pressed = False
                        if self.highlight_ind > 0:
                            self.highlight_ind -= 1
                        else:
                            self.highlight_ind = len(self.buttons)-1
                    if event.key in [K_DOWN, K_s]:
                        self.move_pressed = False
                        if self.highlight_ind < len(self.buttons)-1:
                            self.highlight_ind += 1
                        else:
                            self.highlight_ind = 0
            self.screen.fill((0,0,0))
            self.screen.blit(self.image_game, (0,0))
            self.screen.blit(self.image_pause, (0,0))
            self.screen.blit(self.image_index, self.ind_position[self.buttons[self.highlight_ind]])

            if highlighted == "wznów" and click:
                    self.loop = False
            elif highlighted == "zakończ" and click:
                    self.loop = False
                    ResultScreen(
                        game=self.game,
                        path_media_elements=self.path_media_elements,
                        main_clock=self.main_clock,
                    )
                    self.game.loop = False

            pygame.display.flip()
            self.main_clock.tick(30)
