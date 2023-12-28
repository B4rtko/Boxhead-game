import os
import sys

import pygame
from pygame.locals import *


class ResultScreen:
    """
    Game over screen instance
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

        self._path_media_elements: str = path_media_elements
        self._main_clock: pygame.time.Clock = main_clock

        pygame.mouse.set_visible(0)
        self.myfont = pygame.font.SysFont('Comic Sans MS', 40)

        self.image_result = pygame.image.load(os.path.join(self.path_media_elements, "grafika_menu", "podawanie_wyniku.png"))

        self.name = ""

        self.loop = True
        self.result()
    
    @property
    def path_media_elements(self) -> str:
        return self._path_media_elements
        
    @property
    def main_clock(self) -> pygame.time.Clock:
        return self._main_clock

    def result(self):
        """
        function with main loop
        """
        while self.loop:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP:
                    if event.key == K_ESCAPE:
                        self.loop = False
                        self.game.break_loop = True
                    if event.key == K_RETURN and len(self.name)>0:
                        self.loop = False
                        self.game.break_loop = True

                        with open(os.path.join(self.path_media_elements, "tablica_wynikow.txt"), "a")as file:
                            file.write(f"{self.name}:::{self.game.player.score};;;")
                    if event.key == K_BACKSPACE and len(self.name)>0:
                        self.name = self.name[:-1]
                    else:
                        if len(self.name)<10:
                            key = str(pygame.key.name(event.key))
                            if len(key) == 1:
                                self.name += key

            score_surface = self.myfont.render(f"{self.game.player.score}", False, (255, 255, 255))
            name_surface = self.myfont.render(f"{self.name}", False, (255, 255, 255))
            self.screen.fill((0,0,0))
            self.screen.blit(self.image_result, (0,0))
            self.game.screen.blit(score_surface, (960, 435))
            self.game.screen.blit(name_surface, (920, 590))

            pygame.display.flip()
            self.main_clock.tick(30)
